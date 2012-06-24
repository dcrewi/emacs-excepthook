emacs-excepthook
================

`emacs-excepthook` is a custom python exception hook that sends unhandled exceptions to emacs via emacsclient to be presented in a buffer. Any frame of the call stack can be clicked to open the offending file and line number.


Preparing emacs
---------------

The exception data is sent from python to emacs through emacsclient. Read `man emacsclient` to see how to set up emacs as an edit server. You can use `emacsclient -e '(message "it works")'` to test whether the emacs server is functioning.


Installation via The Packaging System
-------------------------------------

The easiest installation choice is to build a debian package.

    apt-get install debhelper python-support
    dpkg-buildpackage -b
    sudo dpkg -i ../emacs-excepthook_0.1_all.deb


Manual Installation
-------------------

Put `pyexcepthook-handler.el` in your elisp load path. (Or symlink it to the copy in your git repo.) Add  to your `~/.emacs` the line `(autoload 'pyexcepthook-handler "pyexcepthook-handler")`.

Put `emacs_excepthook.py` and `emacs_excepthook.pth` in your python module search path. (Or symlink them to the copy in your git repo.)


Contact
=======

    David Creswick <dmc@gyrae.net>
