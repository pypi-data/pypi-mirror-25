from vecvis.utils.emitter import Emitter

class ObservableString(Emitter):
    def __init__(self, value):
        super().__init__()
        self._value = str(value)

    def get(self):
        """ Get the curent value
        """
        return self._value

    def set(self, value):
        """ Sets a new value
        """
        value = str(value)
        if value != self._value:
            old_value = self._value
            self._value = value
            self._emit("update", (self,old_value, value))
