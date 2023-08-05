""" doc
"""
from tkinter import *


class ObservableList(Listbox):
    """ doc
    """
    def __init__(self, parent, vectors, active_vector, **kwargs):
        Listbox.__init__(self, parent, **kwargs)
        self._vectors = vectors
        self._vectors.add_listener("items_added", self._on_vectors_added)
        self._vectors.add_listener("items_removed", self._on_vectors_removed)
        self.bind('<<ListboxSelect>>', self._on_selection_changed)
        self._active_vector = active_vector

    def _on_vectors_removed(self, event):
        sender, _ = event
        self.delete(0, END)
        for item in sender.get():
            self.insert(END, self._vector_to_string(item))
            if item == self._active_vector.get():
                self.selection_set(END)

    def _on_vectors_added(self, event):
        sender, _ = event
        self.delete(0, END)
        for item in sender.get():
            self.insert(END, self._vector_to_string(item))
            if item == self._active_vector.get():
                self.selection_set(END)

    def _vector_to_string(self, vector):
        vector_string = "("
        for index, value in enumerate(vector):
            vector_string = vector_string + str(value)
            if index < len(vector) - 1:
                vector_string = vector_string + ", "

        vector_string = vector_string + " )"
        return vector_string

    def _on_selection_changed(self, _):
        if self.curselection():
            index = int(self.curselection()[0])
            vector = self._vectors.get()[index]
            self._active_vector.set(vector)
