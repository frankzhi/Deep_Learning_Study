
from math import sqrt, pi, acos,sin
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

    def isZero(self, tolerance = 1e-10):
        return self.magnitude() < tolerance

    def isOrthogonal(self, other, tolerance = 1e-10):
        return abs(self.dot(other)) <tolerance

    def isParallel(self, other):
        if self.isZero() or other.isZero():
            return True
        elif self.angle(other) == 0 or self.angle(other) == pi:
            return True
        else:
            return False

    def projVector(self,basis):
        try:
            ub = basis.normalisation()
            lenth_of_self = self.dot(ub)
            return ub.times(lenth_of_self)
        except Exception as e:
            if str(e) == 'Cannot normalise zero vector':
                raise Exception('No unique parallel component')
            else:
                raise e

    def orthVector(self,basis):
        try:
            projV = self.projVector(basis)
            return self.minus(projV)

        except Exception as e:
            if str(e) == 'No unique parallel component':
                raise Exception('No unique orthogonal component')
            else:
                raise e


    def crossProduct(self,other):
        try:
            x1,y1,z1 = self.coordinates
            x2,y2,z2 = other.coordinates
            new_coordinates = [y1*z2 - y2*z1, x2*z1-x1*z2, x1*y2 - x2*y1]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            if msg =='need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates +('0',))
                other_embedded_in_R3 = Vector(other.coordinates+('0',))
                return self_embedded_in_R3.crossProduct(other_embedded_in_R3)
            elif msg =='need more than 1 value to unpack' or msg =='too many values to unpack':
                raise Exception('There should be two 3-dimension vectors')
            else:
                raise e

    def parallelogram(self,other):
        '''len_of_v = self.magnitude()
        len_of_w = other.magnitude()
        angle = self.angle(other)
        return len_of_v*len_of_w*Decimal(sin(angle))'''

        crossProduct = self.crossProduct(other)
        return crossProduct.magnitude()

    def triangle(self,other):
        return Decimal('0.5')* self.parallelogram(other)

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

v1 = Vector(['-7.579','-7.88'])
w1 = Vector(['22.737','23.64'])

v2 = Vector(['-2.029','9.97','4.172'])
w2 = Vector(['-9.231','-6.639','-7.245'])

v3 = Vector(['-2.328','-7.284','-1.214'])
w3 = Vector(['-1.821','1.072','-2.94'])

v4 = Vector(['2.118','4.827'])
w4 = Vector(['0','0'])

v5 = Vector(['3.039','1.879'])
w5 = Vector(['0.825','2.036'])

v6 = Vector(['-9.88','-3.264','-8.159'])
w6 = Vector(['-2.155','-9.353','-9.473'])

v7 = Vector(['3.009','-6.172','3.692','-2.51'])
w7 = Vector(['6.404','-9.144','2.759','8.718'])

v8 = Vector(['8.462','7.893','-8.187'])
w8 = Vector(['6.984','-5.975','4.778'])

v9 = Vector(['-8.987','-9.838','5.031'])
w9 = Vector(['-4.268','-1.861','-8.866'])

v10 = Vector(['1.5','9.547','3.691'])
w10 = Vector(['-6.007','0.124','5.772'])

vi = Vector(['8.462','7.893','-8.187'])
wi = Vector(['0','0','0'])

t1 = Vector(['1'])
tt1 = Vector(['2'])

t2 = Vector(['1','2'])
tt2 = Vector(['5','3'])

t3 = Vector(['1','1','2','-4'])
tt3 = Vector(['5','-2','-1','0'])


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

print v1.isParallel(w1)
print v1.isOrthogonal(w1)

print v2.isParallel(w2)
print v2.isOrthogonal(w2)

print v3.isParallel(w3)
print v3.isOrthogonal(w3)

print v4.isParallel(w4)
print v4.isOrthogonal(w4)

print v5.projVector(w5)

print v6.orthVector(w6)

print '----test----'
# print t1.crossProduct(tt1)
print t2.crossProduct(tt2)
# print t3.crossProduct(tt3)
print '----test----'
print v8.crossProduct(w8)
print v9.parallelogram(w9)
print v10.triangle(w10)
