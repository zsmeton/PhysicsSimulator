# python import based off of PVector library
# source: http://natureofcode.com/

import math


class Vector:
    def __init__(self, x_=0, y_=0, z_=0):
        self.x = x_
        self.y = y_
        self.z = z_

    def __str__(self):
        if self.z == 0:
            return '%f,%f' % (self.x, self.y)
        elif self.x == 0:
            return '%f,%f' % (self.y, self.z)
        elif self.y == 0:
            return '%f,%f' % (self.x, self.z)
        else:
            return '%f,%f,%f' % (self.x, self.y, self.z)

    # method: sets vector values
    def set(self, x_=0, y_=0, z_=0):
        self.x = x_
        self.y = y_
        self.z = z_

    # method: sets vector value using another vector sadly no multi-processing
    def set_vect(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    # sets vector based on angle
    # ex: from_angle(angle, vector)
    @staticmethod
    def from_angle(angle, target=None):
        if target is None:
            target = Vector(math.cos(angle), math.sin(angle))
        else:
            target.set = Vector(math.cos(angle), math.sin(angle))
        return target

    # static: copies vector to new vector
    def copy(self):
        return Vector(self.x, self.y, self.z)

    # static : magnitude of vector
    # ex: magnitude = self.mag()
    def mag(self):
        mag = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return mag

    # static : magnitude of vector squared
    # ex: magnitude = self.magSq()
    def mag_sq(self):
        mag_squared = self.mag() ** 2
        return mag_squared

    # method: vector addition
    # ex: self.add(vector)
    def add(self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y
        self.z = self.z + v.z

    # static: vector addition
    # ex: vector = self + vect
    def __add__(self, other):
        vector_ = Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        return vector_

    # method: vector subtraction
    # ex: self.sub(vector)
    def sub(self, v):
        self.x = self.x - v.x
        self.y = self.y - v.y
        self.z = self.z - v.z

    # static: vector subtraction
    # ex: vector = self - vect
    def __sub__(self, other):
        vector_ = Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        return vector_

    # method : scalar multiplication
    # ex: self.mult(n)
    def mult(self, n):
        self.x = self.x * n
        self.y = self.y * n
        self.z = self.z * n

    # static : scalar multiplication
    # ex: vector = self * n
    def __mul__(self, other):
        vector_ = Vector(self.x * other, self.y * other, self.z * other)
        return vector_

    # method : scalar division
    # ex: self.div(n)
    def div(self, n):
        if n != 0:
            self.x = self.x / n
            self.y = self.y / n
            self.z = self.z / n

    # static : scalar division
    # ex: vector = self / n
    def __truediv__(self, other):
        vector_ = Vector(self.x / other, self.y / other, self.z / other)
        return vector_

    # static: finds distance between two points
    def dist(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        return dist

    # static : dot product
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    # static/method : cross product
    def cross(self, other):
        cross_x = self.y * other.z - other.y * self.z
        cross_y = self.z * other.x - other.z * self.x
        cross_z = self.x * other.y - other.x * self.y
        self.set(cross_x, cross_y, cross_z)

    # method : normalize
    def normalize(self):
        denominator = self.mag()
        if denominator is not 0 or 1:
            self.div(denominator)

    # method : set limit
    def limit(self, limitation):
        if self.mag_sq() > limitation * limitation:
            self.set_mag(limitation)

    # method : set magnitude of vector
    def set_mag(self, magnitude):
        self.normalize()
        self.mult(magnitude)

    # find angle of rotation for 2D vector
    def heading(self):
        angle = math.atan2(self.y, self.x)
        return angle

    # method : rotates vector by an angle
    def rotate(self, angle):
        x_ = self.x
        self.x = self.x * math.cos(math.radians(angle)) - self.y * math.sin(math.radians(angle))
        self.y = x_ * math.sin(math.radians(angle)) + self.y * math.cos(math.radians(angle))

    # static : finds the angle between two vectors
    @staticmethod
    def angle_between(v1, v2):
        if v1.x == 0 and v1.y == 0 and v1.z == 0:
            return float(0)
        if v2.x == 0 and v2.y == 0 and v2.z == 0:
            return float(0)
        dot = v1.dot(v2)
        v1mag = v1.mag()
        v2mag = v2.mag()
        amount = dot / (v1mag * v2mag)
        if amount <= -1:
            return math.pi
        elif amount >= 1:
            return 0
        else:
            return math.acos(amount)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
