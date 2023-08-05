""" doc
"""
from vecvis.utils.emitter import Emitter
from vecvis.utils.utils import add_items, remove_from_list


class ObservableOrderedList(Emitter):
    """ doc
    """
    def __init__(self):
        super().__init__()
        self._list = []

    def get(self):
        """ Get the curent value
        """
        return self._list

    def add(self, items):
        """ Sets a new value
        """
        if not items:
            return
        new_items = list(items)
        new_items.sort(reverse=True)
        self._list, items_added = add_items(self._list, new_items)
        self._emit("items_added", (self, items_added))

    def remove(self, items):
        """ doc
        """
        if not items:
            return
        remove_items = list(items)
        remove_items.sort(reverse=True)
        self._list, items_removed = remove_from_list(self._list, remove_items)
        self._emit("items_removed", (self, items_removed))

    def remove_all(self):
        """ doc
        """
        if not self._list:
            return
        removed_items = self._list.copy()
        self._list = []
        self._emit("items_removed", (self, removed_items))
