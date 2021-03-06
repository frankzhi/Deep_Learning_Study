from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30




class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def compute_triangular_form(self):
        system = deepcopy(self)

        num_of_rows = len(system)
        num_variables = system.dimension

        variable = 0
        for row in range(num_of_rows) :
            while variable < num_variables:  # in 3 dim v =(0,2)
                c = MyDecimal(system[row].normal_vector.coordinates[variable])
                if c.is_near_zero(): # == {if system[row].normal_vector[variable] == 0}
                    swap_succeeded =system.swap_nonzero_coefficient_row_below(row,variable)
                    if not swap_succeeded:
                        variable +=1
                        continue
                variable +=1
                break

        return system

    def swap_nonzero_coefficient_row_below(self,row,variable):
        num_of_rows = len(self)

        for row_below in range(row+1, num_of_rows):
            coefficient = MyDecimal(self[row_below].normal_vector.coordinates[variable])
            if not coefficient.is_near_zero():   # == {if coefficient != 0}
                self.swap_rows(row, row_below)
                return True
        return False

    def clear_coefficients_below(self, row, variable):
        num_of_rows = len(self)
        x = MyDecimal(self[row].normal_vector.coordinates[variable])

        for row_below in range(row+1, num_of_rows):
            y = self[row_below].normal_vector.coordinates[variable]
            z = - y/x
            self.add_multiple_times_row_to_row(z,row,row_below)

    def swap_rows(self, row1, row2):
        p = self[row1]
        self[row1] = self[row2]
        self[row2] = p
        return self

    def multiply_coefficient_and_row(self, coefficient, row):

        new_normal_vector = self[row].normal_vector.times(coefficient)
        new_constant_term = self[row].constant_term * coefficient
        self[row] = Plane(normal_vector = new_normal_vector, constant_term = new_constant_term)
        return self

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
         normal_vector1 = self[row_to_add].normal_vector.times(coefficient)
         normal_vector2 = self[row_to_be_added_to].normal_vector
         constant_term1 = self[row_to_add].constant_term * coefficient
         constant_term2 = self[row_to_be_added_to].constant_term

         new_normal_vector = normal_vector1.plus(normal_vector2)
         new_constant_term = constant_term1 + constant_term2

         self[row_to_be_added_to] = Plane(normal_vector= new_normal_vector, constant_term = new_constant_term)
         return self


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

s = LinearSystem([p0,p1,p2,p3])


s.swap_rows(0,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print 'test case 1 failed'


s.swap_rows(1,3)
if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    print 'test case 2 failed'


s.swap_rows(3,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print 'test case 3 failed'

print s

s.multiply_coefficient_and_row(1,0)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print 'test case 4 failed'

s.multiply_coefficient_and_row(-1,2)
if not (s[0] == p1 and
        s[1] == p0 and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 5 failed'

s.multiply_coefficient_and_row(10,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 6 failed'


s.add_multiple_times_row_to_row(0,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 7 failed'

s.add_multiple_times_row_to_row(1,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 8 failed'

s.add_multiple_times_row_to_row(-1,1,0)
if not (s[0] == Plane(normal_vector=Vector(['-10','-10','-10']), constant_term='-10') and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 9 failed'


p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])

print s.indices_of_first_nonzero_terms_in_each_row()



p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])

t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print 'test case 1 failed'
