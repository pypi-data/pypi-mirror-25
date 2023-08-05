"""
"""
from vecvis.utils.emitter import Emitter


class ObservableFloat(Emitter):
    """ Class to manage a Number.
    Can inform Observers about a change
    """
    def __init__(self, value):
        super().__init__()
        self._value = value

    def get(self):
        """ Get the curent value
        """
        return self._value

    def set(self, value):
        """ Sets a new value
        """
        value = float(value)
        if value != self._value:
            old_value = self._value
            self._value = value
            self._emit("update", (self,old_value, value))

    """ Reverse add self + other """
    def __radd__(self, other):
        return self.get() + other.get()

    def __add__(self, other):
        return self.get() + other.get()

class ObservableInt(Emitter):
    """ Class to manage a Number.
    Can inform Observers about a change
    """
    def __init__(self, value):
        super().__init__()
        self._value = int(value)

    def get(self):
        """ Get the curent value
        """
        return self._value

    def set(self, value):
        """ Sets a new value
        """
        value = int(value)
        if value != self._value:
            old_value = self._value
            self._value = value
            self._emit("update", (self,old_value, value))

    """ Reverse add self + other """
    def __radd__(self, other):
        return self.get() + other.get()

    def __add__(self, other):
        return self.get() + other.get()
