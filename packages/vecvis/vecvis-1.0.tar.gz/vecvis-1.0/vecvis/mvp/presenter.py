"""
Module holding the Presenter-class.
"""
from vecvis.mvp.view import View
from vecvis.utils.utils import calculate_vectors_min_max
from vecvis.utils.simple_cull import simple_cull


class Presenter():
    """
    The MVP-Presenter
    """
    def __init__(self):
        self._model = None
        self._view = None

    def set_model(self, model):
        """
        Sets the Model for this Presenter.

        Args
            model: Model
                The model
        """
        self._model = model
        self._model.get_all_vectors().add_listener("items_added", self._on_vectors_added)

        self._model.get_non_axis_filtered_vectors().\
            add_listener("items_added", self._on_non_filtered_vectors_added)

        self._model.get_non_axis_filtered_vectors().\
            add_listener("items_removed", self._on_non_filtered_vectors_removed)

        for info in self._model.get_dimension_infos():
            info.add_listener("filter_min_updated", self._filter_min_updated)
            info.add_listener("filter_max_updated", self._filter_max_updated)
            info.add_listener("minimize_updated", self._on_minimize_updated)

        self._model.get_obsb_pareto().add_listener("update", self._pareto_enabled_updated)

    def _pareto_enabled_updated(self, event):
        _, new_value = event
        if new_value:
            self._update_pareto()
        else:
            vectors_to_add = self._model.get_non_axis_filtered_vectors().get().copy()
            self._model.get_active_vectors().add(vectors_to_add)

    def calculate_scales(self, reset_filter):
        """
        Calculates and sets the min and max values for each dimension.
        Each vector this is added can then be displayed.

        Args:
            reset_filter: bool
                Set to True if you want the filter to be set to the new
                min and max.
        """
        vectors = self._model.get_all_vectors().get()
        if vectors:
            ranges = calculate_vectors_min_max(vectors)
            for i in range(len(ranges)):
                self._model.set_dimension_value_range(i, ranges[i][0], ranges[i][1],
                                                      reset_filter=reset_filter)

    def _on_vectors_added(self, event):
        """
        Called when vectors are added to the program

        Args
            event: Tuple<ObservableSet, set>
                The added vectors are inside the set
        """
        _, vectors = event
        vectors_to_add = set()
        # check if each vector is outoplayed by a axis-filter
        for vector in vectors:
            if self._is_not_filtered(vector):
                vectors_to_add.add(vector)
        # add the vectors to the non-axisfilterde vectors
        self._model.get_non_axis_filtered_vectors().add(vectors_to_add)

    def _on_non_filtered_vectors_added(self, event):
        """
        Called when vectors have been added to the non-axisfiltered vectors

        Args
            event: Tuple<ObservableList, list>
        """
        _, new_vectors = event
        # Check if the paretofilter is on:
        if self._model.get_is_pareto_on():
            self._update_pareto()
        else:
            self._model.get_active_vectors().add(new_vectors)

    def _on_non_filtered_vectors_removed(self, event):
        _, removed_vectors = event
        # Check if the paretofilter is on:
        if self._model.get_is_pareto_on():
            self._model.get_active_vectors().remove(removed_vectors)
            self._update_pareto()
        else:
            self._model.get_active_vectors().remove(removed_vectors)

    def _update_pareto(self):
        # calculate pareto front
        minimize = []
        for info in self._model.get_dimension_infos():
            minimize.append(info.get_minimize().get())
        non_dom, dom = simple_cull(self._model.get_non_axis_filtered_vectors().get(), minimize)
        self._model.get_active_vectors().remove(dom)
        self._model.get_active_vectors().add(non_dom)

    def _on_minimize_updated(self, _):
        self._update_pareto()

    def present(self):
        """
        Call this method if the preseter should start his work.
        """
        if self._model is None:
            return
        if self._view is not None:
            return
        self._view = View(self._model.get_dimension_infos(),
                          self._model.get_active_vectors(), self._model.get_obsb_pareto())
        self._view.add_listener("reset_filter", self._on_reset_filter)

    def update(self):
        """
        Updates the UI.

        Returns
            bool
                False if the programm should be terminated
        """
        return self._view.update()

    def _is_not_filtered(self, vector):
        # check if the vector is not filtered
        infos = self._model.get_dimension_infos()
        for info in infos:
            dim = info.get_number()
            if vector[dim] < info.get_filter_min().get() or\
                    vector[dim] > info.get_filter_max().get():
                return False
        return True

    def _filter_min_updated(self, event):
        sender, old, new = event
        dim = sender.get_number()
        active_vectors = self._model.get_non_axis_filtered_vectors().get()
        all_vectors = self._model.get_all_vectors().get()
        vectors_to_add = set()
        vectors_to_remove = set()
        if new > old:
            # filter is more strict
            for vector in active_vectors:
                if vector[dim] < new:
                    vectors_to_remove.add(vector)
        else:
            # filter is less strict
            for vector in all_vectors:
                if self._is_not_filtered(vector):
                    vectors_to_add.add(vector)

        self._model.get_non_axis_filtered_vectors().add(vectors_to_add)
        self._model.get_non_axis_filtered_vectors().remove(vectors_to_remove)

    def _filter_max_updated(self, event):
        sender, old, new = event
        dim = sender.get_number()
        active_vectors = self._model.get_non_axis_filtered_vectors().get()
        all_vectors = self._model.get_all_vectors().get()
        vectors_to_add = []
        vectors_to_remove = []
        if new < old:
            # filter is more strict
            for vector in active_vectors:
                if vector[dim] > new:
                    vectors_to_remove.append(vector)
        else:
            # filter is less strict
            for vector in all_vectors:
                if self._is_not_filtered(vector):
                    vectors_to_add.append(vector)

        self._model.get_non_axis_filtered_vectors().add(vectors_to_add)
        self._model.get_non_axis_filtered_vectors().remove(vectors_to_remove)

    def _on_reset_filter(self, _):
        infos = self._model.get_dimension_infos()
        for info in infos:
            info.get_filter_max().set(info.get_max().get())
            info.get_filter_min().set(info.get_min().get())

    def close(self):
        self._view.close()
