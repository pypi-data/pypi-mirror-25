flapjack_stack
==============

This provides a simple way to handle settings in a multi-layer fashion, which
allows you to composing settings by add in different configuration components.
It will read from files, objects, and environment variables.

Example Usage::

    from flapjack_stack import FlapjackStack
    settings = FlapjackStack()
    settings.add_layer_from_file('/path/to/our_file')
    settings.add_layer(thing)
    settings.add_layer_from_env()

Which will create a new FlapjackStack instance, then read settings in from
a file, then the thing object and finally from the environment. This would
result in a group of settings like:

===== ======
Layer Source
===== ======
3     loaded from env
2     loaded from thing object
1     loaded from '/path/to/our_file'
Base  Empty created during init
===== ======

And settings would be returned from the top to the bottom.  For example if we
had a setting called COOKIES in both the thing object and our_file, the one from
the thing object would be returned.

**NOTE**
``add_layer_from_env()`` only searchs for environment variables already in the
settings object regardless of their layer that are prefixed with an ``FJS_`` at
the moment it is called.  So if you add the variable later, it will not be seen.


