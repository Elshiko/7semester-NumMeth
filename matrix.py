class matrix:
  #format data[i] - i-th row in matrix
  def __init__(self, matrix):
    """Matrix must be list of lists of int/float"""
    self.filled = False
    correct = True
    self.data = []
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
      self.data = [row[:] for row in matrix]
      self.filled = True

  def generate_e(self, dim):
    """Method replace current matrix with E-matrix, dim --> dimension"""
    for row in range(dim):
      self.data.append([0] * dim)
      self.data[row][row] = 1

  def print(self, precision = 6):
    if type(precision) != int:
      print('Incorrect precision type, ignored')
      precision = 6
    pattern = '{0:.' + str(precision) + 'f} '
    for row in range(len(self.data)):
      for col in range(len(self.data[row])):
        print(pattern.format(self.data[row][col]), end = '')
      print()

  def is_square(self):
    square = True
    row_cnt = len(self.data)
    for row in self.data:
      square &= row_cnt == len(row)
    return square

  def size(self):
    return len(self.data)

  def get(self, row, col):
    return self.data[row][col]

  def mult_row(self, row, multiplier):
    for col in range(len(self.data[row])):
      self.data[row][col] *= multiplier

  def set_elem(self, row, col, element):
    if row < len(self.data) and col < len(self.data[row]):
      self.data[row][col] = element

  def add_rows(self, row, to_add):
    """Add line number 'to_add' to line number 'row'"""
    if row < self.size() and to_add < self.size():
      for col in range(len(self.data[row])):
        self.data[row][col] += self.data[to_add][col]

  def rate(self):
    """Euclidean rate"""
    rate = 0
    for row in range(self.size()):
      for col in range(len(self.data[row])):
        rate += self.data[row][col] ** 2
    return pow(rate, 0.5)

  def diagonal_dominance(self):
    """Check for ||a[i][i]|| >= Sum(||a[i][j]||)"""
    dominance = True
    for row in range(len(self.data)):
      diag_elem = abs(self.data[row][row])
      row_sum = 0
      for col in range(len(self.data[row])):
        if col == row:
          continue
        row_sum += abs(self.data[row][col])
      dominance &= row_sum < diag_elem
    return dominance

  def diagonal_split(self):
    """Split matrix A to U(upper) and L(lower)"""
    size = len(self.data)
    upper_triangular = []
    lower_triangular = []
    for row in range(size):
      lower_triangular.append(self.data[row][:row] + [0] * (size - row))
      upper_triangular.append([0] * row + self.data[row][row:])
    upper_triangular = matrix(upper_triangular)
    lower_triangular = matrix(lower_triangular)
    return upper_triangular, lower_triangular
