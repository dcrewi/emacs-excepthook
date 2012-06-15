# Copyright (c) 2012 David Creswick
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import subprocess
import traceback

shadowedHook = None

def install():
    'Install the excepthook.'
    global shadowedHook
    assert shadowedHook is None
    shadowedHook = sys.excepthook
    sys.excepthook = excepthook_impl

def uninstall():
    'Uninstall the execepthook and restore the previous excepthook.'
    global shadowedHook
    assert shadowedHook is not None
    sys.excepthook = shadowedHook
    shadowedHook = None

class Symbol:
    '''Simple class used to distinguish symbols from strings.
    '''

    def __init__(self, sym):
        self.sym = sym

def elispSexpr(items):
    strs = []
    _elispSexpr(items, strs)
    return ''.join(strs)

def _elispSexpr(items, strs):
    strs.append('(')
    firstItem = True
    for item in items:
       if firstItem:
           firstItem = False
       else:
           strs.append(' ')
       if item is None:
           strs.append('nil')
       elif isinstance(item, Symbol):
           strs.append(item.sym)
       elif isinstance(item, int):
           strs.append(str(item));
       elif isinstance(item, list) or isinstance(item, tuple):
           _elispSexpr(item, strs)
       elif isinstance(item, str): # FIXME: someone will probably want to properly handle unicode strings someday
           strs.append('"')
           for c in item:
               n = ord(c)
               if n < 127 and n >= 32: # printable characters
                   strs.append(c)
               else: # unprintable character
                   strs.append('\\')
                   strs.append(oct(n))
           strs.append('"')
       else:
           raise TypeError('unable to handle type '+item.__class__.__name__)
    strs.append(')')

def excepthook_impl(type, value, tb):
    shadowedHook(type, value, tb)
    s = [Symbol('pyexcepthook-handler'),
         type.__name__,
         str(value),
         [Symbol('list')] + \
         [[Symbol('list'), filename, line_no, fnc_name, line]
          for (filename, line_no, fnc_name, line) in traceback.extract_tb(tb)]]
    subprocess.call(['emacsclient', '-e', elispSexpr(s)])
