import vector
import matrix

class seidel:
  def __init__(self):
    pass

  def transform(self, old_matr, old_vect):
    dim = old_matr.size()
    for row in range(0, dim):
      if old_matr.get(row, row) == 0:
        for to_add in range(0, dim):
          if old_matr.get(to_add, row) != 0:
            old_matr.sum_rows(row, to_add)
            old_vect.add_elem(row, old_vect.get_elem(to_add))
            break
      if old_matr.get(row, row) == 0:
        return old_matr, old_vect, "Exist column with 0 in all rows"
    #TODO convert to a[ii] >= sum(a[ij]) i != j
    if not old_matr.diagonal_dominance():
      return old_matr, old_vect, "There no diagonal dominance"
    for row in range(0, dim):
      multiplier = -1/old_matr.get(row, row)
      old_matr.mult_row(row, multiplier)
      old_vect.mult_elem(row, -multiplier)
      old_matr.set_elem(row, row, 0)
    return old_matr, old_vect, "OK"

  def check_precision(cur_approx, next_approx, precision):
    #||x(k) - x(k+1)|| <= precision
    rate = 0
    for num in range(0, next_approx.size()):
      rate += pow(cur_approx.get_elem(num) - next_approx.get_elem(num), 2)
    return pow(rate, 0.5) <= precision

  def calculate_real_precision(self, rate, precision):
    return ((1 - rate)/rate)*precision

  def find_solution(self, matr, vect, precision, iterations):
    error = "OK"
    if not matr.is_square():
      error = "Coefficient matrix is not square"
      return vect, error
    if matr.size() != vect.size():
      error = "Different size of matrix and vector"
      return vect, error
    dim = vect.size()
    matr, vect, error = self.transform(matr, vect)
    if error != "OK":
      return vect, error
    upper_triangular, lower_triangular = matr.diagonal_split()
    cur_approx = vector.vector(vect)
    next_approx = vector.vector(vect)
    if (matr.rate() == 0):
      return vect, 'Matrix rate = 0'
    precision = self.calculate_real_precision(matr.rate(), precision)
    iteration_num = 0
    while iteration_num < iterations:
      for row in range(0, dim):
        new_elem = 0
        for col in range(0, dim):
          new_elem += next_approx.get_elem(col)*lower_triangular.get(row, col)
          new_elem += cur_approx.get_elem(col)*upper_triangular.get(row, col)
        new_elem += vect.get_elem(row)
        next_approx.set_elem(row, new_elem)
      if seidel.check_precision(cur_approx, next_approx, precision):
        break
      cur_approx = vector.vector(next_approx)
    return next_approx, error
