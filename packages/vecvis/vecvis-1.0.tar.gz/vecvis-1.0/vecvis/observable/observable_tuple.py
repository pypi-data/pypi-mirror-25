""" doc
"""
from vecvis.utils.emitter import Emitter

class ObservableTuple(Emitter):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def get(self):
        return self._value

    def set(self, value):
        if self._value != value:
            old_value = self._value
            self._value = value
            self._emit("update", (self, old_value, value))
