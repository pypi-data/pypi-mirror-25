# encoding: utf-8
"""
The main Module for Vecvis.
"""
import queue
import threading
import time
import tkinter
from distutils.dist import warnings
import vecvis.mvp.model
import vecvis.mvp.presenter


class API(threading.Thread):
    """
    Use this constructor to open the GUI.
    Later on this instance can be used to send orders to the module.

    Args:
        ``num_dimensions: int``
            The number of dimensions the vectors you want to add have.

        ``names: list<string>``, *optional*
            List with names of the dimensions.
            Default names are set to "a", "b", "c" and so on.
            If the name of one dimension should not be changed
            set the corresponding entry to ``None``.
        ``value_ranges: list<tuple<float, float>>``
            List of tuples with two floats. First float sets the minimal value
            on the axis. Second float sets the maximal value.
            By default each axis has the range 0 - 1. If you don't want to change
            the default value of an axis, set the corresponding entry in the list to ``None``.
        ``minimize: set<int>``
            A set with integers. If an integer *i* is present in the set the module
            will regard smaller values as better in the dimension *i*.
        ``num_markers: list<int>``
            List with how many marker appear on the axes. Default value is 3.
            If you don't want to change the amount of markers on one axis,
            set the corresponding value to ``None``.
    """

    def __init__(self, num_dimensions, names=[], value_ranges=[], minimize=set(), num_markers=[]):
        """
        Sets up and starts the Program.
        """
        self._show_warnings = True
        if tkinter.TkVersion < 8.6:
            self._error("Tcl/Tk is needed in a Version higher or equal to 8.6." +
                        "Your installed version is: " + str(tkinter.TkVersion))
            return

        # check if num_dimensions is greater 2
        try:
            num_dimensions = int(num_dimensions)
        except Exception:
            self._warn(
                "'" + str(num_dimensions) +
                "' can't be converted to int. num_dimensions will be set to 3")
            num_dimensions = 3

        if num_dimensions < 3:
            self._warn(
                "num_dimensions is less than 3. num_dimensions will be set to 3")
            num_dimensions = 3

        self._num_dimensions = num_dimensions
        # super constructor
        threading.Thread.__init__(self, name="gui thread")
        # condition object to be used at startup
        self._start_semaphore = threading.Semaphore(value=0)

        self.message_queue = queue.Queue()
        self._should_stop = False
        self.name = "GUI Thread"
        self._gui_thread = None
        self._model = None
        self._presenter = None
        self.setDaemon(True)
        # start the Thread, initialize the ui
        self.start()

        # wait for the initialisation to be finished
        self._start_semaphore.acquire()

        # set default stuff
        self._init_names(names)
        self._init_value_ranges(value_ranges)
        self.set_minimizes(minimize)
        self._init_num_markers(num_markers)

    def _init_names(self, names):
        if not names:
            names = []

        while len(names) < self._num_dimensions:
            names.append(None)

        for i in range(self._num_dimensions):
            if not names[i]:
                names[i] = str(chr(ord('a') + i))
        self.set_names(names)

    def _init_value_ranges(self, ranges):
        while len(ranges) < self._num_dimensions:
            ranges.append([0, 1])

        for i in range(self._num_dimensions):
            if not ranges[i]:
                ranges[i] = [0, 1]
        self.set_value_ranges(ranges)

    def _init_num_markers(self, num_markers):
        while len(num_markers) < self._num_dimensions:
            num_markers.append(3)
        self.set_marker_amounts(num_markers)

    def add_vector(self, vector):
        """
        Adds a single vector to the UI.

        Args:
            ``vector: tuple<float>``
                The vector to be added. A tuple with float values.
        """
        # switch the thread if necessary
        if threading.current_thread() != self._gui_thread:
            vectors = set()
            vector = self._check_vector(vector)
            if vector is not None:
                vectors.add(vector)
                self._run_in_gui_thread(self.add_vectors, vectors)

    def add_vectors(self, vectors):
        """
        Adds multiple vectors to the UI.

        Args:
            ``vectors: set<tuple<float>>``
                A set of tuples with the vectors to be added to the UI.
        """
        # switch the thread if necessary
        if threading.current_thread() != self._gui_thread:
            # check container
            try:
                vectors = set(vectors)
            except Exception:
                self._print_conversion_error(vectors, "list")
                return
            # check vectors
            valid_vectors = set()
            for vector in vectors:
                vec = self._check_vector(vector)
                if vec is not None:
                    valid_vectors.add(vec)
            self._run_in_gui_thread(self.add_vectors, valid_vectors)
        else:
            self._model.add_vectors(vectors)

    def _check_vector(self, vector):
        """
        Checks if a vector is valid.

        Args:
            ``vector: hopefully iterable``
                The vector to check.

        Returns:
            ``None | list<int|float>``
                Returns ``None`` if the vector is not valid.
                Returns the Vector if it is valid.
        """
        vector_to_check = vector
        # check container
        try:
            vector = list(vector)
        except Exception:
            self._print_conversion_error(vector, "iterable")
            return None
        # check entries
        for i in range(len(vector)):
            try:
                vector[i] = float(vector[i])
            except Exception:
                self._print_entry_error(vector_to_check, "float")
                return None
        # check length
        if len(vector) < self._num_dimensions:
            self._warn("Vector '" + str(vector_to_check) +
                       "' is too short. Missing dimensions will be set to zero.")
            while len(vector) < self._num_dimensions:
                vector.append(0.0)
        if len(vector) > self._num_dimensions:
            self._warn("Vector '" + str(vector_to_check) +
                       "' is too long. Additional dimensions will be ignored.")
            vector = vector[0:self._num_dimensions]
        return tuple(vector)

    def set_names(self, names):
        """
        Sets the names of the dimensions.

        Args:
            ``name: list<String|None>``
                The names of the dimensions. If you don't want to change
                a name of a dimension you can pass ``None`` at the corresponding position.
        """
        try:
            names_to_add = list(names)
        except Exception:
            self._print_conversion_error(names, "list")
            return
        while len(names) < self._num_dimensions:
            names.append(None)

        for i in range(self._num_dimensions):
            if names[i] is not None:
                self.set_name(i, names[i])

    def set_name(self, dimension, name):
        """
        Sets the name of a single dimension.
        The name is displayed at the corresponding axis.

        Args:
            ``dimension: int``
                The number of the dimension that you want to name.
            ``name: str``
                The new name for the dimension.
        """
        # switch the thread if necessary
        if threading.current_thread() != self._gui_thread:
            try:
                dim_to_set = int(dimension)
            except Exception:
                self._print_conversion_error(dimension, "int")
                return

            try:
                name_to_set = str(name)
            except Exception:
                self._error("Given Parameter can't be converted to String'")
                return

            if dim_to_set < 0 or dim_to_set >= self._num_dimensions:
                self._error(str(dim_to_set) + "' is not a valid dimension index.")
                return

            self._run_in_gui_thread(self.set_name, dim_to_set, name_to_set)
        else:
            self._model.set_dimension_name(dimension, name)

    def set_value_ranges(self, ranges, reset_filters=True):
        """
        Sets minimal and maximal displayable values for the axes.

        Args:
            ``ranges: list<tuple<float, float>|None>``
            A list with a tuple for each dimension. The tuple contains
            respectively minimal and the maximal values.
        """
        try:
            ranges = list(ranges)
        except Exception:
            self._print_conversion_error(ranges, "list")
            return
        while len(ranges) < self._num_dimensions:
            ranges.append(None)

        for i in range(self._num_dimensions):
            if ranges[i]:
                self.set_value_range(i, ranges[i], reset_filter=reset_filters)

    def set_value_range(self, dimension, minmax, reset_filter=True):
        """
        Sets the displayable minimal and maximal value for one dimension.

        Args:
            ``dimension: int``
                Number of the dimension.
            ``minmax: tuple<float, float>``
                Tuple with min and max value displayable on the axis.
            ``reset_filter: bool``
                Whether or not the filter should be set to the new minimal and maximal value.
                Default is True.
        """
        # switch the thread if necessary
        if threading.current_thread() != self._gui_thread:
            try:
                dimension = int(dimension)
            except Exception:
                self._print_conversion_error(dimension, "int")
                return
            try:
                minmax = list(minmax)
            except Exception:
                self._print_conversion_error(minmax, "iterable")
                return

            if len(minmax) >= self._num_dimensions:
                self._warn("The tuple has more than two entries. " +
                           "Additional entries will be ignored")

            if len(minmax) < 2:
                self._error("'" + str(minmax) + "' has less than 2 entries.")
                return
            for i in range(2):
                try:
                    minmax[i] = float(minmax[i])
                except:
                    self._print_entry_error(minmax, "float")
                    return
            if minmax[0] > minmax[1]:
                self._warn("Min value is greater max value. Switching values.")
                minmax[1], minmax[0] = minmax[0], minmax[1]

            if minmax[0] == minmax[1]:
                self._error(
                    "A dimensions mustn't have the same min and max value.")
                return
            if dimension >= self._num_dimensions or dimension < 0:
                self._print_dimension_error(dimension)
                return

            self._run_in_gui_thread(
                self.set_value_range, dimension, minmax, reset_filter)
        else:
            self._model.set_dimension_value_range(
                dimension, minmax[0], minmax[1], reset_filter)

    def calculate_value_ranges(self, reset_filter=True):
        """
        Sets displayable min and max for each axis. After this operation
        all vectors currently added to the UI are visible.

        Args:
            ``reset_filter: bool``
                Whether or not the filter should be set to the new minimal and maximal values.
                Default is True.
        """
        # switch the thread if necessary
        if threading.current_thread() != self._gui_thread:
            self._run_in_gui_thread(
                self.calculate_value_ranges, reset_filter=reset_filter)
            return
        self._presenter.calculate_scales(reset_filter)

    def set_minimizes(self, minimize):
        """
        Sets if smaller values should be considered better or not in a dimension.

        Args:
            ``minimize: set<int>``
                A Set with the numbers of the dimensions where smaller values are better.
                In all other dimensions grater values are regarded to be better.
        """
        try:
            minimize = set(minimize)
        except Exception:
            self._print_conversion_error(minimize, "set")
            return
        for dim in range(self._num_dimensions):
            if dim in minimize:
                self.set_minimize(dim, True)
            else:
                self.set_minimize(dim, False)

    def set_minimize(self, dimension, minimize):
        """
        Explicity sets whether small values are better or not for one dimension.

        Args:
            ``dimension: int``
                Zero based number of the dimension.
            ``minimize: bool``
                Set to True if smaller values are better.
                False if greater values should be better.
        """
        # switch the thread if necessary
        if threading.current_thread() != self._gui_thread:
            try:
                minimize = bool(minimize)
            except Exception:
                self._print_conversion_error(minimize, "bool")
                return
            try:
                dimension = int(dimension)
            except Exception:
                self._print_conversion_error(dimension, "int")
                return
            if dimension < 0 or dimension >= self._num_dimensions:
                self._print_dimension_error(dimension)
                return
            self._run_in_gui_thread(
                self.set_minimize, dimension, minimize)
            return
        else:
            self._model.set_dimension_minimize(dimension, minimize)

    def set_marker_amounts(self, num_markers):
        """
        Sets the amount of visible markers for each axis.

        Args:
            ``num_markers: List<int|None>``
                List with number of markers for each dimension. Set
                one entry to ``None`` if the number of displayed markers
                should not be changed on the axis.
        """
        try:
            num_markers = list(num_markers)
        except Exception:
            self._print_conversion_error(num_markers, "list")
            return
        while len(num_markers) < self._num_dimensions:
            num_markers.append(None)
        for i in range(self._num_dimensions):
            if num_markers[i] is not None:
                self.set_marker_amount(i, num_markers[i])

    def set_marker_amount(self, dimension, num_markers):
        """
        Sets the amount of markers for one axis.

        Args:
            ``dimension: int``
                The corresponding dimension to the axis.
            ``num_markers: int``
                Number of markers.
        """
        if threading.current_thread() != self._gui_thread:
            try:
                dimension = int(dimension)
            except Exception:
                self._print_conversion_error(dimension, "int")
                return
            try:
                num_markers = int(num_markers)
            except Exception:
                self._print_conversion_error(num_markers, "int")
                return
            if dimension < 0 or dimension >= self._num_dimensions:
                self._print_dimension_error(dimension)
                return
            if num_markers < 0:
                self._warn(
                    "Less than 0 markers are unacceptable. Setting num_markers to 0.")
                num_markers = 0
            self._run_in_gui_thread(
                self.set_marker_amount, dimension, num_markers)
        else:
            self._model.get_dimension_infos(
            )[dimension].get_num_markers().set(num_markers)

    def close(self):
        """
        Terminates the Application.
        """
        if threading.current_thread() != self._gui_thread:
            self._run_in_gui_thread(self.close)
            return
        self._should_stop = True
        self._presenter.close()

    def disable_warnings(self):
        """
        Disables the output of warnings to the console.
        """
        self._show_warnings = False

    def _warn(self, message):
        if self._show_warnings:
            print("WARNING: " + message)

    def _error(self, message):
        print("ERROR: " + message)

    def _print_conversion_error(self, obj, target_name):
        self._error("'" + str(obj) + "' can't be converted to " + target_name + ".")

    def _print_dimension_error(self, dimension):
        self._error("'" + str(dimension) + "' is not a valid dimension index.")

    def _print_entry_error(self, obj, target_name):
        self._error("An entry of '" + str(obj) + "' can't be converted to " + target_name + ".")

    def run(self):
        # Get reference to our thread. Needed to decide later if we need to
        # change the thread
        self._gui_thread = threading.current_thread()

        # Create and link MVP-Stuff
        self._create_mvp()

        # All MVP stuff created, let the constructor return
        self._start_semaphore.release()

        # start our event loop
        self._event_loop()

    def _create_mvp(self):
        self._model = vecvis.mvp.model.Model(self._num_dimensions)
        self._presenter = vecvis.mvp.presenter.Presenter()
        self._presenter.set_model(self._model)
        self._presenter.present()

    def _event_loop(self):
        time_per_update = 1 / 30
        while not self._should_stop:
            start_time = time.time()
            self._process_queue_events()
            if not self._presenter.update():
                self.close()
            delta_time = time.time() - start_time
            time.sleep(max(0.0, time_per_update - delta_time))

    def _process_queue_events(self):
        while not self.message_queue.empty():
            try:
                function, args, kwargs = self.message_queue.get(block=False)
                function(*args, **kwargs)
            except queue.Empty:
                break

    def _run_in_gui_thread(self, function, *args, **kwargs):
        self.message_queue.put((function, args, kwargs))