__author__ = "Andrew Leech"
__copyright__ = "Copyright 2017, alelec"
__license__ = "MIT"
__maintainer__ = "Andrew Leech"
__email__ = "andrew@alelec.net"

import os
import yaml
import wrapt
import inspect
import appdirs
import logging


class ConfigFile(object):
    def __init__(self, config_path, config, appname=None):
        """
        Config file container.
        :param str config_path: path to file for storage. Either absolute
                                 or relative. If relative, appname is required
                                 to determine user config folder for platform
        :param Structure config: top level config item
        :param str appname: When using relative path fon config_file, 
                             appname is required for user config dir
        """
        self.write_enabled = False
        self.config_path = config_path
        # convert passed in config to a registered instance
        self.config = self.register_structure(config)
        conftype = config if config.__class__ is type else config.__class__
        assert isinstance(self.config, conftype)
        log = logging.getLogger("Config")

        if not os.path.isabs(self.config_path):
            if not appname:
                raise ValueError("Must provide appname for relative config file path")
            appdir = appdirs.user_data_dir(appname=appname)
            if not os.path.exists(appdir):
                try:
                    os.makedirs(appdir)
                except:
                    pass
            self.config_path = os.path.join(appdir, self.config_path)

        # Startup
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as configfile:
                saved_config = yaml.load(configfile).__getstate__()
                self.config.__setstate__(saved_config)
                # self.register_structure(config)
                log.info("Loaded config from %s" % self.config_path)

        self.write_enabled = True

        # Ensure the config file exists for new installations.
        if not os.path.exists(self.config_path):
            self.write_yaml()
            log.info("Initialised new config file at %s" % self.config_path)

    def write_yaml(self):
        if self.write_enabled:
            try:
                os.makedirs(os.path.dirname(self.config_path))
            except OSError:
                pass
            with open(self.config_path, 'w') as configfile:
                yaml.dump(self.config, configfile, 
                          default_flow_style=False, Dumper=NoAliasDumper)

    def register_structure(self, structure):
        """
        This will attach this config files' writer to the structure
        :param Structure structure: key to register
        :returns: structure as passed in
        """
        def attach(_structure):
            if inspect.isclass(_structure) and issubclass(_structure, Structure):
                _structure = _structure()
            if isinstance(_structure, Structure):
                _structure.__reg_configfile__(self)

            return _structure

        structure = attach(structure)

        for key, val in structure:
            if isinstance(val, dict):
                for k, v in val.items():
                    val[k] = attach(v)

            elif isinstance(val, (list, set, tuple)):
                val = List((attach(v) for v in val))
                val.__reg_configfile__(self)

            else:
                val = attach(val)
            structure[key] = val

        return structure


class Structure(object):
    def __init__(self, *args, **kwargs):
        """
        Initialise a new structured config object.
        :param args: accepts filename, (optionally) appname to create top level config file
        :param kwargs: default values can be set / overridden for elements
        """
        cls = self.__class__
        self._config_file = None  # type: ConfigFile
        # Set the yaml name of the class
        self._yaml_tag = '!' + cls.__name__

        # Ensure instance has copy of attributes from class
        self.__dict__.update({k:v for k,v in cls.__dict__.items()
                              if not k.startswith('_')})

        self.__dict__.update(kwargs)

        yaml.add_constructor(self._yaml_tag, cls._from_yaml)
        yaml.add_representer(cls, self._to_yaml)
        if args:
            appname = args[1] if len(args) > 1 else None
            ConfigFile(args[0], self, appname)

    @classmethod
    def _from_yaml(cls, loader, node):
        return loader.construct_yaml_object(node, cls)

    def _to_yaml(self, dumper, data):
        return dumper.represent_yaml_object(self._yaml_tag, data, 
                                            self.__class__, flow_style=False)

    def __dir__(self):
        return [k for k in self] + ['__update__', '__as_dict__']

    def __reg_configfile__(self, config_file):
        self._config_file = config_file

    def __iter__(self):
        for key, val in self.__dict__.items():
            yield key, val

    def __contains__(self, item):
        return item in self.__dict__

    def __hasattr__(self, key):
        return key in self.__dict__
        
    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, val, raw=False):
        return self.__setattr__(item, val)

    def __setattr__(self, key, value, raw=False):
        value = value.value if isinstance(value, TypedField) else value
        if not hasattr(self, key):
            changed = True
            super().__setattr__(key, value)
        else:
            try:
                current = self.__dict__[key]
            except KeyError:
                current = self.__getattribute__(key, raw=True)

            if isinstance(current, TypedField):
                current.converter(value)  # Ensure the value is valid
                changed = value != current
                current.value = value
            else:
                changed = not hasattr(self, key) or value != current
                super().__setattr__(key, value)

        # Write out the yaml on each attribute update
        if changed and not key.startswith('_') and getattr(self, '_config_file', None):
            self._config_file.write_yaml()

    def __getattribute__(self, item, raw=False):
        current = object.__getattribute__(self, item)
        if not raw and isinstance(current, TypedField):
            return current.converter(current.value)
        return current

    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        if isinstance(other, Structure):
            other = other.__getstate__()
        return self.__getstate__() == other

    def __getstate__(self):
        return {key: val.value if isinstance(val, TypedField) else val
                for key, val in self.__dict__.items() if not key.startswith('_')}

    def __setstate__(self, state):
        if hasattr(state, '__getstate__'):
            state = state.__getstate__()
        for key, val in state.items():
            current = self[key]
            if inspect.isclass(current) and issubclass(current, Structure):
                self[key] = current = current()
            if hasattr(current, '__setstate__'):
                current.__setstate__(val)
            else:
                self[key] = val

    def to_dict(self):
        import warnings
        warnings.warn('to_dict is deprecated, please use __as_dict__', DeprecationWarning, stacklevel=2)
        return self.__as_dict__()

    def __as_dict__(self):
        def _dict(val):
            if isinstance(val, Structure):
                val = val.__as_dict__()
            elif isinstance(val, List):
                val = [_dict(val) for val in list(val)]
            return val

        return {key: _dict(self[key]) for key, val in self if not key.startswith('_')}
    
    def update(self):
        import warnings
        warnings.warn('update is deprecated, please use __update__', DeprecationWarning, stacklevel=2)
        return self.__as_dict__()

    def __update__(self, data, conf=None):
        conf = self if conf is None else conf
        for key, val in data.items():
            if (not key.startswith('_') and
                        key != '$$hashKey' and
                        key in conf):
                if isinstance(val, dict):
                    self.__update__(val, conf[key])
                elif isinstance(val, list):
                    for idx, lval in enumerate(val):
                        self.__update__(lval, conf[key][idx])
                else:
                    conf[key] = val

class List(list):
    """
    Overridden list to allow us to wrap functions for automatic write.
    This is required as we can't wrap/replace the builtin list functions
    """
    yaml_tag = '!list'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config_file = None  # type: ConfigFile

    def __reg_configfile__(self, config_file):
        self._config_file = config_file
        wrapt.wrap_function_wrapper(self, 'clear', self.write_after)
        wrapt.wrap_function_wrapper(self, 'extend', self.write_after)
        wrapt.wrap_function_wrapper(self, 'pop', self.write_after)
        wrapt.wrap_function_wrapper(self, 'remove', self.write_after)
        wrapt.wrap_function_wrapper(self, 'append', self.write_after)
        wrapt.wrap_function_wrapper(self, 'insert', self.write_after)

    def write_after(self, wrapped, instance, args, kwargs):
        ret = wrapped(*args, **kwargs)
        if self._config_file:
            self._config_file.write_yaml()
        return ret

    def __getstate__(self):
        return list(self)

    def __setstate__(self, state):
        self.clear()
        for elem in state:
            if isinstance(elem, Structure):
                elem.__reg_configfile__(self._config_file)
        self.extend(state)


def list_rep(dumper, data):
    """
    Ensure pyyaml treats our list as a regular list
    """
    return dumper.represent_list(list(data))


yaml.add_representer(List, list_rep)


class NoAliasDumper(yaml.dumper.Dumper):
    """ 
    Disable alias when writing yaml as these make it harder to 
    manually read/modify the config file
    """
    def ignore_aliases(self, data):
        return True


class TypedField(object):
    def __init__(self, value, converter):
        self.value = value
        self.converter = converter

        cls = self.__class__
        self._yaml_tag = '!' + cls.__name__

        yaml.add_constructor(self._yaml_tag, self._from_yaml)

    def __getstate__(self):
        return self.value

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def _from_yaml(cls, loader, node):
        return loader.construct_yaml_object(node, cls)



class IntField(TypedField):
    def __init__(self, value):
        super(IntField, self).__init__(value, int)


class StrField(TypedField):
    def __init__(self, value):
        super(StrField, self).__init__(value, str)


class FloatField(TypedField):
    def __init__(self, value):
        super(FloatField, self).__init__(value, float)


class PathField(TypedField):
    def __init__(self, value):
        try:
            from pathlib import Path
        except ImportError:
            from pathlib2 import Path
        super(PathField, self).__init__(value, Path)
