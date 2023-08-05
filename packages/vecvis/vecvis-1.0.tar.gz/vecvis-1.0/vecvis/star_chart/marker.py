'''
Created on 24.07.2017

@author: Mo
'''
from vecvis.utils.vector2 import Vector2


class Marker():
    SIZE = 0.032
    def __init__(self,min_value, max_value, npos, canvas):
        self._min_value = min_value
        self._min_value.add_listener("update", self._set_text_value)
        self._max_value = max_value
        self._max_value.add_listener("update", self._set_text_value)
        self._npos = npos
        self._line_widget = None
        self._text_widget = None
        self._canvas = canvas

    def create_visuals(self, min_point, max_point, text_angle, text_anchor):
        """ doc """
        canvas = self._canvas
        min_point = min_point.get()
        max_point = max_point.get()
        start_end = Vector2.sub(max_point, min_point)
        scale = Vector2.len(start_end)
        direction = Vector2.normalize(start_end)
        direction2 = Vector2.rotate(direction, 90)
        start_point = Vector2.add(
            min_point, Vector2.mul(direction, self._npos * scale))
        point_1 = Vector2.add(start_point, Vector2.mul(
            direction2, Marker.SIZE * scale))
        point_0 = Vector2.sub(start_point, Vector2.mul(
            direction2, Marker.SIZE * scale))

        self._line_widget = canvas.create_line(point_0[0], point_0[1], point_1[0], point_1[1],
                                               tag="axis", fill="RED")
        self._text_widget = canvas.create_text(point_1[0], point_1[1], text=" ",
                                               angle=text_angle, anchor=text_anchor,
                                               tag="axis")
        self._set_text_value(None)

    def remove_visuals(self):
        """
        Deletes this marker form the canvas
        """
        self._canvas.delete(self._line_widget)
        self._canvas.delete(self._text_widget)
        self._min_value.remove_listener("update", self._set_text_value)
        self._max_value.remove_listener("update", self._set_text_value)

    def _set_text_value(self, _):
        value = (self._max_value.get() - self._min_value.get()) * self._npos + self._min_value.get()
        value = int(value * 100) / 100
        self._canvas.itemconfig(self._text_widget, text=" "+str(value) + " ")
