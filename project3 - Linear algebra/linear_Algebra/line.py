from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term

            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)

            initial_coefficient = n.coordinates[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def linesAreParallel(self, other):
        return self.normal_vector.isParallel(other.normal_vector)

    def __eq__(self,other):
        if self.normal_vector.isZero():
            if not other.normal_vector.isZero():
                return False
            else:
                diff =self.constant_term - other.constant_term
                return MyDecimal(diff).is_near_zero()
        elif other.normal_vector.isZero():
            return False

        if not self.linesAreParallel(other):
            return False

        b1 = self.basepoint
        b2 = other.basepoint

        v = b1.minus(b2)
        n = self.normal_vector   #2 lines have already parallel, no need to compare to normal vector to v

        return n.isOrthogonal(v)


    def intersectionIs(self, other):

        try:
            n1 = self.normal_vector
            k1 = self.constant_term
            A,B = n1.coordinates

            n2 = other.normal_vector
            k2 = other.constant_term
            C,D = n2.coordinates


            x = D*k1 - B*k2
            y = A*k2 - C*k1

            return Vector([x,y]).times(Decimal('1')/(A*D - B*C))

        except ZeroDivisionError:
            if self == other:
                return self
            else:
                return None

    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n.coordinates[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n.coordinates[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)



class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


l1 = Line(normal_vector = Vector(['4.046','2.836']),constant_term = '1.21')
l2 = Line(normal_vector = Vector(['10.115','7.09']),constant_term = '3.025')
l3 = Line(normal_vector = Vector(['7.204','3.182']),constant_term = '8.68')
l4 = Line(normal_vector = Vector(['8.172','4.114']),constant_term = '9.883')
l5 = Line(normal_vector = Vector(['1.182','5.562']),constant_term = '6.744')
l6 = Line(normal_vector = Vector(['1.773','8.343']),constant_term = '9.525')


print'--l1 vs l2--'
print l1.linesAreParallel(l2)
print l1.__eq__(l2)
print l1.intersectionIs(l2)

print'--l3 vs l4--'
print l3.linesAreParallel(l4)
print l3.__eq__(l4)
print l3.intersectionIs(l4)

print'--l5 vs l6--'
print l5.linesAreParallel(l6)
print l5.__eq__(l6)
print l5.intersectionIs(l6)