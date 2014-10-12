import json
import sys

def read(filename, input_type, separator, matr_list, vect_list, need_file):
  json_error = 'Incorrect JSON, need [[a11, a12, a13, ... b1], ... , [an1, an2, an3, ... , bn]]'
  matr_list = []
  vect_list = []
  if input_type == 'CSV':
    if need_file:
      with open(filename, 'r') as file_with_data:
        data = file_with_data.read().split('\n')
    else:
      data = sys.stdin.read().split('\n')
    if data[-1] == '':
      data = data[:-1]
    for row in range(len(data)):
      data[row] = data[row].split(separator)
      matr_list.append([])
      for col in range(len(data[row]) - 1):
        matr_list[row].append(float(data[row][col]))
      vect_list.append(float(data[row][-1]))
  elif input_type == 'interactive':
    if need_file:
      with open(filename, 'r') as file_with_data:
        data = file_with_data.read().split('\n')
    else:
      data = sys.stdin.read().split('\n')
      if data[-1] == '':
        data = data[:-1]
    if data[-1] == '':
      del data[-1]
    dim = int(data[0])
    del data[0]
    for row in range(dim):
      data[row] = data[row].split(' ')
      matr_list.append([float(data[row][col]) for col in range(dim)])
    data[-1] = data[-1].split(' ')
    vect_list = [float(data[-1][num]) for num in range(dim)]
  elif input_type == 'JSON':
    if need_file:
      with open(filename, 'r') as file_with_data:
        data = file_with_data.read()
    else:
      data = input()
    data = json.loads(data)
    if type(data) != list:
      raise Exception(json_error)
    for row in data:
      if type(row) != list:
        raise Exception(json_error)
      matr_list.append(row[:-1])
      vect_list.append(row[-1])
  return matr_list, vect_list

def write(filename, output_type, separator, solution, need_file, amount):
  if output_type == 'CSV':
    sol = solution.to_csv(separator, amount)
  elif output_type == 'interactive':
    sol = solution.to_string(amount)
  elif output_type == 'JSON':
    sol = solution.to_json()
  if need_file:
    with open(filename, 'w') as file_to_write:
      file_to_write.write(sol)
  else:
    print(sol)
