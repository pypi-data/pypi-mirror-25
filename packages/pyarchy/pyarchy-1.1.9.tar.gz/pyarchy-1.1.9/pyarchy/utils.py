"""
Container for useful functions.
"""


import copy
import types


def make_deep_copy(object_, n = 1) -> list:
    """
    Return n deepcopies of the object
    """
    assert n > 0
    return [copy.deepcopy(object_) for _ in range(n)]


def raise_type_error(arg_name: str, correct_type: (tuple, list)):
    """
    Raise a template TypeError.
    """
    if isinstance(correct_type, (tuple, list)):
        correct_type = ' or '.join(str(e) for e in correct_type)

    raise TypeError("'%s' must be of type %s" % (
                    arg_name,
                    correct_type))


def raise_key_index_error(key, exists: bool = False):
    """
    Raises key exists/does not exist errors.
    """
    if exists:
        msg = 'key already exists: '
    else:
        msg = 'key does not exist: '

    raise IndexError(msg + str(key))


class StrictArg(object):
    """
    Decorator for any function requiring an argument of a specific type.
    """

    class wrapper(object):
        """
        The wrapper that performs an argument type-check.
        """

        def __init__(self, func: types.FunctionType, arg_names: list,
                     name: str, types_: tuple, inner: tuple):
            object.__init__(self)
            self.__func = func
            self._arg_names = arg_names

            self.__name = name
            self.__types = types_
            self.__inner = inner

        def __call__(self, *args, **kwargs):
            if isinstance(self.__func, type):
                args.insert(0, self.__func)

            for arg, arg_name in zip(args, self._arg_names):
                if arg_name == self.__name:
                    if isinstance(arg, self.__types):
                        return self.__func(*args, **kwargs)
                    else:
                        raise_type_error(self.__name, self.__types)

            if self.__name not in kwargs:
                arg = kwargs[self.__name]

            if not isinstance(arg, self.__types):
                raise_type_error(self.__name, self.__types)
            elif self.__inner \
                and isinstance(arg, (tuple, list)) \
                and any(not isinstance(v, self.__inner) for v in arg):
                    raise_type_error(self.__name, '[%s]' % type(arg))
            elif self.__inner \
                and isinstance(arg, dict) \
                and any(not isinstance(v, self.__inner) for v in arg.values()):
                    raise_type_error(self.__name, '{:%s}' % type(arg))
            else:
                return self.__func(*args, **kwargs)

    def __init__(self, name: str, types_: tuple = (), inner: tuple = ()):
        self._name = name
        self._types = types_
        self._inner = inner

    def __call__(self, func: types.FunctionType) -> object:
        if hasattr(func, '_arg_names'):
            arg_names = func._arg_names
        else:
            code = func.__code__
            arg_names = list(code.co_varnames[:code.co_argcount])

        if self._name not in arg_names:
            raise NameError('missing required argument: ' + self._name)
        else:
            return StrictArg.wrapper(func, arg_names,
                                     self._name, self._types, self._inner)


__all__ = [
    make_deep_copy,
    raise_type_error,
    raise_key_index_error,

    StrictArg,
]
