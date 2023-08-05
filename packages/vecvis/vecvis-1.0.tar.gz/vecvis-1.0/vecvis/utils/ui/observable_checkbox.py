""" doc
"""
from tkinter import *


class BoundCheckbox(Checkbutton):
    """ doc
    """
    def __init__(self, parent, obs_bool, **kwargs):
        self._value = obs_bool
        self._current_state = False
        # intvar causes some problems because of threading
        # quick and dirty solution: ignore it.
        # seems like there is no better solution.
        # self._intvar = IntVar(int(obs_bool.get()))
        Checkbutton.__init__(self, parent,
                             command=self._on_value_changed, **kwargs)
        self.deselect()

    def _on_obs_value_changed(self, event):
        _, new = event
        if new != self._current_state:
            self.toggle()
            self._current_state = not self._current_state

    def _on_value_changed(self):
        self._current_state = not self._current_state
        self._value.set(self._current_state)
