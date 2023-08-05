'''
Created on 24.07.2017

@author: Mo
'''
from vecvis.utils.vector2 import Vector2

class Arrow():
    SIZE = 0.032
    def __init__(self, canvas, name):
        self._main_line = None
        self._edge1 = None
        self._edge2 = None
        self._name_wigdget = None
        self._canvas = canvas
        self._name = name
        self._name.add_listener("update", self._set_text_value)

    def create_visuals(self, start_point, end_point, text_angle, text_anchor):
        """ doc """
        canvas = self._canvas
        min_point = start_point.get()
        max_point = end_point.get()
        # draw main line
        self._main_line = self._canvas.create_line(min_point + max_point, tag="axis", fill="RED")
        self._name_wigdget = canvas.create_text(max_point, text=self._name.get(),
                                                anchor=text_anchor, angle=text_angle,
                                                tag="axis")

        start_end = Vector2.sub(max_point, min_point)
        scale = Vector2.len(start_end)
        direction = Vector2.normalize(start_end)
        direction1 = Vector2.rotate(direction, 135)
        direction2 = Vector2.rotate(direction, -135)
        # Draw the sides of the arrow
        end_point = Vector2.add(max_point, Vector2.mul(direction1, scale * Arrow.SIZE))
        self._edge1 = canvas.create_line(max_point[0], max_point[1], end_point[0],
                                         end_point[1], tag="axis", fill="RED")

        end_point = Vector2.add(max_point, Vector2.mul(direction2, scale * Arrow.SIZE))
        self._edge2 = canvas.create_line(max_point[0], max_point[1], end_point[0],
                                         end_point[1], tag="axis", fill="RED")
    def remove_visuals(self):
        self._canvas.delete(self._edge1)
        self._canvas.delete(self._edge2)
        self._canvas.delete(self._main_line)
        self._canvas.delete(self._name_wigdget)
        self._edge1 = None
        self._edge2 = None
        self._main_line = None
        self._name_wigdget = None

    def _set_text_value(self, _):
        if self._name_wigdget != None:
            self._canvas.itemconfig(self._name_wigdget, text=self._name.get())
