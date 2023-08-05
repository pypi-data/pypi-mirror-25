'''
Created on 24.07.2017

@author: Mo
'''
import math


class Vector2:
    @staticmethod
    def normalize(point):
        thelen = Vector2.len(point)
        return [point[0] / thelen, point[1] / thelen]

    @staticmethod
    def len(point):
        return math.sqrt(point[0] * point[0] + point[1] * point[1])

    @staticmethod
    def angle_to_vec(angle):
        return [math.cos(math.radians(
            angle)), math.sin(math.radians(angle))]

    @staticmethod
    def sub(vec_a, vec_b):
        """ returns a - b """
        return [vec_a[0] - vec_b[0], vec_a[1] - vec_b[1]]

    @staticmethod
    def add(vec_a, vec_b):
        """ returns a + b """
        return [vec_a[0] + vec_b[0], vec_a[1] + vec_b[1]]

    @staticmethod
    def rotate(vec, degree):
        """ rotates vec by degree """
        result = [0, 0]
        result[0] = vec[0] * math.cos(math.radians(degree)) - \
            vec[1] * math.sin(math.radians(degree))
        result[1] = vec[0] * math.sin(math.radians(degree)) + \
            vec[1] * math.cos(math.radians(degree))
        return result

    @staticmethod
    def dot(vec_a, vec_b):
        """ return the dotproduct between a and b """
        return vec_a[0] * vec_b[0] + vec_a[1] * vec_b[1]

    @staticmethod
    def mul(vec_a, amount):
        """ returns vec_a * amount """
        return [vec_a[0] * amount, vec_a[1] * amount]
