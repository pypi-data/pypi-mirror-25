from vecvis.utils.emitter import Emitter

class ObservableSet(Emitter):
    def __init__(self):
        super().__init__()
        self._set = set()

    def get(self):
        """ Get the curent value
        """
        return self._set

    def set(self, new_set):
        old_set = self._set
        self._set = new_set
        self._emit("set_changed", (self, old_set, new_set))

    def add(self, items):
        """ Sets a new value
        """
        new_items = items - self._set
        if new_items:
            self._set |= new_items
            self._emit("items_added", (self, new_items))

    def remove(self, items):
        remove_items = items & self._set
        if remove_items:
            self._set -= remove_items
            self._emit("items_removed", (self, remove_items))
