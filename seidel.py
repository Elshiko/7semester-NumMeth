from vector import vector
from matrix import matrix

class seidel:
  def __init__(self):
    self.__eps = 1e-11

  def __transform(self, old_matr, old_vect):
    """Convert matrix A to B in eq Ax=b to x=Bx+h"""
    dim = old_matr.cnt_row()
    for row in range(dim):
      if old_matr.get(row, row) == 0:
        for to_add in range(dim):
          if old_matr.get(to_add, row) != 0:
            old_matr.sum_rows(row, to_add)
            old_vect.add_elem(row, old_vect.get_elem(to_add))
            break
      if old_matr.get(row, row) == 0:
        raise Exception("Exist column with 0 in all rows")
    #if not old_matr.diagonal_dominance():
    #  return old_matr, old_vect, "There no diagonal dominance"
    for row in range(dim):
      multiplier = -1/old_matr.get(row, row)
      old_matr.mult_row(row, multiplier)
      old_vect.mult_elem(row, -multiplier)
      old_matr.set_elem(row, row, 0.0)
    return old_matr, old_vect

  def __check_precision(self, cur_approx, next_approx, precision):
    """Check ||x(k) - x(k+1)|| <= precision"""
    rate = 0
    for num in range(next_approx.size()):
      if cur_approx.get_elem(num) - next_approx.get_elem(num) > self.__eps:
        temp = cur_approx.get_elem(num) - next_approx.get_elem(num)
        temp = temp*temp if temp > self.__eps else 0
        rate += temp
    rate = rate if rate > self.__eps else 0
    return pow(rate, 0.5) <= precision, pow(rate, 0.5)

  def __calculate_real_precision(self, rate, precision):
    """Transform preciosion, maybe it need to remove"""
    return ((1 - rate)/rate)*precision

  def use_seidel(self, matr, vect, precision, iterations, silent, interval):
    """Main method of class seidel, returns solution of Ax=b,
        params: A --> matr, b --> vect, precision --> effect on number of steps,
        iterations --> max number of steps"""
    if not matr.is_square():
      raise Exception('Coefficient matrix is not square')
    if matr.cnt_row() != vect.size():
      raise Exception('Different size of matrix and vector')
    dim = vect.size()
    matr, vect = self.__transform(matr, vect)
    upper_triangular, lower_triangular = matr.diagonal_split()
    ed_matr = matrix()
    ed_matr.generate_e(matr.cnt_row())
    ed_matr.minus(lower_triangular)
    rev = ed_matr.find_lower_square_reverse()
    kth_step_matr = rev.multiply(upper_triangular)
    vect = rev.multiply(vect)
    cur_approx = vector(vect)
    next_approx = vector(vect)
    self.__eps = precision
    statistics = [[],[]]
    if kth_step_matr.determinant() > 1:
      raise Exception('Matrix determinant > 1')
    for iteration_num in range(iterations):
      next_approx = kth_step_matr.multiply(cur_approx)
      next_approx.add(vect)
      is_accurate, error = self.__check_precision(cur_approx, next_approx, precision)
      if is_accurate:
        if interval != 0:
          statistics[0].append(iteration_num + 1)
          statistics[1].append(error)
        if not silent:
          print('Total number of iterations = ' + str(iteration_num))
        break
      if interval != 0 and iteration_num % interval == 0:
        statistics[0].append(iteration_num + 1)
        statistics[1].append(error)
      cur_approx = vector(next_approx)
    return statistics, next_approx
