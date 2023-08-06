import sys
import re
import inspect
from distutils.core import Command
from scriptine import log
from wrapt import decorator

class DistutilsCommand(Command):
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass

def dict_to_options(d):
    d = Options(d)
    for k, v in d.iteritems():
        if isinstance(v, dict):
            d[k] = dict_to_options(v)
    return d

class Options(dict):
    """
    Dictionary with attribute style access.
    
    >>> o = Options(bar='foo')
    >>> o.bar
    'foo'
    """
    def __repr__(self):
        args = ', '.join(['%s=%r' % (key, value) for key, value in
            self.iteritems()])
        return '%s(%s)' % (self.__class__.__name__, args)
    
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError(name)
    
    __setattr__ = dict.__setitem__
    
    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError(name)

options = Options()
options.dry = False


def dry(message, func, *args, **kw):
    log.info(message)
    
    if not options.dry:
        return func(*args, **kw)

@decorator
def log_call(func, instance, args, kw):
    _log_function_call(func, *args, **kw)
    return func(*args, **kw)

def _log_function_call(func, *args, **kw):
    message = func.__name__
    if args:
        message += ' ' + ' '.join(map(str, args))
    if kw:
        # for python2 iteritems would be better, however items() works everywhere and is reasonably well for python2
        kw_str = ' '.join(['%s %r' % (k, v) for k, v in kw.items()])
        message += '(' + kw_str + ')'
    log.info(message)

@decorator
def dry_guard(func, instance, args, kw):
    _log_function_call(func, *args, **kw)
    if not options.dry:
        return func(*args, **kw)
