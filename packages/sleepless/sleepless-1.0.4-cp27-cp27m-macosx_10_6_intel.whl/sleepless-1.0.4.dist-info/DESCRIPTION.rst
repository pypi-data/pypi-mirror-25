sleepless
------------

Python wrapper around the macOS (OSX) assertion for preventing standby "due to lack of user action".

Usage:
------------

.. code:: python

    import sleepless

    # Tell OS to keep awake
    sleepless.keep_awake(u"MyApp - why I don't sleep")

    # Do stuff
    do_lengthy_action()

    # Calling again is harmless
    sleepless.keep_awake(u"MyApp - why I don't sleep")

    # When done
    sleepless.allow_sleep()


2012 The SABnzbd Team <team@sabnzbd.org>


