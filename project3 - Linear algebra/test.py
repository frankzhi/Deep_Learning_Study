
from math import sqrt, pi, acos
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):
    def __init__(self, coordinates):
        """ Create a vector, example: v = Vector(1,2) """
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)
        #self.values = coordinates
        except ValueError:
            raise ValueError('Cannot normalise zero vector')


    def plus(self,other):
        new_coordinates = [x + y for x,y in zip(self.coordinates, other.coordinates)]
        return Vector(new_coordinates)

    def minus(self, other):
        new_coordinates = [x-y for x,y in zip(self.coordinates, other.coordinates)]
        return Vector(new_coordinates)

    def times(self,c):
        new_coordinates = [x*Decimal(c) for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):

        v = [x**2 for x in self.coordinates]
        return Decimal.sqrt(sum(v))

    def normalisation(self):
        try:
            magnitude = self.magnitude()
            return self.times(Decimal(1.0)/magnitude)

        except ZeroDivisionError:
            raise Exception('Cannot normalise zero vector')

    def dot(self,other):
        inner_product = [x*y for x,y in zip(self.coordinates, other.coordinates)]
        return sum(inner_product)

    def angle(self,other,isRad = True):
        try:
            self_norm = self.normalisation()
            other_norm = other.normalisation()
            angle_in_radians = acos(self_norm.dot(other_norm))

            # dot = self.dot(other)
            # self_magnitude = self.magnitude()
            # other_magnitude = other.magnitude()
            # rad = acos(dot/(self_magnitude*other_magnitude))
            if isRad:
                return angle_in_radians
            else:
                return angle_in_radians* 180./pi

        except ValueError:
            print "error"

    def __iter__(self):
        return self.coordinates.__iter__()

    def __eq__(self,other):
        return self.coordinates ==other.coordinates

    def __repr__(self):
        return 'Vector: {}'.format(self.coordinates)

# v = Vector(1,2,-1)
# w = Vector(3,1,0)
# x = Vector(5,-3)
# y = Vector(0.221,7.437)
# z = Vector(8.813,-1.331,-6.247)
# a = Vector(5.581,-2.136)
# b = Vector(0,0,0)

x1 = Vector(['7.35','0.221','5.188'])
x2 = Vector(['2.751','8.259','3.985'])

print x1.plus(x2)
print x1.times(10.0)
print x1.dot(x2)
print x1.normalisation()
# print v.plus(w)
# print v.minus(x)
# print v.times(10)
# print y.magnitude()
# print z.magnitude()
# print b.normalisation()
# # print b.normalisation()
# print v.dot(v)
print x1.angle(x2,False)
