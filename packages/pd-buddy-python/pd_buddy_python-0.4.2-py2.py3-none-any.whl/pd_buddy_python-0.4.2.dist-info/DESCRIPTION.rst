pd-buddy-python
===============

Python library for working with the PD Buddy Sink Serial Console
Configuration Interface

Features
--------

-  Provides a Pythonic interface to the PD Buddy Sink shell commands
-  Configuration is represented as a SinkConfig object
-  SinkConfig objects can be manipulated locally and written to the
   device with one method call
-  Allows control of whether or not the output is enabled
-  Provides a Pythonic interface for reading advertised PDOs

Examples
--------

Open the first PD Buddy Sink device and read its configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import pdbuddy
    >>> pdbs = pdbuddy.Sink(list(pdbuddy.Sink.get_devices())[0])
    >>> pdbs.get_cfg()
    SinkConfig(status=<SinkStatus.VALID: 2>, flags=<SinkFlags.NONE: 0>, v=5000, i=3000)
    >>> print(pdbs.get_cfg())
    status: valid
    flags: (none)
    v: 5.00 V
    i: 3.00 A

Locally manipulate a SinkConfig object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> cfg = pdbs.get_cfg()
    >>> cfg = cfg._replace(v=20000, i=2250)
    >>> cfg = cfg._replace(flags=cfg.flags | pdbuddy.SinkFlags.GIVEBACK)
    >>> cfg
    SinkConfig(status=<SinkStatus.VALID: 2>, flags=<SinkFlags.GIVEBACK: 1>, v=20000, i=2250)

Write the SinkConfig object to flash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> pdbs.set_tmpcfg(cfg)
    >>> pdbs.write()
    >>> pdbs.get_cfg()
    SinkConfig(status=<SinkStatus.VALID: 2>, flags=<SinkFlags.GIVEBACK: 1>, v=20000, i=2250)

Requirements
------------

-  Python 2.7, >= 3.3
-  pySerial >= 3.0
-  aenum >= 2.0 (if using Python < 3.6)

Testing
-------

To run the unit tests, run::

    $ python setup.py test

This will test the Sink class only if a PD Buddy Sink is plugged in and in
setup mode, so make sure that's the case if you're testing any changes to the
Sink class.  Also, make sure the Status LED is blinking quickly when the tests
are run, since that's the only real way to test the ``identify`` command.  Be
aware that the Sink's configuration will get clobbered by the tests.


