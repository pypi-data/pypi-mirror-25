'''
Created on 25.07.2017

@author: Mo
'''
from tkinter import Canvas

from vecvis.utils.emitter import Emitter
from vecvis.utils.vector2 import Vector2
from vecvis.observable.observable_number import ObservableFloat
from vecvis.observable.observable_point import ObservableVector2
from vecvis.star_chart.axis import Axis
from vecvis.star_chart.polygon import Polygon


class StarChart(Canvas, Emitter):
    """
    The starchart-widget.

    Args
        parent: Widget
            The parent widget
        dimsension_infos: list<DimensionInfo>
            The information about the dimensions to be shown.
        vectors: ObservableOrderedList
            The vectors this starchart should show as polygons.
        highlighted_vector: ObservableTuple
            The polygon for the vector inside the ObservableTuple gets
            highlighted in the starchart.
        **kwargs:
            named args for the tk Canvas
    """
    NORMAl_COLOR = "ORANGE"
    HIGHLIGHT_COLOR = "BLUE"

    def __init__(self, parent, dimension_infos, vectors, highlighted_vector, **kwargs):
        Canvas.__init__(self, parent, width=1, height=1, **kwargs)
        Emitter.__init__(self)

        self.bind("<B3-Motion>", self._on_drag)
        self.bind("<Button-3>", self._on_click)
        self.bind("<Configure>", self._on_canvas_resize)
        self.bind_all("<space>", self._reset_view)
        self.bind_all("+", self._on_plus_clicked)
        self.bind_all("-", self._on_minus_clicked)

        self._infos = dimension_infos
        for info in self._infos:
            info.get_min().add_listener("update", self._redraw_polygons)
            info.get_max().add_listener("update", self._redraw_polygons)

        self._scale = 1
        self._user_scale = 1
        self._offset = [0, 0]
        self._user_offset = [0, 0]
        self._last_pos = [0, 0]
        self._ges_scale = ObservableFloat(self._user_scale * self._scale)
        self._ges_offset = ObservableVector2(Vector2.add(self._user_offset, self._offset))

        self._highlighted_vector = highlighted_vector
        self._highlighted_vector.add_listener("update", self._on_highlited_chaned)
        self._vectors = vectors
        self._vectors.add_listener("items_added", self._on_vectors_added)
        self._vectors.add_listener("items_removed", self._on_vectors_removed)
        self._polygons = {}

        self._axes = []
        self._create_axes()

    def _on_highlited_chaned(self, event):
        _, old, new = event
        if old in self._polygons:
            self._polygons[old].set_color(StarChart.NORMAl_COLOR)
        if new in self._polygons:
            self._polygons[new].set_color(StarChart.HIGHLIGHT_COLOR)
        self._ensure_z_index()

    def _on_vectors_added(self, event):
        _, vectors = event
        for vector in vectors:
            polygon = Polygon(self._axes, self, StarChart.NORMAl_COLOR, vector)
            self._polygons[vector] = polygon
            polygon.create_visuals()
        self._ensure_z_index()

    def _on_vectors_removed(self, event):
        _, vectors = event
        for vector in vectors:
            if vector not in self._polygons:
                continue
            polygon = self._polygons.pop(vector, None)
            polygon.remove_visuals()
            if vector == self._highlighted_vector.get():
                self._highlighted_vector.set(None)
        self._ensure_z_index()

    def _on_canvas_resize(self, event):
        # How to move to stay in the center?
        offset_cange = [event.width / 2 - self._offset[0],
                        event.height / 2 - self._offset[1]]
        self.move("all", offset_cange[0], offset_cange[1])
        self._offset = [event.width / 2, event.height / 2]

        # How much would we have to scale if the canvas was still 1x1 px?
        ges_scale_x = (float(event.width) / 2 - 30)
        ges_scale_y = (float(event.height) / 2 - 30)
        # Take the current scale into account
        new_scale = min(ges_scale_x, ges_scale_y)
        scale_change = new_scale / self._scale

        # scale the stuff!
        if scale_change != 0:
            self.scale("all", self._offset[0] + self._user_offset[0],
                       self._offset[1] + self._user_offset[1],
                       scale_change, scale_change)
            self._scale = new_scale

        # Sets ges_scale and ges_offset, so that the axes can recalculate thier points.
        self._apply_scale_and_offset()

    def _on_click(self, event):
        self._last_pos = [event.x, event.y]

    def _on_drag(self, event):
        self.increase_user_offset(- (self._last_pos[0] - event.x),
                                  - (self._last_pos[1] - event.y))
        self._last_pos = [event.x, event.y]

    def _on_plus_clicked(self, _):
        self.increase_user_scale(1.7)

    def _on_minus_clicked(self, _):
        self.increase_user_scale(1/1.7)

    def _reset_view(self, _):
        self.increase_user_offset(- self._user_offset[0],
                                  - self._user_offset[1])
        self.increase_user_scale(1 / self._user_scale)

    def increase_user_scale(self, amount):
        """doc
        """
        self.scale("all", self._offset[0] + self._user_offset[0],
                   self._offset[1] + self._user_offset[1],
                   amount, amount)
        usr_x, usr_y = self._user_offset
        self.increase_user_offset((usr_x * amount) - usr_x,
                                  (usr_y * amount) - usr_y)
        self._user_scale *= amount
        self._apply_scale_and_offset()

    def increase_user_offset(self, offset_x, offset_y):
        """ doc
        """
        self.move("all", offset_x,  offset_y)
        self._user_offset = [self._user_offset[0] +
                             offset_x, self._user_offset[1] + offset_y]
        self._apply_scale_and_offset()

    def _apply_scale_and_offset(self):
        self._ges_offset.set(Vector2.add(self._offset, self._user_offset))
        self._ges_scale.set(self._user_scale * self._scale)

    def _create_axes(self):
        angle_per_axis = 360 / len(self._infos)
        current_angle = -90

        for i in range(len(self._infos)):
            new_axis = Axis(self._infos[i], current_angle, self, self._ges_scale, self._ges_offset)
            new_axis.create_visuals()
            self._axes.append(new_axis)
            current_angle = current_angle + angle_per_axis
        self._ensure_z_index()

    def _ensure_z_index(self):
        self.tag_raise("axis")
        self.tag_raise("polygon")
        if self._highlighted_vector.get() in self._polygons:
            self._polygons[self._highlighted_vector.get()].tag_raise()
        self.tag_raise("filter_marker")

    def _redraw_polygons(self, _):
        for polygon in self._polygons:
            self._polygons[polygon].remove_visuals()
            self._polygons[polygon].create_visuals()
            self._ensure_z_index()
