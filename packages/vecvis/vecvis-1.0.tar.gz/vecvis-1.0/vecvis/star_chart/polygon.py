""" doc
"""
class Polygon():
    def __init__(self, axes, canvas, color, vector):
        self._axes = axes
        self._canvas = canvas
        self._color = color
        self._vector = vector
        self._polygon = None

    def create_visuals(self):
        points = []
        for i in range(len(self._axes)):
            points = points + self._axes[i].value_to_point(self._vector[i])
        self._polygon = self._canvas.create_polygon(points, outline=self._color,
                                                    fill="", tag="polygon")

    def remove_visuals(self):
        self._canvas.delete(self._polygon)
        self._polygon = None

    def set_color(self, color):
        self._color = color
        if self._polygon is None:
            return
        self._canvas.itemconfig(self._polygon, outline=self._color)

    def tag_raise(self):
        self._canvas.tag_raise(self._polygon)
