Structured Config
=================

A configuration module for python where the config structure is solely
defined in python.

There are lots of different modules and formats available for creating
configuration files in a python project.

All of the ones I've used in the past have one main limitations in common however;
the primary definition of the configuration elements it either not written in python,
or it's written in something like a python dict where you don't get particularly
good static inspection of elements.

I personally like to do my python development in a smart ide like pycharm where
I can take full advantage of inspection and auto-completion. If you config is
not written in python however, I don't get to do this.

If you want any kind of introspection of config files, you end up having some
kind of python parser of the config file with all the configuration elements
repeated in both the default template and in some kind of mirror class.

This module aims to remove this limitation.

Basic Usage
-----------

Now, your config.py file in your project can be something like ::

    from structured_config import ConfigFile, Structure

    class Config(Structure):

        class server(Structure):
            url = 'https:www.example.com'
            username = '<user>'
            password = '<password>'


        # Max number of tcp connections at any one time
        concurrent_connections =  32

        # Local service port
        service_port = 45080


    config = Config('/path/to/config.yaml')

Any other modules in your project can then simply ::

    from config import config

    import requests
    from requests.auth import HTTPBasicAuth

    r = requests.get(config.server.url, auth=HTTPBasicAuth(config.server.username, config.server.password))

and so on. Your IDE should give you full autocomplete on all these elements, becuase as far as it knows your config is
a normal class with normal static attributes.

If you want to change these config items in code it's as simple as setting the attribute ::

    from config import config

    config.concurrent_connections = 64

That's it. The config is written to disk in the yaml file pointed to in Config() instantiation

The yaml file can be manually changed on disk of course. At this stage it'll require
a restart of the app to reload the file however ::

    !config
    server: !server
      password: <password>
      url: https:www.example.com
      username: <user>
    concurrent_connections: 32
    service_port: 45080

Lists of elements
-----------------

If you want a slightly more complex config file with a list of elements, this can be handled too ::

    import structured_config
    from structured_config import Structure, ConfigFile

    # Pre-define the object we want to store a list of.
    class Map(Structure):
        remote_path = None
        local_path = None


    # Default configuration for the application
    class Config(Structure):

        class server(Structure):
            url = 'https:www.example.com'
            username = '<user>'
            password = '<password>'

        mapping = [
            Map(
                remote_path="/test/",
                local_path="~/test/"
            ),
            Map(
                remote_path="/one/",
                local_path="~/two/"
            ),
            Map(
                remote_path="/two/",
                local_path="~/one/"
            )
        ]

    config = Config('config.yaml')

Your main code can access the Map items in the list by all the normal means.
if you append() new ones onto the list or pop() old ones off the list, the
config will automatically write them to disk. Same goes for editing either of the
attributes in any of the Map objects that have been added to the list.

Format convertions
------------------

If you want to enforce the type of some attributes, we've got that covered as well ::

    from structured_config import ConfigFile, Structure, TypedField, IntField

    class config(Structure):

        concurrent_connections = IntField(32)

        path = TypedField('$HOME', os.path.expandvars)


    config = Config('config.yaml')

Currently available TypeFields include:
 * IntField : converts to int()
 * FloatField : converts to float()
 * StrField : converts to str()
 * PathField : converts to pathlib.Path()

Others can be created on demand by using `TypeField(value, converter_funtion)` 
or by subclassing TypeField as per the ones above.

Any time a config attribute is set, it will be passed through the validation
function first. The raw (unconverted) value will be saved to disk.

Get's on the config objects attribute return the converted value, not the Field object.

Config file location
--------------------

When instantiating your Config object, the yaml filename needs to be passed in.  

If an absolute path is provided this will be used verbatim. 

A relative path is assumed to be stored in the standard system location for config 
files, as handled by `appdirs <https://pypi.python.org/pypi/appdirs/1.4.3>`_.

In this case the projects appname should be provided as well to create the folder
 the config file will be stored in ::

    config = Config('config.yaml', 'ExampleApp')


