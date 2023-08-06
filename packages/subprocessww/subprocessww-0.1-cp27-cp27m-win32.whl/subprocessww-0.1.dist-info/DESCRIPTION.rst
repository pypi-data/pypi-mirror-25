Applied the C-patch proposed in https://bugs.python.org/issue1759845 to the most recent (3 October 2017) version of _subprocess.c.

This allows Unicode parameters to be passed to POpen on Python 2.7.

Usage:
------------

.. code:: python


    # Use patched version of subprocess module for Unicode on Windows
    import subprocessww

    # Load the regular POpen, which is now patched
    from subprocess import Popen


2017 The SABnzbd Team <team@sabnzbd.org>


