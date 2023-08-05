Delfick Logging
===============

Some opinionated settings for python logging to allow for structured logging in
your application.

Getting Started
---------------

There are three parts to the setup encouraged by this module:

The standard library
    You are using the standard library to do your logging when you use this
    module

The logging context
    Instead of giving strings to the standard library, you use this context
    object to give dictionaries instead.

The custom handlers
    You use the ``setup_logging`` method to setup global handlers that either go
    to the terminal as key-value pairs, or to syslog as a dictionary.

The most basic example of usage would look something like:

.. code-block:: python

    #!/usr/bin/env python

    from delfick_logging import lc, setup_logging
    import logging

    mylogger = logging.getLogger("mylogger")

    if __name__ == "__main__":
        setup_logging()
        mylogger.info(lc("a message", arg=1, arg2={"more": "options"}, arg3="etc"))

Note that this module uses https://github.com/laysakura/rainbow_logging_handler
to make your console logs colorful.

Installation
------------

Just use pip::

    $ pip install delfick_logging

The logging Context
-------------------

The ``lc`` object is an instance of ``delfick_logging.logContext`` with no initial
context.

You may create new ``lc`` objects with more context by using the ``using``
method.

For example:

.. code-block:: python

    from delfick_logging import lc
    import logging

    log = logging.getLogger("counting")

    lc2 = lc.using(one=1, two=2)

    log.info(lc2("counting is fun", three=2))

Will log out ``counting is fun\tone=1\ttwo=2\tthree=3`` in console mode and
``{"msg": "counting is fun", "one": 1, "two": 2, "three": 3}`` in syslog mode.

When you use this method, you are not modifying the original ``lc`` object, but
instead creating a new immutable copy.

Setting up the logging
----------------------

The ``setup_logging`` method has the following arguments:

log
    The log to add the handler to.

    * If this is a string we do logging.getLogger(log)
    * If this is None, we do logging.getLogger("")
    * Otherwise we use as is

level
    The level we set the logging to. Defaults to logging.INFO

program
    The program name to use when not logging to the console.

syslog_address
tcp_address
udp_address
    If none of these is specified, then we log to the console.

    Otherwise we use the address to converse with a remote server.

    tcp_address and udp_address Must be of the form "{host}:{port}".
    i.e. "localhost:9001"

    syslog_address may either be a filename or of the form "{host}:{port}"

    Only one will be used.

    If syslog is specified that is used, otherwise if udp is specified that is used,
    otherwise tcp.

only_message
    Whether to only print out the message when going to the console. Defaults to
    False

logging_handler_file
    The file to go to when going to the console. Defaults to stderr

Different theme
---------------

The ``setup_logging`` function returns a ``handler``, which you may pass into the
``delfick_logging.setup_logging_theme`` function to change the colours for INFO
level messages:

.. code-block:: python

    from delfick_logging import setup_logging, setup_logging_theme

    handler = setup_logging()
    setup_logging_theme(handler, colors="dark")

There are currently two options: "light", which is default; and "dark".
