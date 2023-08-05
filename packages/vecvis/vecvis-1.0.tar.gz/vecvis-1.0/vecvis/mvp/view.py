"""
Module holding the View-Class.
"""
from tkinter import *

from vecvis.utils.emitter import Emitter
from vecvis.star_chart.star_chart import StarChart
from vecvis.observable.observable_tuple import ObservableTuple
from vecvis.utils.ui.observable_list import ObservableList
from vecvis.utils.ui.observable_checkbox import BoundCheckbox


class View(Emitter):
    """
    A View-class.

    Args
        dimension_infos: List<DimensionInfo>
            Infos about the dimensions.
        vectors: ObservableList
            List with vectors that should be displayed.
        obs_bool_pareto: ObservableBool
            Holding the info if the pareto-filter is enabled
    """
    def __init__(self, dimension_infos, vectors, obs_bool_pareto):
        super().__init__()
        self._window = None
        self._star_chart = None
        self._list_box = None
        self._window_closed = False
        self._highlighted_vector = ObservableTuple(None)
        self._dimension_infos = dimension_infos
        self._vectors = vectors
        self._obs_bool_pareto = obs_bool_pareto

        self._build_ui()

        # Call update once to get the resolution of the canvas in the starchart
        self._window.update()
        #self._window.iconify()
        #self._window.deiconify()
        #self._window.state('zoomed')
        #self._window.attributes("-fullscreen", True)

    def _build_ui(self):
        self._window = Tk()
        self._window.minsize(400, 300)
        self._window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._window.wm_title("VecVis")
        # PannedWindow has left and right
        main_panned_window = PanedWindow(self._window, sashwidth=5, sashrelief=RAISED)
        # Create the StarChart and put it on the left side
        self._star_chart = StarChart(self._window, self._dimension_infos,
                                     self._vectors, self._highlighted_vector, bg='white')
        main_panned_window.add(self._star_chart, stretch="always", minsize=200)

        container_frame = Frame(self._window)
        options_frame = Frame(container_frame, bg="WHITE", border=5)
        checkbox = BoundCheckbox(options_frame, self._obs_bool_pareto,
                                 text="Parteo Filter", bg="WHITE", activebackground="WHITE")
        checkbox.pack(side=RIGHT)
        btn_reset_filter = Button(options_frame, text="Reset filter",
                                  command=self._on_btn_reset_filter_clicked)
        btn_reset_filter.pack(side=LEFT)
        options_frame.pack(fill=X)

        list_frame = Frame(container_frame)
        scrollbar = Scrollbar(list_frame, orient=VERTICAL)
        self._list_box = ObservableList(
            list_frame, self._vectors, self._highlighted_vector, relief=FLAT,
            yscrollcommand=scrollbar.set, highlightthickness=0)
        scrollbar.config(command=self._list_box.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self._list_box.pack(fill=BOTH, expand=1)
        list_frame.pack(fill=BOTH, expand=1)

        main_panned_window.add(container_frame, stretch="never", minsize=220)
        # Add the PannedWindwo to the UI
        main_panned_window.pack(fill=BOTH, expand=1, side=LEFT)

    def _on_closing(self):
        """ Callback called when the window closes.
        Occurs when the user hits the 'x' - button.
        """
        self._window_closed = True
        try:
            self._window.destroy()
        except:
            pass

    def close(self):
        """
        Closes the Window and 'terminates' the View
        """
        try:
            self._window.destroy()
        except:
            pass
        self._window_closed = True

    def update(self):
        """
        Keeps the Window form freezing. Returns False if the Window is closed.

        Returns:
            Bool
                True if the Window is still open, False in other cases
        """
        if not self._window_closed:
            try:
                self._window.update()
            except:
                return False
            return True
        return False

    def _on_btn_reset_filter_clicked(self):
        self._emit("reset_filter", None)
