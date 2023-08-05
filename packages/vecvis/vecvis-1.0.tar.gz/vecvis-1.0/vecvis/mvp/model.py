"""
Module with the Model-Class.
"""
from vecvis.utils.dimension_info import DimensionInfo
from vecvis.observable.obserable_set import ObservableSet
from vecvis.observable.observable_ordered_list import ObservableOrderedList
from vecvis.observable.observable_bool import ObservableBool


class Model():
    """
    This class represents the Model.

    Args
        num_dimensions: int
            The number of dimensions that should be managed by this Model.
    """
    def __init__(self, num_dimensions):
        self._dimensions_infos = [DimensionInfo(i) for i in range(num_dimensions)]
        self._active_vectors = ObservableOrderedList()
        self._non_axis_filtered_vectors = ObservableOrderedList()
        self._all_vectors = ObservableSet()
        self._pfilter_enabled = ObservableBool()

    def set_dimension_name(self, dimension, name):
        """
        Sets the name of a specified dimension

        Args
            dimensions: int
                The index of the dimension
            name: str
                The new name
        """
        self._dimensions_infos[dimension].get_name().set(name)

    def set_dimension_minimize(self, dimension, minimize):
        """
        Sets whether small values are considered better in a given dimension.

        Args:
            dimension: int
                The index of the dimension.
            minimize: bool
                Set to True if smaller values are better.
        """
        self._dimensions_infos[dimension].get_minimize().set(minimize)

    def set_dimension_num_marker(self, dimension, num_markers):
        """
        Sets the number of markers appearing on the axis for the given dimension.

        Args
            dimension: int
                The index of the dimension.
            num_markers: int
                How many Markers should appear?
        """
        self._dimensions_infos[dimension].get_num_markers().set(num_markers)

    def add_vectors(self, vectors):
        """
        Adds a collection of vectors to the programm.

        Args
            vectors: iterable<iterable<Number>>
                The vectors.
        """
        self._all_vectors.add(vectors)

    def get_dimension_infos(self):
        """
        Returns a list with an info-object for each dimension.

        Returns
            list<DimensionInfo>
                List with the info-objects
        """
        return self._dimensions_infos

    def get_all_vectors(self):
        """
        Returns all vectors that have been added to the program.

        Returns
            ObservableSet
                All vectors.
        """
        return self._all_vectors

    def get_active_vectors(self):
        """
        Returns a list of vectors that are not filtered
        neither by the sliders nor by the pareto-filter.

        Returns
            ObservableList
                The vectors.
        """
        return self._active_vectors

    def get_non_axis_filtered_vectors(self):
        """
        Returns a list of vectors that are not filtered
        by the sliders on the axes of the starchart.

        Returns
            ObservableList
                The vectors.
        """
        return self._non_axis_filtered_vectors

    def get_is_pareto_on(self):
        """
        Returns a boolean indicating if the pareto-filter is turned on.

        Returns
            bool
                True if the pareto-filter is turned on. False else.
        """
        return self._pfilter_enabled.get()

    def get_obsb_pareto(self):
        """
        Returns an ObservableBool with the flag whether the pareto-filter is on.

        Returns
            ObservableBool
                Flag if pareto-filter is on
        """
        return self._pfilter_enabled

    def set_pareto_active_state(self, is_active):
        """
        Enables or disables the pareto-filter.

        Args
            is_active: bool
                Set to True if the pareto-filter should be on.
        """
        self._pfilter_enabled.set(is_active)

    def set_dimension_value_range(self, dimension, min_value, max_value, reset_filter):
        """
        Sets the min an max values for a dimension.

        Args:
            dimension: int
                The index of the dimension.
            min_value: number
                The smallest value.
            max_value: number
                The highest value.
            reset_filter: bool
                Set to True if you want to set the filters to the
                new min and max
        """
        if min_value == max_value:
            min_value = min_value - 1

        if min_value == self._dimensions_infos[dimension].get_max().get():
            self._dimensions_infos[dimension].get_min().set(min_value - 1)
            self._dimensions_infos[dimension].get_max().set(max_value)
            self._dimensions_infos[dimension].get_min().set(min_value)
        else:
            self._dimensions_infos[dimension].get_min().set(min_value)
            self._dimensions_infos[dimension].get_max().set(max_value)

        if reset_filter:
            self._dimensions_infos[dimension].get_filter_min().set(min_value)
            self._dimensions_infos[dimension].get_filter_max().set(max_value)
