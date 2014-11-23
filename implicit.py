from vector import vector
from matrix import matrix
import math

class implicit:
  def __init__(self):
    pass

  def __convert_to_symmetric_positive(self, matr, vect):
    """symmetric: A = A_transpose, positive: (Mx, x) > 0"""
    if not matr.is_symmetric():
      matr = matr.multiply(matr.transpose())
      if not matr.is_symmetric():
        raise Exception('Matrix A is not symmetric & A_transpose*A is not symmetric')
    vector_x = vector([1 for num in range(vect.size())])
    vector_mx = matr.multiply(vector_x)
    if vector_x.scalar_mult(vector_mx) <= 0:
      raise Exception('Matrix A*A is not positive')
    return matr

  def __calculate_xi(self, matr, matr_m):
    #TODO FIX IT
    return 1/matr.multiply(matr_m.find_lower_square_reverse()).rate()

  def __calculate_ro(self, matr, matr_m):
    xi = self.__calculate_xi(matr, matr_m)
    return (1 - xi)/(1 + xi)

  def __calculate_t_list(self, total_steps):
    """tk = cos((2k - 1) * pi / (2n)"""
    for step in range(total_steps):
      yield math.cos((2*step)*math.pi/(2*total_steps))

  def __calculate_tau_list(self, tau, iterations, ro):
    t_list = list(self.__calculate_t_list(iterations))
    for t in t_list:
      yield tau/(1 + ro*t)

  def __calculate_tau(self, matr):
    """Calculate tau = 2/(M + m) or tau = 2 / sigma, where sigma > Matrix rate"""
    return 1/matr.rate()

  def __calculate_matrix_M(sefl, matr):
    """M = D(A), M * (x(k + 1) - x() / tau(k + 1)) + Ax = b"""
    matr_m = matrix([])
    matr_m.generate_e(matr.cnt_row())
    for row in range(matr.cnt_row()):
      matr_m.set_elem(row, row, matr.get(row, row))
    return matr_m

  def __next_step(self, matr_m, matr, vect, cur_approx, t):
    """In this func: from M*(x(k+1)-x(k))/t(k+1) + Ax(k) = b
                     to x(k+1) = t(k+1)b - t(k + 1)Ax(k) + x(k)"""
    next_approx = vector(vect)
    next_approx.mult_by_number(t)
    next_approx.add(cur_approx)
    matr_a = matr.multiply(cur_approx)
    matr_a.mult_by_number(t)
    next_approx.add(matr_a)
    next_approx.print()
    print()
    return next_approx

  def use_implicit(self, matr, vect, precision, iterations, silent, interval):
    """Main method of class implicit, returns solution of Ax=b,
        params: A --> matr, b --> vect, precision --> effect on number of steps,
        iterations --> max number of steps"""
    if not matr.is_square():
      raise Exception('Coefficient matrix is not square')
    if matr.cnt_row() != vect.size():
      raise Exception('Different size of matrix and vector')
    matr = self.__convert_to_symmetric_positive(matr, vect)
    matr_m = self.__calculate_matrix_M(matr)
    tau = self.__calculate_tau(matr)
    ro = self.__calculate_ro(matr, matr_m)
    t_list = list(self.__calculate_tau_list(tau, iterations, ro))
    cur_approx = vector([0]*vect.size())
    print(cur_approx)
    matr_m = matr_m.find_lower_square_reverse()
    for t in t_list:
      cur_approx = self.__next_step(matr_m, matr, vect, cur_approx, t)
    return cur_approx
