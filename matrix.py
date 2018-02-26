from __future__ import division

from math import sin, cos, tan

from vector import Vector


__author__ = 'gua'


class Matrix(object):
    def __init__(self, matrix_list=None):
        if matrix_list is not None:
            self.m = matrix_list
        else:
            self.m = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]

    def __getitem__(self, item):
        """
        :type item: tuple
        """
        i, j = item
        return self.m[i][j]

    def __setitem__(self, key, value):
        """
        :type key: tuple
        """
        i, j = key
        self.m[i][j] = value

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        s = ''.join(['{0:.3f}'.format(self[i // 4, i % 4]) + ('\n' if i % 4 == 3 else ' ')
                    for i in range(16)])
        return s

    def __mul__(self, other):
        m1 = self
        m2 = other
        m = Matrix()

        for index in range(16):
            i = index // 4
            j = index % 4
            m[i, j] = m1[i, 0] * m2[0, j] + m1[i, 1] * m2[1, j] + m1[i, 2] * m2[2, j] + m1[i, 3] * m2[3, j]
            # m[i, j] = sum([m1[i, x] * m2[x, j] for x in range(4)])

        return m

    @staticmethod
    def zero():
        return Matrix()

    @staticmethod
    def identity():
        m = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        return Matrix(m)

    @staticmethod
    def lookAtLH(eye, target, up):
        """
        Builds a left-handed look-at matrix.

        :type eye: Vector
        :type target: Vector
        :type up: Vector

        :rtype : Matrix
        """
        zaxis = (target - eye).normalize()
        xaxis = up.cross(zaxis).normalize()
        yaxis = zaxis.cross(xaxis).normalize()

        ex = -xaxis.dot(eye)
        ey = -yaxis.dot(eye)
        ez = -zaxis.dot(eye)

        m = [
            [xaxis.x, yaxis.x, zaxis.x, 0],
            [xaxis.y, yaxis.y, zaxis.y, 0],
            [xaxis.z, yaxis.z, zaxis.z, 0],
            [ex, ey, ez, 1]
        ]
        return Matrix(m)

    @staticmethod
    def perspectiveFovLH(field_of_view, aspect, znear, zfar):
        """
        Builds a left-handed perspective projection matrix based on a field of view.

        :type field_of_view: float
        :type aspect: float
        :type znear: float
        :type zfar: float

        :rtype: Matrix
        """
        h = 1 / tan(field_of_view / 2)
        w = h / aspect
        m = [
            [w, 0, 0, 0],
            [0, h, 0, 0],
            [0, 0, zfar / (zfar - znear), 1],
            [0, 0, (znear * zfar) / (znear - zfar), 0],
        ]
        return Matrix(m)

    @staticmethod
    def rotationX(angle):
        s = sin(angle)
        c = cos(angle)
        m = [
            [1, 0,  0, 0],
            [0, c,  s, 0],
            [0, -s, c, 0],
            [0, 0,  0, 1],
        ]
        return Matrix(m)

    @staticmethod
    def rotationY(angle):
        s = sin(angle)
        c = cos(angle)
        m = [
            [c, 0, -s, 0],
            [0, 1, 0,  0],
            [s, 0, c,  0],
            [0, 0, 0,  1],
        ]
        return Matrix(m)

    @staticmethod
    def rotationZ(angle):
        s = sin(angle)
        c = cos(angle)
        m = [
            [c,  s, 0, 0],
            [-s, c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1],
        ]
        return Matrix(m)

    @staticmethod
    def rotation(angle):
        matrix = Matrix.rotationZ(angle.z) * Matrix.rotationX(angle.x) * Matrix.rotationY(angle.y)
        return matrix

    @staticmethod
    def translation(vector):
        v = vector
        x, y, z = v.x, v.y, v.z
        m = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1],
        ]

        return Matrix(m)

    def transformVector(self, vector):
        v = vector
        m = self
        x = v.x * m[0, 0] + v.y * m[1, 0] + v.z * m[2, 0] + m[3, 0]
        y = v.x * m[0, 1] + v.y * m[1, 1] + v.z * m[2, 1] + m[3, 1]
        z = v.x * m[0, 2] + v.y * m[1, 2] + v.z * m[2, 2] + m[3, 2]
        w = v.x * m[0, 3] + v.y * m[1, 3] + v.z * m[2, 3] + m[3, 3]

        return Vector(x / w, y / w, z / w)


class Vector(object):
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        l = self.length()
        if l == 0:
            return self
        factor = 1 / l

        return self * factor

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        x = self.y * v.z - self.z * v.y
        y = self.z * v.x - self.x * v.z
        z = self.x * v.y - self.y * v.x
        return Vector(x, y, z)
