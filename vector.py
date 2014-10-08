import json

class vector:
  def __init__(self, vector):
    correct = True
    self.filled = False
    if type(vector) == type(self):
      self.data = []
      for num in range(0, vector.size()):
        self.data.append(vector.get_elem(num))
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
      self.data = list(vector)
    else:
      self.data = []

  def print(self):
    for num in range(0, len(self.data)):
      print('{0:.6f} '.format(self.data[num]), end = '')
    print()

  def size(self):
    return len(self.data)

  def get_elem(self, num):
    if num < vector.size(self):
      return self.data[num]

  def set_elem(self, num, value):
    if num < vector.size(self):
      self.data[num] = value

  def mult_elem(self, num, multiplier):
    if num < len(self.data):
      self.data[num] *= multiplier

  def add_elem(self, num, add):
    if num < len(self.data):
      self.data[num] += add

  def rate(self):
    rate = 0
    for num in range(0, len(self.data)):
      rate += self.data[num] ** 2
    return pow(rate, 0.5)

  def to_json(self):
   return json.dumps(self.data)

  def to_csv(self, separator, amount):
    csv_string = ''
    for num in range(0, len(self.data)):
      csv_string += format(self.data[num], '.' + str(amount) + 'f') + ','
    csv_string = csv_string[0:-1]
    return csv_string

  def to_string(self, amount):
    string = ''
    form_param = '.' + str(amount) + 'f'
    for num in range(0, len(self.data)):
      string += format(self.data[num], '.' + str(amount) + 'f') + ' '
    return string
