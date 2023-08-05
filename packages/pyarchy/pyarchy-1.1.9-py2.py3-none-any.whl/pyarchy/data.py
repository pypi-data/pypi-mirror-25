"""
A container for custom data containers.
"""


import types

from .utils import make_deep_copy, raise_key_index_error, StrictArg


class HardKeySet(object):
    """
    A set of key-value pairs that allows mutable objects to be keys. They are
    copied on addition to the set, and will remain unchanged.
    """

    def __init__(self):
        object.__init__(self)
        self.__items = {}

    def __contains__(self, key):
        return id(key) in self.__items

    def __getitem__(self, key):
        for id_, (k, v) in self.__items.items():
            if id_ == id(key):
                return make_deep_copy(v)
        else:
            raise_key_index_error(key)

    def __setitem__(self, key, value):
        if id(key) in self.__items.keys():
            raise KeyError('keys can only be set once')
        else:
            self.__items[id(key)] = (
                make_deep_copy(key),
                make_deep_copy(value),
            )

    def __delitem__(self, key):
        for id_, (k, v) in self.__items.items():
            if id_ == id(key):
                raise KeyError('keys cannot be removed')
        else:
            raise_key_index_error(key)

    def __iter__(self):
        for id_, (k, v) in self.__items.items():
            yield (k, v)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.__class__.__name__ + '([%i])' % len(self.__items)

    def get(self, key):
        return self.__getitem__(key, value)

    def add(self, key, value):
        self.__setitem__(key, value)
        return (key, value)

    def remove(self, key):
        self.__delitem__(key)

    def update(self, key, value):
        self.__setitem__(key, value)
        return (key, value)


class ItemPool(object):
    """
    A hybrid container object.
    """

    object_type = object

    def __init__(self, *objs):
        self.readonly = False
        self.protected = False
        self.__objects = set(o for o in objs if isinstance(e, self.object_type))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.__class__.__name__ + '[%i]' % len(self)

    def __iter__(self):
        """
        A list of the objects in the pool. Can be overridden by subclasses.
        """
        return iter(list(self.__objects))

    def __reversed__(self):
        """
        A list of the objects in the pool, in reverse.
        """
        return self[::-1]

    def __getitem__(self, idx):
        return list(self)[idx]

    def __len__(self):
        return len(self.__objects)

    def create(self, *args, **kwargs) -> object:
        """
        Base function for creating new objects in the pool.
        """
        obj = self.object_type(*args, **kwargs)
        self.add(obj)
        return obj

    @property
    def protected(self):
        """
        A boolean representing whether Objects in the pool can be modified.
        """
        return self.__protected

    @protected.setter
    @StrictArg('mode', bool)
    def protected(self, mode: bool):
        self.__protected = mode

    def protect_objects(func):
        """
        A decorator for functions that require the instance have the ability
        to modify objects in the pool.
        """
        def wrapper(self, *args, **kwargs):
            if self.protected:
                raise UserWarning('cannot modify pool elements')
            else:
                return func(self, *args, **kwargs)

        return wrapper

    @property
    def readonly(self):
        """
        A boolean representing whether the pool itself can be modified.
        """
        return self.__readonly

    @readonly.setter
    @StrictArg('mode', bool)
    def readonly(self, mode):
        self.__readonly = mode

    def protect_pool(func):
        """
        A decorator for functions that require the instance be mutable.
        """
        def wrapper(self, *args, **kwargs):
            if self.readonly:
                raise UserWarning('cannot modify pool')
            else:
                return func(self, *args, **kwargs)

        return wrapper

    @protect_objects
    @StrictArg('func', types.FunctionType)
    def map(self, func: types.FunctionType):
        """
        Apply a function to all objects in the pool.
        """
        if not isinstance(func, types.FunctionType):
            raise_type_error('func', types.FunctionType)
        else:
            for o in self:
                func(o)

    @StrictArg('func', types.FunctionType)
    def get(self, func: types.FunctionType):
        """
        Return the first item for which the supplied function returns True.
        A KeyError is raised if no item matches.
        """
        for o in self:
            if func(o):
                return o

        raise KeyError('no matching object found')

    @StrictArg('func', types.FunctionType)
    def filter(self, func: types.FunctionType):
        """
        Return a subset of the pool where only an object, o, where func(o) is
        True is included.
        """
        return type(self)(*filter(func, self))

    @protect_objects
    def add(self, obj: object):
        """
        Add the provided object to the pool.
        """
        if not isinstance(obj, self.object_type):
            raise_type_error('obj', self.object_type)
        else:
            self.__objects.add(obj)

    @protect_pool
    def update(self, *pools):
        """
        Add to the pool all objects in the provided pool.
        """
        if self.strict and any(not isinstance(p, self.__class__) for p in pools):
            raise TypeError('pools must be of same type')
        else:
            self.__objects.update(*(pool.objects for pool in pools))

    def remove(self, obj: object):
        """
        Remove the provided object from the pool.
        """
        if not isinstance(obj, self.object_type):
            raise_type_error('obj', self.object_type)
        else:
            self.__objects.remove(obj)

    @protect_pool
    def disjoint(self, pool):
        """
        Remove from the pool any objects that are also in the provided pool.
        """
        self.__objects.difference_update(pool)

    @protect_pool
    def clear(self, func: types.FunctionType = None):
        """
        Remove all objects from the pool. If a function is provided, only an
        object, o, where func(o) is True will be removed from the pool.
        """
        if callable(func):
            for obj in self.filter(func):
                self.remove(obj)
        else:
            self.__objects.clear()

    @protect_pool
    def pop(self):
        """
        Remove and return an object from the pool.
        """
        if len(self) > 0:
            obj = self[-1]
            self.remove(obj)
            return obj
        else:
            raise IndexError("can't pop from empty pool")


__all__ = [
    HardKeySet,
    ItemPool,
]
