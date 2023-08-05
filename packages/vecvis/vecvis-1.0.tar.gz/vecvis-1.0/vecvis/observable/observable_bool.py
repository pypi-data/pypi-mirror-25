'''
Created on 25.07.2017

@author: Mo
'''
from vecvis.utils.emitter import Emitter
class ObservableBool(Emitter):
    def __init__(self, initial_value=False):
        super().__init__()
        self._value = initial_value

    def get(self):
        return self._value

    def set(self, value):
        if value != self._value:
            self._value = bool(value)
            self._emit("update", (self, value))
