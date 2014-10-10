import json

class vector:
  def __init__(self, vector):
    """Vector must be list of int/float"""
    correct = True
    self.filled = False
    self.__data = []
    if type(vector) == type(self):
      vector = vector.to_string().split(' ')
      self.__data = vector[:-1]
      for num in range(self.size()):
        self.__data[num] = float(self.__data[num])
      self.filled = True
      return
    if type(vector) == list:
      for elem in vector:
        if type(elem) != int and type(elem) != float:
          correct = False
    else:
      correct = False
    if correct:
      self.filled = True
      self.__data = vector[:]

  def print(self, precision = 6):
    if type(precision) != int:
      print('Incorrect preciosion type, ignored')
      precision = 6
    pattern = '{0:.' + str(precision) + 'f} '
    for num in range(self.size()):
      print(pattern.format(self.__data[num]), end = '')
    print()

  def size(self):
    return len(self.__data)

  def get_elem(self, num):
    if num < vector.size(self):
      return self.__data[num]

  def set_elem(self, num, value):
    if num < vector.size(self):
      self.__data[num] = value

  def mult_elem(self, num, multiplier):
    if num < self.size():
      self.__data[num] *= multiplier

  def add_elem(self, num, add):
    if num < self.size():
      self.__data[num] += add

  def rate(self):
    """Euclidean rate"""
    rate = 0
    for num in range(self.size()):
      rate += self.__data[num] ** 2
    return pow(rate, 0.5)

  def to_json(self):
   return json.dumps(self.__data)

  def to_csv(self, separator = ',', amount = 6):
    csv_string = ''
    for num in range(self.size()):
      csv_string += format(self.__data[num], '.' + str(amount) + 'f') + ','
    csv_string = csv_string[0:-1]
    return csv_string

  def to_string(self, amount = 6):
    string = ''
    form_param = '.' + str(amount) + 'f'
    for num in range(self.size()):
      string += format(self.__data[num], '.' + str(amount) + 'f') + ' '
    return string

  def add(self, to_add):
    if type(to_add) == vector:
      if self.size() != to_add.size():
        return 'Different sizes'
      for num in range(self.size()):
        self.add_elem(num, to_add.get_elem(num))
      return 'OK'
    else:
      return 'Need ' + str(type(self)) + ', but recieved ' + str(type(to_add))
