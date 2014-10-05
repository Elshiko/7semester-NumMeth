class matrix:
  #format data[i] - i-th row in matrix
  def __init__(self, matrix):
    self.filled = False
    correct = True
    if type(matrix) == list:
      for row in matrix:
        if type(row) == list:
          for elem in row:
            if type(elem) != int and type(elem) != float:
              correct = False
        else:
          correct = False
    else:
      correct = False
    if correct:
      self.filled = True
      self.data = matrix
    else:
      self.data =[[]]

  def print(self):
    for row in range(0, len(self.data)):
      for col in range(0, len(self.data[row])):
        print('{0:.6f} '.format(self.data[row][col]), end = '')
      print()

  def is_filled(self):
    return self.filled

  def is_square(self):
    square = True
    row_cnt = len(self.data)
    for row in self.data:
      if row_cnt != len(row):
        square = False
    return square

  def size(self):
    return len(self.data)

  def get(self, row, col):
    return self.data[row][col]

  def mult_row(self, row, multiplier):
    for col in range(0, len(self.data[row])):
      self.data[row][col] *= multiplier

  def set_elem(self, row, col, element):
    if row < len(self.data) and col < len(self.data[row]):
      self.data[row][col] = element

  def diagonal_split(self):
    size = len(self.data)
    upper_triangular = []
    lower_triangular = []
    for row in range(0, size):
      lower_triangular.append([])
      upper_triangular.append([])
      for col in range(0, row):
        lower_triangular[row].append(self.data[row][col])
        upper_triangular[row].append(0)
      for col in range(row, size):
        lower_triangular[row].append(0)
        upper_triangular[row].append(self.data[row][col])
    upper_triangular = matrix(upper_triangular)
    lower_triangular = matrix(lower_triangular)
    return upper_triangular, lower_triangular
