"""
Container for pseudo-mechanical Object types.
"""


from .core import Object
from .utils import raise_type_error


class StateObject(Object):

    state_types = (type(None),)

    def __init__(self, default=None):
        Object.__init__(self)
        self.state = default

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.state)

    @property
    def state(self):
        """
        Any object, typically an integer or boolean, representing a state.
        """
        return self.__state

    @state.setter
    def state(self, state):
        if not isinstance(state, self.state_types):
            raise_type_error(
                'state',
                ' or '.join(str(t) for t in self.state_types))
        else:
            self.__state = state


class BinarySwitch(StateObject):
    """
    A switch that is either on or off.
    """

    state_types = (bool,)

    def __init__(self):
        StateObject.__init__(self, False)

    def toggle(self):
        """
        Switch to the opposite state.
        """
        self.state = not self.state


class TrinarySwitch(StateObject):
    """
    A switch that is either positive, negative, or off.
    """

    state_types = (type(None), bool)

    def __init__(self):
        StateObject.__init__(self, None)

    def switch(self):
        """
        Switch the function from positive to negative, or remain off.
        """
        if self.state is None:
            pass
        else:
            self.state = not self.state


class RotarySwitch(StateObject):
    """
    A switch that can have any number of states.
    """

    state_types = (int,)

    def __init__(self, num_positions=0, wrapping=False):
        assert num_positions >= 0

        self.__range = range(0, num_positions + 1) or [0]
        self.__wrapping = wrapping

        StateObject.__init__(self, 0)

    @property
    def wrapping(self):
        """
        A boolean representing whether the switch can be turned infinitely.
        """
        return self.__wrapping

    @property
    def state(self):
        return StateObject.state.fget(self)

    @state.setter
    def state(self, state):
        if self.wrapping and state not in self.__range:
            if state > self.__range[-1]:
                state = self.__range[0]
            else:
                state = self.__range[-1]

        StateObject.state.fset(self, state)


__all__ = [
    StateObject,
    BinarySwitch,
    TrinarySwitch,
    RotarySwitch,
]
