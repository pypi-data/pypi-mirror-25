Overview
========



Ever wanted to load plain ``.ini`` config files and then validate loaded config?

Ever wanted to load config from multiple locations (``/etc/appconfig.conf``, ``~/.appconfig.conf``) into single object and then validate that?

Worry no more!

Python's `ConfigParser`_ met `marshmallow`_ and now they get along just fine - without any JSON in sight to spoil the fun.


Installation
============

::

    pip install marshmallow_configparser


Example
=======

Having config file ``/tmp/example_config.conf`` looking like this:

.. code-block:: ini

    [Section1]
    option1 = mandatory string
    option2 = optional string
    option3 = 42
    option4 = 24

    [Section2]
    option1 = mandatory string
    option2 = optional string
    option3 = 42
    option4 = 24

And wanting to load it into our config object:

.. code-block:: python

    class ConfigObject(object):
        MANDATORY_STRING1 = None
        OPTIONAL_STRING1 = None
        MANDATORY_INTEGER1 = None
        OPTIONAL_INTEGER1 = None
        MANDATORY_STRING2 = None
        OPTIONAL_STRING2 = None
        MANDATORY_INTEGER2 = None
        OPTIONAL_INTEGER2 = None


We can define `marshmallow`_ schema:

.. code-block:: python

    from marshmallow.validate import Range

    from marshmallow_configparser import (ConfigBoolean, ConfigInteger,
                                          ConfigParserSchema, ConfigString,
                                          IsNotBlank)

    class ConfigSchema(ConfigParserSchema):
        class Meta:
            model = ConfigObject

        MANDATORY_STRING1 = ConfigString(
            section='Section1', load_from='option1', dump_to='option1',
            validate=[IsNotBlank()]
        )
        OPTIONAL_STRING1 = ConfigString(
            section='Section1', load_from='option2', dump_to='option2',
        )
        MANDATORY_INTEGER1 = ConfigInteger(
            section='Section1', load_from='option3', dump_to='option3',
            validate=[Range(min=24, max=42)]
        )
        OPTIONAL_INTEGER1 = ConfigInteger(
            section='Section1', load_from='option4', dump_to='option4',
        )

        MANDATORY_STRING2 = ConfigString(
            section='Section2', load_from='option1', dump_to='option1',
            validate=[IsNotBlank()]
        )
        OPTIONAL_STRING2 = ConfigString(
            section='Section2', load_from='option2', dump_to='option2',
        )
        MANDATORY_INTEGER2 = ConfigInteger(
            section='Section2', load_from='option3', dump_to='option3',
            validate=[Range(min=24, max=42)]
        )
        OPTIONAL_INTEGER2 = ConfigInteger(
            section='Section2', load_from='option4', dump_to='option4',
        )


Which can then load and validate our config:

.. code-block:: python

    schema = ConfigSchema()
    obj, errors = schema.load(['/tmp/example_config.conf'])

In the end we have:

.. code-block:: python

    obj.__dict_

    {'MANDATORY_INTEGER1': 42,
     'MANDATORY_INTEGER2': 42,
     'MANDATORY_STRING1': 'mandatory string',
     'MANDATORY_STRING2': 'mandatory string',
     'OPTIONAL_INTEGER1': 24,
     'OPTIONAL_INTEGER2': 24,
     'OPTIONAL_STRING1': 'optional string',
     'OPTIONAL_STRING2': 'optional string'}

Instead of using convenience classes like ``ConfigString``, there are also
classes in ``marshmallow_configparser.fields`` module that expose full `marshmallow`_ API. Check the docs for details.

Documentation
=============

http://marshmallow-configparser.readthedocs.io/en/latest/index.html


.. _marshmallow: https://github.com/marshmallow-code/marshmallow
.. _ConfigParser: https://docs.python.org/3/library/configparser.html#configparser.ConfigParser

Changelog
=========

0.3.3 (2017-09-20)
------------------
* Added attribute to Schema that gives access to underlying config data


0.3.2 (2017-08-07)
------------------
* docs cleanup


0.3.1 (2017-08-07)
------------------
* repo cleanup


0.3.0 (2017-05-08)
------------------

* config validation now fails if there is no config files to read from or they are not readable.


0.2.0 (2017-05-02)
------------------

* Added convenience_fields module


0.1.0 (2017-04-30)
------------------

* First release on PyPI.


