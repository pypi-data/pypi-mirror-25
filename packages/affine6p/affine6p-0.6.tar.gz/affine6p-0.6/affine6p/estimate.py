# -*- coding: utf-8 -*-
import math
from .transform import Transform


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

    if N >= 3:
        return estimate_full(origin, convrt)
    elif N == 2:
        return estimate_helmert(origin, convrt)
    elif N == 1:
        return Transform([1.0, 0.0, 0.0, 1.0, convrt[0][0] - origin[0][0], convrt[0][1] - origin[0][1]])
    else:
        raise ValueError


def estimate_full(origin, convrt):
    '''
    Parameters
        origin
            list of [x, y] 2D lists
        convrt
            list of [x, y] 2D lists
    '''
    N = min(len(origin), len(convrt))

    mat00 = mat11 = mat22 = mat01 = mat10 = mat02 = mat20 = mat12 = mat21 = 0.0
    vec0 = vec1 = vec2 = vec3 = vec4 = vec5 = 0.0

    for i in range(N):
        ox = origin[i][0]
        oy = origin[i][1]
        cx = convrt[i][0]
        cy = convrt[i][1]

        mat00 += ox * ox
        mat01 += ox * oy
        mat02 += ox
        mat10 += ox * oy
        mat11 += oy * oy
        mat12 += oy
        mat20 += ox
        mat21 += oy
        mat22 += 1

        vec0 += ox * cx
        vec1 += oy * cx
        vec2 += cx
        vec3 += ox * cy
        vec4 += oy * cy
        vec5 += cy

    # Determinant of mat
    det = 0.0
    det += (mat00 * mat11 * mat22 + mat10 * mat21 * mat02 + mat20 * mat01 * mat12)
    det -= (mat00 * mat21 * mat12 + mat20 * mat11 * mat02 + mat10 * mat01 * mat22)

    params = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

    if abs(det) < 1e-8:
        raise ZeroDivisionError("Value of determinant is almost zero.")

    inv_det = 1.0 / det

    inv_mat00 = inv_det * (mat11 * mat22 - mat12 * mat21)
    inv_mat01 = inv_det * (mat12 * mat20 - mat10 * mat22)
    inv_mat02 = inv_det * (mat10 * mat21 - mat11 * mat20)
    inv_mat10 = inv_mat01
    inv_mat11 = inv_det * (mat22 * mat00 - mat20 * mat02)
    inv_mat12 = inv_det * (mat20 * mat01 - mat21 * mat00)
    inv_mat20 = inv_mat02
    inv_mat21 = inv_mat12
    inv_mat22 = inv_det * (mat00 * mat11 - mat01 * mat10)

    # Estimators
    params[0] = inv_mat00 * vec0 + inv_mat01 * vec1 + inv_mat02 * vec2
    params[1] = inv_mat10 * vec0 + inv_mat11 * vec1 + inv_mat12 * vec2
    params[2] = inv_mat00 * vec3 + inv_mat01 * vec4 + inv_mat02 * vec5
    params[3] = inv_mat10 * vec3 + inv_mat11 * vec4 + inv_mat12 * vec5
    params[4] = inv_mat20 * vec0 + inv_mat21 * vec1 + inv_mat22 * vec2
    params[5] = inv_mat20 * vec3 + inv_mat21 * vec4 + inv_mat22 * vec5

    return Transform(params)


def estimate_helmert(origin, convrt):
    '''
    Parameters
        origin
            list of [x, y] 2D lists
        convrt
            list of [x, y] 2D lists
    '''
    N = min(len(origin), len(convrt))

    x0 = x1 = y0 = y1 = x02 = y02 = x0x1 = y0y1 = y0x1 = x0y1 = 0.0

    for i in range(N):
        ox = origin[i][0]
        oy = origin[i][1]
        cx = convrt[i][0]
        cy = convrt[i][1]

        x0 += ox
        y0 += oy
        x1 += cx
        y1 += cy

        x02 += ox * ox
        y02 += oy * oy
        x0x1 += ox * cx
        x0y1 += ox * cy
        y0x1 += oy * cx
        y0y1 += oy * cy

    det = x0 * x0 + y0 * y0 - N * (x02 + y02)

    if abs(det) < 1e-8:
        raise ZeroDivisionError("Value of determinant is almost zero.")

    inv_det = 1.0 / det

    # Estimators
    params = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    params[0] = (x0 * x1 + y0 * y1 - N * (x0x1 + y0y1)) * inv_det
    params[1] = (y0 * x1 - x0 * y1 - N * (y0x1 - x0y1)) * inv_det
    params[2] = -params[1]
    params[3] = params[0]
    params[4] = (x1 - params[0] * x0 - params[1] * y0) / N 
    params[5] = (y1 - params[0] * y0 + params[1] * x0) / N

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

    origin2 = transform.transform(origin)
    convrt2 = convrt

    # Allow arrays of different length but
    # ignore the extra points.
    N = min(len(origin2), len(convrt2))

    se = 0.0
    for i in range(N):
        ox = origin2[i][0]
        oy = origin2[i][1]
        cx = convrt2[i][0]
        cy = convrt2[i][1]

        dx = ox - cx
        dy = oy - cy

        se += dx * dx + dy * dy

    if N == 0:
        return 0
    else:
        return math.sqrt(se / N)
