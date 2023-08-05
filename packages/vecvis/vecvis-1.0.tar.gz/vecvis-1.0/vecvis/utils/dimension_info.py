"""
Module with the DimensionInfo-class
"""

from vecvis.utils.emitter import Emitter
from vecvis.observable.observable_number import ObservableFloat, ObservableInt
from vecvis.observable.observable_string import ObservableString
from vecvis.observable.observable_bool import ObservableBool


class DimensionInfo(Emitter):
    """
    Class holding multiple informations about a dimension.

    Args
        number: int
            The id of the dimension.
    """

    def __init__(self, number):
        super().__init__()
        self._min = ObservableFloat(0)
        self._max = ObservableFloat(1)
        self._filter_min = ObservableFloat(0)
        self._filter_min.add_listener("update", self._on_filter_min_updated)
        self._filter_max = ObservableFloat(1)
        self._filter_max.add_listener("update", self._on_filter_max_updated)
        self._dimension_number = number
        self._name = ObservableString("unnamed")
        self._minimize = ObservableBool()
        self._minimize.add_listener("update", self._on_minimize_updated)
        self._num_markers = ObservableInt(3)

    def _on_filter_max_updated(self, event):
        _, old, new = event
        self._emit("filter_max_updated", (self, old, new))

    def _on_filter_min_updated(self, event):
        _, old, new = event
        self._emit("filter_min_updated", (self, old, new))

    def _on_minimize_updated(self, event):
        _, new = event
        self._emit("minimize_updated", (self, new))

    def get_name(self):
        """
        Returns the ObservableString-object for the name of the dimension.

        Returns
            ObservableString
                The Name
        """
        return self._name

    def get_min(self):
        """
        Returns the ObservableFloat-object for the
        lowest value of the dimension.

        Returns
            ObservableFloat
                The smallest value
        """
        return self._min

    def get_max(self):
        """
        Returns the ObservableFloat-object for the highest
        value of the dimension.

        Returns
            ObservableFloat
                The highest value.
        """
        return self._max

    def get_filter_min(self):
        """
        Returns the ObservableFloat-object holding the value of the
        lower filter.

        Returns
            ObservableFloat
                The lower filter.
        """
        return self._filter_min

    def get_filter_max(self):
        """
        Returns the ObservableFloat-object holding the value of the
        higher filter.

        Returns
            ObservableFloat
                The higher filter.
        """
        return self._filter_max

    def get_minimize(self):
        """
        Returns the ObservableBool-object holding the value whether
        smaller values are better on this dimension.

        Returns
            ObservableBool
                Are smaller values better?
        """
        return self._minimize

    def get_number(self):
        """
        Returns the number of the dimension this info-object is for.

        Returns
            int
        """
        return self._dimension_number

    def get_num_markers(self):
        """
        Returns the ObservableInt which wrappes the value of
        how many markers get rendered on the starchart.

        Returns
            ObservableInt
        """
        return self._num_markers
