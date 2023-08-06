# -*- coding: utf-8 -*-

import math


class Transform(object):

    def __init__(self, params):
        # Public, to allow user access
        self.params = params

    def a(self):
        return self.params[0]
    def b(self):
        return self.params[1]
    def c(self):
        return self.params[2]
    def d(self):
        return self.params[3]
    def p(self):
        return self.params[4]
    def q(self):
        return self.params[5]

    def transform(self, points):
        '''
        Parameter
            p
                point [x, y] or list of points [[x1,y1], [x2,y2], ...]
        '''
        def transform_one(point):
            return [self.params[0] * point[0] + self.params[1] * point[1] + self.params[4],
                    self.params[2] * point[0] + self.params[3] * point[1] + self.params[5]]

        if not isinstance(points[0], list):
            # Single point
            return transform_one(points)
        # else
        return list(map(transform_one, points))

    def transform_inv(self, points):
        '''
        Parameter
            p
                point [x, y] or list of points [[x1,y1], [x2,y2], ...]
        '''
        def transform_inv_one(point):
            det = self.params[0] * self.params[3] - \
                self.params[2] * self.params[1]
            return [(self.params[3] * (point[0] - self.params[4]) - self.params[1] * (point[1] - self.params[5])) / det,
                    (self.params[2] * (point[0] - self.params[4]) - self.params[0] * (point[1] - self.params[5])) / det * -1.0]

        if not isinstance(points[0], list):
            # Single point
            return transform_inv_one(points)
        # else
        return list(map(transform_inv_one, points))

    def get_matrix(self):
        return [[self.params[0], self.params[1], self.params[4]],
                [self.params[2], self.params[3], self.params[5]],
                [0,              0,              1]]

    def get_rotation_x(self):
        return math.atan2(-self.params[1], self.params[0])

    def get_rotation_y(self):
        return math.atan2(self.params[2], self.params[3])

    def get_scale_x(self):
        return math.sqrt(self.params[0] * self.params[0] + self.params[1] * self.params[1])

    def get_scale_y(self):
        return math.sqrt(self.params[2] * self.params[2] + self.params[3] * self.params[3])

    def get_scale(self):
        summed = self.get_scale_x() * self.get_scale_x() + \
            self.get_scale_y() * self.get_scale_y()
        return math.sqrt(summed * 0.5)

    def get_translation(self):
        return [self.params[4], self.params[5]]
