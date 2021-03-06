# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.36
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

"""
This module provides a function for accelerating the convergence of
series based on the Levin u-transform.  This method takes a small
number of terms from the start of a series and uses a systematic
approximation to compute an extrapolated value and an estimate of its
error. The u-transform works for both convergent and divergent
series, including asymptotic series.
"""

import _sum
import new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


def levin_sum(a, truncate=False, info_dict=None):
    """Return (sum(a), err) where sum(a) is the extrapolated
    sum of the infinite series a and err is an error estimate.

    Uses the Levin u-transform method.

    Parameters:
      a : A list or array of floating point numbers assumed
          to be the first terms in a series.
      truncate: If True, then use a more efficient algorithm, but with
          a less accurate error estimate
      info_dict: If info_dict is provided, then two entries will
          be added: 'terms_used' will be the number of terms
          used and 'sum_plain' will be the sum of these terms
          without acceleration.

    Notes: The error estimate is made assuming that the terms a are
    computed to machined precision.

    Example: Computing the zeta function 
    zeta(2) = 1/1**2 + 1/2**2 + 1/3**2 + ... = pi**2/6

    >>> from math import pi
    >>> zeta_2 = pi**2/6
    >>> a = [1.0/n**2 for n in range(1,21)]
    >>> info_dict = {}
    >>> (ans, err_est) = levin_sum(a, info_dict=info_dict)
    >>> ans, zeta_2             # doctest: +ELLIPSIS
    1.644934066..., 1.644934066...
    >>> err = abs(ans - zeta_2)
    >>> err < err_est
    True
    >>> (ans, err_est) = levin_sum(a, truncate=False)
    >>> ans             # doctest: +ELLIPSIS
    1.644934066...
    """
    if truncate:
        l = _levin_utrunc(len(a))
    else:
        l = _levin(len(a))

    ans = l.accel(a)
    if info_dict is not None:
        info_dict['sum_plain'] = l.sum_plain()
        info_dict['terms_used'] = l.get_terms_used()
    del l
    return ans

class _levin(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, _levin, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, _levin, name)
    __repr__ = _swig_repr
    def __init__(self, *args, **kwargs): 
        this = _sum.new__levin(*args, **kwargs)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _sum.delete__levin
    __del__ = lambda self : None;
    def accel(*args, **kwargs): return _sum._levin_accel(*args, **kwargs)
    def get_terms_used(*args, **kwargs): return _sum._levin_get_terms_used(*args, **kwargs)
    def sum_plain(*args, **kwargs): return _sum._levin_sum_plain(*args, **kwargs)
    def minmax(*args, **kwargs): return _sum._levin_minmax(*args, **kwargs)
_levin_swigregister = _sum._levin_swigregister
_levin_swigregister(_levin)

class _levin_utrunc(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, _levin_utrunc, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, _levin_utrunc, name)
    __repr__ = _swig_repr
    def __init__(self, *args, **kwargs): 
        this = _sum.new__levin_utrunc(*args, **kwargs)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _sum.delete__levin_utrunc
    __del__ = lambda self : None;
    def accel(*args, **kwargs): return _sum._levin_utrunc_accel(*args, **kwargs)
    def get_terms_used(*args, **kwargs): return _sum._levin_utrunc_get_terms_used(*args, **kwargs)
    def sum_plain(*args, **kwargs): return _sum._levin_utrunc_sum_plain(*args, **kwargs)
    def minmax(*args, **kwargs): return _sum._levin_utrunc_minmax(*args, **kwargs)
_levin_utrunc_swigregister = _sum._levin_utrunc_swigregister
_levin_utrunc_swigregister(_levin_utrunc)



