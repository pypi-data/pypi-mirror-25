# -*- coding: utf-8 -*-
import math

class Transform(object):

    def __init__(self, params):
        # Public, to allow user access
        self.params = params

    def transform(self, p):
        '''
        Parameter
            p
                point [x, y] or list of points [[x1,y1], [x2,y2], ...]
        '''
        def transform_one(q):
            return [self.params[0] * q[0] + self.params[1] * q[1] + self.params[4],
                    self.params[2] * q[0] + self.params[3] * q[1] + self.params[5]]

        if not isinstance(p[0], list):
            # Single point
            return transform_one(p)
        # else
        return list(map(transform_one, p))

    def transform_inv(self, p):
        '''
        Parameter
            p
                point [x, y] or list of points [[x1,y1], [x2,y2], ...]
        '''
        def transform_inv_one(q):
            det = self.params[0] * self.params[3] - self.params[2] * self.params[1]
            return [(self.params[3] * (q[0] - self.params[4]) - self.params[1] * (q[1] - self.params[5])) / det,
                    (self.params[2] * (q[0] - self.params[4]) - self.params[0] * (q[1] - self.params[5])) / det * -1.0]

        if not isinstance(p[0], list):
            # Single point
            return transform_inv_one(p)
        # else
        return list(map(transform_inv_one, p))

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
        summed = self.get_scale_x() * self.get_scale_x() + self.get_scale_y() * self.get_scale_y()
        return math.sqrt(summed * 0.5)

    def get_translation(self):
        return [self.params[4], self.params[5]]


def estimate(origin, convrt):
    '''
    Parameters
        origin
            list of [x, y] 2D lists
        convrt
            list of [x, y] 2D lists
    '''

    # Allow arrays of different length but
    # ignore the extra points.
    N = min(len(origin), len(convrt))

    mat00 = mat11 = mat22 = mat01 = mat10 = mat02 = mat20 = mat12 = mat21 = 0.0
    vec0 = vec1 = vec2 = vec3 = vec4 = vec5 = 0.0

    for i in range(N):
        mat00 += origin[i][0] * origin[i][0]
        mat11 += origin[i][1] * origin[i][1]
        mat22 += 1
        mat01 += origin[i][0] * origin[i][1]
        mat10 += origin[i][0] * origin[i][1]
        mat02 += origin[i][0]
        mat20 += origin[i][0]
        mat12 += origin[i][1]
        mat21 += origin[i][1]

        vec0 += origin[i][0] * convrt[i][0]
        vec1 += origin[i][1] * convrt[i][0]
        vec2 += convrt[i][0]
        vec3 += origin[i][0] * convrt[i][1]
        vec4 += origin[i][1] * convrt[i][1]
        vec5 += convrt[i][1]

    inv_det = 0.0
    inv_det += mat00 * mat11 * mat22 + mat10 * mat21 * mat02 + mat20 * mat01 * mat12 
    inv_det +=-mat00 * mat21 * mat12 - mat20 * mat11 * mat02 - mat10 * mat01 * mat22

    params = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

    if abs(inv_det) < 1e-8:
        return Transform(params)

    det = 1.0 / inv_det

    inv_mat00 = det * (mat11 * mat22 - mat12 * mat21)
    inv_mat01 = det * (mat12 * mat20 - mat10 * mat22)
    inv_mat02 = det * (mat10 * mat21 - mat11 * mat20)
    inv_mat11 = det * (mat22 * mat00 - mat20 * mat02)
    inv_mat12 = det * (mat20 * mat01 - mat21 * mat00)
    inv_mat22 = det * (mat00 * mat11 - mat01 * mat10)
    inv_mat10 = inv_mat01
    inv_mat20 = inv_mat02
    inv_mat21 = inv_mat12

    # Estimators
    params[0] = inv_mat00 * vec0 + inv_mat01 * vec1 + inv_mat02 * vec2
    params[1] = inv_mat10 * vec0 + inv_mat11 * vec1 + inv_mat12 * vec2
    params[4] = inv_mat20 * vec0 + inv_mat21 * vec1 + inv_mat22 * vec2
    params[2] = inv_mat00 * vec3 + inv_mat01 * vec4 + inv_mat02 * vec5
    params[3] = inv_mat10 * vec3 + inv_mat11 * vec4 + inv_mat12 * vec5
    params[5] = inv_mat20 * vec3 + inv_mat21 * vec4 + inv_mat22 * vec5

    return Transform(params)


def estimate_error(transform, origin, convrt):
    '''
    Parameters
        transform
            a affine6p.Transform instance
        origin
            list of [x, y] 2D lists
        convrt
            list of [x, y] 2D lists
    '''

    origin = transform.transform(origin)
    convrt = convrt

    # Allow arrays of different length but
    # ignore the extra points.
    N = min(len(origin), len(convrt))

    se = 0.0
    for i in range(N):
        a = origin[i][0]
        b = origin[i][1]
        c = convrt[i][0]
        d = convrt[i][1]

        dx = a - c
        dy = b - d

        se += dx * dx + dy * dy

    if N == 0:
        return 0
    rms = math.sqrt(se / N)
    return rms
