'''
Created on 25.07.2017

@author: Mo
'''
from vecvis.star_chart.arrow import Arrow
from vecvis.star_chart.filter_widget import FilterWidget
from vecvis.star_chart.marker import Marker
from vecvis.observable.observable_point import ObservableVector2
from vecvis.utils.vector2 import Vector2


class Axis():
    def __init__(self, dimension_info, angle, canvas, scale, offset):
        self._info = dimension_info
        self._info.get_num_markers().add_listener("update", self._redraw_markers)
        self._angle = angle % 360
        self._direction = Vector2.angle_to_vec(angle)
        self._scale = scale
        self._scale.add_listener("update", self._calculate_start_end)
        self._offset = offset
        self._offset.add_listener("update", self._calculate_start_end)
        self._canvas = canvas
        self._start_point = ObservableVector2([0, 0])
        self._end_point = ObservableVector2(Vector2.rotate([0, 1], angle))
        self._markers = []
        self._arrow = None
        self._num_markers = self._info.get_num_markers().get()
        self._filters = []
        self._calculate_start_end(None)
        self._create_arrow()
        self._create_filters()
        self._create_markers()

    def _calculate_start_end(self, _):
        start = self._offset.get()
        end = Vector2.add(start, Vector2.mul(self._direction, self._scale.get()))
        self._start_point.set(start)
        self._end_point.set(end)

    def _create_arrow(self):
        self._arrow = Arrow(self._canvas, self._info.get_name())

    def _create_filters(self):
        filter_bottom = FilterWidget(self._start_point, self._end_point, self._info.get_min(),
                                     self._info.get_max(), self._info.get_filter_min(),
                                     self._info.get_filter_max(), False, self._canvas)
        filter_top = FilterWidget(self._start_point, self._end_point, self._info.get_min(),
                                  self._info.get_max(), self._info.get_filter_max(),
                                  self._info.get_filter_min(), True, self._canvas)
        self._filters = [filter_bottom, filter_top]

    def _create_markers(self):
        step_per_marker = 1 / (self._num_markers + 1)
        for i in range(1, self._num_markers + 1):
            self._markers.append(Marker(self._info.get_min(), self._info.get_max(),
                                        i * step_per_marker, self._canvas))
    def _redraw_markers(self, event):
        _, _, new_value = event
        self._num_markers = new_value
        for mkr in self._markers:
            mkr.remove_visuals()
        self._markers = []
        self._create_markers()
        ang = self._angle
        if ang < 180:
            ang = 90 - ang
            anc_mkr = "e"
        else:
            ang = 270 - ang
            anc_mkr = "w"
        for marker in self._markers:
            marker.create_visuals(self._start_point, self._end_point, ang, anc_mkr)

    def create_visuals(self):
        ang = self._angle
        if ang < 180:
            ang = 90 - ang
            anc_mkr = "e"
            anc_arr = "n"
        else:
            ang = 270 - ang
            anc_arr = "s"
            anc_mkr = "w"

        self._arrow.create_visuals(self._start_point, self._end_point, ang, anc_arr)
        for thefilter in self._filters:
            thefilter.create_visuals()
        for marker in self._markers:
            marker.create_visuals(self._start_point, self._end_point, ang, anc_mkr)

    def remove_visuals(self):
        self._canvas.delete("axis")
        self._canvas.delete("filter_marker")

    def value_to_point(self, value):
        min_value = self._info.get_min().get()
        max_value = self._info.get_max().get()
        min_point = self._start_point.get()
        max_point = self._end_point.get()

        normalized_value = (value - min_value) / (max_value - min_value)
        vec_start_end = Vector2.sub(max_point, min_point)
        point = Vector2.add(min_point,Vector2.mul(vec_start_end, normalized_value))
        return point
