from typing import *
from enum import Enum
from cs103 import Image
import os
import sys
import traceback
import inspect

class TypecheckError(TypeError):
    def __init__(self, val, a, b, fn):
        self.fn = fn
        return super().__init__('\x1b[32m%s\x1b[0m is %s, not %s'%(val,pretype(a),pretype(b)))
    def _render_traceback_(self):
        print('\x1b[31m')
        print('-'*75)
        print(type(self).__name__)
        print('\n' + str(self) + '\n')
        print(traceback.format_tb(sys.exc_info()[2])[1])
        print('as expected in\n\x1b[34m')
        print(''.join(['  ' + x for x in inspect.getsourcelines(self.fn)[0]]))
        print('\x1b[0m')

class ReturnError(TypecheckError):
    def __init__(self, te):
        self.te = te
        return None
    def _render_traceback_(self):
        print('\x1b[31m')
        print('-'*75)
        print(type(self).__name__)
        print('\nreturned value ' + str(self.te) + ' as expected in\n\x1b[34m')
        print(''.join(['  ' + x for x in inspect.getsourcelines(self.te.fn)[0]]))
        print('\x1b[0m')

def pretype(s: str) -> str:
    pre = 'a'
    if s[0].lower() in ['a', 'e', 'i', 'o']:
        pre = 'an'
    return pre + ' \x1b[36m%s\x1b[0m'%s

def ustr(t: Union) -> str:
    try:
        params = t.__union_params__
    except AttributeError:
        params = t.__args__

    if len(params) == 2 and params[1] is type(None):
        return 'Optional[%s]'%params[0].__name__
    return 'Union[' + ', '.join([x.__name__ for x in params]) + ']'

def astr(t: any) -> str:
    try:
        if issubclass(t, Image):
            return 'Image'
        else:
            return t.__name__
    except:
        return t.__name__

def subtype(va: any, tb: any, fn: any = None, strict: bool = False) -> bool:
    ta = type(va)
    name = astr(ta)

    if tb == None:
        if va != None:
            raise TypeError("The return type of the function is None, but it returned " + str(va))
        else:
            return True

    if hasattr(tb, '__name__') and tb.__name__ == "cs103.image":
        raise TypeError("The return type of the function is \x1b[36mimage\x1b[0m; did you mean \x1b[36mImage\x1b[0m?")
    
    if type(tb) is type(Union):
        if sys.version_info >= (3,6):
            if not (ta == tb or any(subtype(va,t,fn) for t in tb.__args__)):
                raise TypecheckError(va,name,ustr(tb),fn)
        else:
            if not (ta == tb or any(subtype(va,t,fn) for t in tb.__union_params__)):
                raise TypecheckError(va,name,ustr(tb),fn)
    elif issubclass(tb, List):
        if ta is not list:
            raise TypecheckError(va,name,tb.__name__, fn)
        all(subtype(v, tb.__args__[0], fn, True) for v in va)
    elif tb is float:
        rv = ta is int or ta is float
        if strict and not rv:
            raise TypecheckError(va,name,tb.__name__, fn)
        return rv
    elif ta is bool and tb is int:
        if strict:
            raise TypecheckError(va,name,tb.__name__, fn)
        return False
    elif not issubclass(ta, tb):
        if strict:
            raise TypecheckError(va,name,tb.__name__, fn)
        return False
        
    return True

def typecheck(fn):
    def wrapper(*args):
        types = get_type_hints(fn)
        for name, val in zip(fn.__code__.co_varnames, args):
            subtype(val, types[name], fn, True)

        retval = fn(*args)
        try:
            subtype(retval, types['return'], fn, True)
        except TypecheckError as e:
            raise ReturnError(e)

        return retval
    return wrapper

__all__ = ['subtype', 'typecheck']
