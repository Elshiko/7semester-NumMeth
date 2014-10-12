from vector import vector
from matrix import matrix
import math

class implicit:
  def __init__(self):
    pass

  def __convert_to_symmetric_positive(self, matr):
    #TODO
    return matr
  
  def __calculate_xi(self, matr, matr_m):
    #TODO lambda(min)(M^-1*A)/lambda(max)(M^-1*A)
    return 1/matr.rate()

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

  def use_implicit(self, matr, vect, precision, iterations):
    """Main method of class implicit, returns solution of Ax=b,
        params: A --> matr, b --> vect, precision --> effect on number of steps,
        iterations --> max number of steps"""
    matr = self.__convert_to_symmetric_positive(matr)
    matr_m = self.__calculate_matrix_M(matr)
    tau = self.__calculate_tau(matr)
    ro = self.__calculate_ro(matr, matr_m)
    t_list = list(self.__calculate_tau_list(tau, iterations, ro))
    for t in t_list:
      pass

    return vect, 'OK'
