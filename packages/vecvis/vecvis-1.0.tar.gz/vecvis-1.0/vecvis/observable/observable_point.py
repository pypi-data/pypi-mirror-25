'''
Created on 24.07.2017

@author: Mo
'''
from vecvis.utils.emitter import Emitter


class ObservableVector2(Emitter):

    def __init__(self, point):
        super().__init__()
        self._point = point

    def set(self, point):
        if self._point[0] != point[0] or self._point[1] != point[1]:
            old_value = [self._point[0], self._point[1]]
            if abs(point[0]) < 0.00001:
                point[0] = 0
            if abs(point[1]) < 0.00001:
                point[1] = 0
            new_value = [point[0], point[1]]
            self._point = [new_value[0], new_value[1]]
            self._emit("update", (self, old_value, new_value))

    def get(self):
        return [self._point[0], self._point[1]]
