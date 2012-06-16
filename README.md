emacs-excepthook
================

`emacs-excepthook` is a custom python exception hook that sends unhandled exceptions to emacs via emacsclient to be presented in a buffer. Any frame of the call stack can be clicked to open the offending file and line number.

Installation
------------

1. The exception data is sent from python to emacs through emacsclient. Read `man emacsclient` to see how to set up emacs as an edit server. You can use `emacsclient -e '(message "it works")'` to test whether the emacs server is functioning.

2. Put `pyexcepthook-handler.el` in your elisp load path. (Or symlink it to the copy in your git repo.) Add  to your `~/.emacs` the line `(load "pyexcepthook-handler")`.

3. Put `emacs_excepthook.py` in your python module search path. (Or symlink it to the copy in your git repo.) If it does not exist, create the file `usercustomize.py` in your python module search path. Add to it the two lines `import emacs_excepthook` and `emacs_excepthook.install()`.
