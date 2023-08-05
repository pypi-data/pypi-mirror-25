'''
'''

from vecvis.utils.vector2 import Vector2


class FilterWidget():
    """ doc
    """
    SIZE = 0.01

    def __init__(self, min_point, max_point, min_value, max_value, value, value_cap, reverse, canvas):
        self._min_point = min_point
        self._max_point = max_point
        self._min_value = min_value
        self._min_value.add_listener("update", self._on_min_value_changed)
        self._max_value = max_value
        self._max_value.add_listener("update", self._on_max_value_changed)
        self._value_cap = value_cap
        self._value = value
        self._value.add_listener("update", self._on_value_changed)
        self._reverse = reverse
        self._current_value = self._value.get()
        self._widget = None
        self._canvas = canvas

    def create_visuals(self):
        """doc
        """
        canvas = self._canvas
        min_point = self._min_point.get()
        max_point = self._max_point.get()
        start_end = Vector2.sub(max_point, min_point)
        direction = Vector2.normalize(start_end)
        scale = len(start_end)
        direction2 = Vector2.rotate(direction, 90)

        # 0 - 1 * axis is the point where to draw
        nlen = (self._value.get() - self._min_value.get()) / \
            (self._max_value.get() - self._min_value.get())
        modif = 1
        if self._reverse:
            modif *= -1

        # startpoint
        start = Vector2.add(min_point, Vector2.mul(start_end, nlen))
        # from startpoint in direction
        end = Vector2.add(start, Vector2.mul(
            direction, scale * FilterWidget.SIZE * modif))
        mkr = canvas.create_polygon([start[0], start[1],
                                     end[0] + direction2[0] *
                                     scale * FilterWidget.SIZE,
                                     end[1] + direction2[1] *
                                     scale * FilterWidget.SIZE,
                                     end[0] - direction2[0] *
                                     scale * FilterWidget.SIZE,
                                     end[1] - direction2[1] * scale * FilterWidget.SIZE],
                                    fill="GREEN", outline="#40d412",
                                    tag="filter_marker")
        self._widget = mkr
        canvas.tag_bind(mkr, "<B1-Motion>", self._on_drag)
        canvas.tag_bind(mkr, "<Button-1>", self._on_click)
        canvas.tag_bind(mkr, "<ButtonRelease-1>", self._on_release)

    def remove_visuals(self):
        """ doc """
        canvas = self._canvas
        canvas.delete(self._widget)

    def _on_drag(self, event):
        # Aquire some infos
        vec_start_end = Vector2.sub(
            self._max_point.get(), self._min_point.get())
        len_vec_start_end_px = Vector2.len(vec_start_end)

        # Where are we atm?
        len_current_normalized = (self._current_value - self._min_value.get()) / \
            (self._max_value.get() - self._min_value.get())
        old_point = Vector2.add(self._min_point.get(), Vector2.mul(
            vec_start_end, len_current_normalized))

        # Where is the mouse?
        vec_direction = Vector2.normalize(vec_start_end)
        vec_start_mouse = Vector2.sub(
            [event.x, event.y], self._min_point.get())

        # At which value do we want to be?
        len_projection_px = Vector2.dot(vec_direction, vec_start_mouse)

        new_value = (self._max_value.get() - self._min_value.get()
                     ) * (len_projection_px / len_vec_start_end_px) + self._min_value.get()

        # Is the new value valid?
        if not self._reverse:
            if new_value < self._min_value.get():
                new_value = self._min_value.get()
            if new_value > self._value_cap.get():
                new_value = self._value_cap.get()
        else:
            if new_value > self._max_value.get():
                new_value = self._max_value.get()
            if new_value < self._value_cap.get():
                new_value = self._value_cap.get()

        # What is the new point
        new_len_normalized = (new_value - self._min_value.get()) / \
            (self._max_value.get() - self._min_value.get())

        new_point = Vector2.add(self._min_point.get(),
                                Vector2.mul(vec_start_end, new_len_normalized))
        change = Vector2.sub(new_point, old_point)

        # Move to the new point
        self._current_value = new_value
        self._canvas.move(self._widget, change[0], change[1])

    def _on_click(self, _):
        self._current_value = self._value.get()
        self._canvas.tag_raise(self._widget)

    def _on_release(self, _):
        self._value.set(self._current_value)

    def _on_value_changed(self, event):
        _, old, new = event
        if new == self._current_value:
            return
        len_current_normalized = (old - self._min_value.get()) / \
            (self._max_value.get() - self._min_value.get())

        vec_start_end = Vector2.sub(
            self._max_point.get(), self._min_point.get())
        old_point = Vector2.add(self._min_point.get(), Vector2.mul(
            vec_start_end, len_current_normalized))
        len_new_normalized = (new - self._min_value.get()) / \
            (self._max_value.get() - self._min_value.get())
        new_point = Vector2.add(self._min_point.get(), Vector2.mul(
            vec_start_end, len_new_normalized))
        change = Vector2.sub(new_point, old_point)
        self._canvas.move(self._widget, change[0], change[1])
        self._current_value = new

    def _on_min_value_changed(self, event):
        _, old, new = event

        len_current_normalized = (self._current_value - old) / \
            (self._max_value.get() - old)

        vec_start_end = Vector2.sub(
            self._max_point.get(), self._min_point.get())
        old_point = Vector2.add(self._min_point.get(), Vector2.mul(
            vec_start_end, len_current_normalized))
        if self._current_value < new:
            self._current_value = new
        len_new_normalized = (self._current_value - self._min_value.get()) / \
            (self._max_value.get() - self._min_value.get())
        new_point = Vector2.add(self._min_point.get(), Vector2.mul(
            vec_start_end, len_new_normalized))
        change = Vector2.sub(new_point, old_point)
        self._canvas.move(self._widget, change[0], change[1])
        self._value.set(self._current_value)

    def _on_max_value_changed(self, event):
        _, old, new = event

        len_current_normalized = (self._current_value - self._min_value.get()) / \
            (old - self._min_value.get())

        vec_start_end = Vector2.sub(
            self._max_point.get(), self._min_point.get())
        old_point = Vector2.add(self._min_point.get(), Vector2.mul(
            vec_start_end, len_current_normalized))
        if self._current_value > new:
            self._current_value = new
        len_new_normalized = (self._current_value - self._min_value.get()) / \
            (self._max_value.get() - self._min_value.get())
        new_point = Vector2.add(self._min_point.get(), Vector2.mul(
            vec_start_end, len_new_normalized))
        change = Vector2.sub(new_point, old_point)
        self._canvas.move(self._widget, change[0], change[1])
        self._value.set(self._current_value)
