"""
Container for metaclasses.
"""


import types


class MetaNamedObject(type):
    """
    A metaclass for any object whose name can be set at the class level.
    """

    _name = None
    name = property(lambda cls: cls._name)


class MetaSingleton(MetaNamedObject):
    """
    A metaclass for any class that should make only one instance.
    """

    __instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(MetaSingleton, cls).__call__(*args, **kwargs)

        return cls.__instance


class MetaConditional(MetaNamedObject):
    """
    A metaclass for any object that requires that a function returns True to
    call its functions.

    Note: MetaConditional is a subclass of MetaNamedObject only to pacify the
    metaclass conflict we get in the Event class.
    """

    @classmethod
    def status_checker(cls, func: types.FunctionType):
        """
        A decorator for functions that require the status attribute to be
        True for the function to be executed.
        """
        def func_wrapper(self, *args, **kwargs):
            if self.__condition():
                return func(self, *args, **kwargs)
            else:
                return None

        return func_wrapper

    def __new__(cls, name, bases, attrs):
        """
        Decorate all public methods with the status_checker function.
        """

        for k, v in attrs.items():
            if k == '_condition':
                if isinstance(v, (property, types.FunctionType)):
                    condition_func = v
                else:
                    condition_func = lambda self: bool(v)
            elif not k.startswith('__') and isinstance(v, types.FunctionType):
                attrs[k] = cls.status_checker(v)
            else:
                continue

        if '_condition' in attrs:
            func = attrs['_condition']
            if callable(func):
                del attrs['_condition']
        else:
            for base in bases:
                func = base.__dict__.get('_MetaConditional__condition')
                if func:
                    condition_func = func
                    break

        try:
            attrs['_MetaConditional__condition'] = condition_func
        except NameError:
            raise AttributeError('expected %s._condition' % name)

        return type.__new__(cls, name, bases, attrs)


__all__ = [
    MetaNamedObject,
    MetaSingleton,
    MetaConditional,
]
