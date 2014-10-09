from vector import vector

class matrix:
  #format data[i] - i-th row in matrix
  def __init__(self, matrix = []):
    """Matrix must be list of lists of int/float"""
    correct = True
    self.__data = []
    if type(matrix) == list:
      for row in matrix:
        if type(row) == list:
          for elem in row:
            correct = False if type(elem) != int and type(elem) != float else True
        else:
          correct = False
    else:
      correct = False
    if correct:
      self.__data = [row[:] for row in matrix]

  def generate_e(self, dim):
    """Method replace current matrix with E-matrix, dim --> dimension"""
    for row in range(dim):
      self.__data.append([0.0] * dim)
      self.__data[row][row] = 1.0

  def print(self, precision = 6):
    if type(precision) != int:
      print('Incorrect precision type, ignored')
      precision = 6
    pattern = '{0:.' + str(precision) + 'f} '
    for row in range(self.cnt_row()):
      for col in range(self.cnt_col()):
        print(pattern.format(self.__data[row][col]), end = '')
      print()

  def is_square(self):
    return self.cnt_row() == self.cnt_col()

  def cnt_row(self):
    return len(self.__data)

  def cnt_col(self):
    return 0 if len(self.__data) == 0 else len(self.__data[0])

  def get(self, row, col):
    return self.__data[row][col]

  def mult_row(self, row, multiplier):
    if row < self.cnt_row():
      for col in range(self.cnt_col()):
        self.__data[row][col] *= multiplier

  def set_elem(self, row, col, element):
    if row < self.cnt_row() and col < self.cnt_col():
      self.__data[row][col] = element

  def add_rows(self, row, to_add):
    """Add line number 'to_add' to line number 'row'"""
    if row < self.cnt_row() and to_add < self.cnt_col():
      for col in range(self.cnt_col()):
        self.__data[row][col] += self.__data[to_add][col]

  def rate(self):
    """Euclidean rate"""
    rate = 0
    for row in range(self.cnt_row()):
      for col in range(self.cnt_col()):
        rate += self.__data[row][col] ** 2
    return pow(rate, 0.5)

  def diagonal_dominance(self):
    """Check for ||a[i][i]|| >= Sum(||a[i][j]||)"""
    dominance = True
    for row in range(self.cnt_row()):
      diag_elem = abs(self.__data[row][row])
      row_sum = 0
      for col in range(self.cnt_col()):
        row_sum += abs(self.__data[row][col]) if col != row else 0
      dominance &= row_sum < diag_elem
    return dominance

  def diagonal_split(self):
    """Split matrix A to U(upper) and L(lower), need square matrix"""
    upper_triangular = []
    lower_triangular = []
    if not self.is_square():
      return upper_triangular, lower_triangular, 'Maxtrix must be square'
    size = self.cnt_row()
    for row in range(size):
      lower_triangular.append(self.__data[row][:row] + [0.0] * (size - row))
      upper_triangular.append([0.0] * row + self.__data[row][row:])
    upper_triangular = matrix(upper_triangular)
    lower_triangular = matrix(lower_triangular)
    return upper_triangular, lower_triangular, 'OK'

  def get_dim(self):
    return self.cnt_row(), self.cnt_col()

  def minus(self, subtrahend):
    if self.get_dim() != subtrahend.get_dim():
      return 'Some problems with dimension'
    for row in range(self.cnt_row()):
      for col in range(self.cnt_col()):
        self.__data[row][col] -= subtrahend.get(row, col)
    return 'OK'

  def add_row_with_ratio(self, row, to_add, ratio):
    if self.cnt_row() > 0:
      for col in range(self.cnt_col()):
        self.__data[row][col] += self.__data[to_add][col] * ratio

  def find_lower_square_reverse(self):
    rev = matrix()
    rev.generate_e(self.cnt_row())
    for row in range(self.cnt_row()):
      for col in range(row):
        if self.__data[row][col] != 0:
          multiplier = self.__data[row][col]
          rev.add_row_with_ratio(row, col, -multiplier)
    return rev

  def multiply(self, multiplier):
    error = 'Number of columns in first matrix must equal number of rows in second multiplier(matrix/vector)'
    result = []
    if type(multiplier) == matrix:
      if self.cnt_col() != multiplier.cnt_row():
        return error, matrix(result)
      for row in range(self.cnt_row()):
        result.append([])
        for col in range(multiplier.cnt_col()):
          result[row].append(0)
          for step in range(self.cnt_col()):
            result[row][col] += self.get(row, step) * multiplier.get(step, col)
      return 'OK', matrix(result)
    elif type(multiplier) == vector:
      if self.cnt_col() != multiplier.size():
        return error, vector(result)
      for row in range(self.cnt_row()):
        result.append(0)
        for col in range(self.cnt_col()):
          result[row] += self.get(row, col) * multiplier.get_elem(col)
      return 'OK', vector(result)
