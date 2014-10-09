import json

def read(filename, input_type, separator, matr_list, vect_list, need_file):
  json_error = 'Incorrect JSON, need [[a11, a12, a13, ... b1], ... , [an1, an2, an3, ... , bn]]'
  matr_list = []
  vect_list = []
  if input_type == 'CSV':
    if need_file:
      with open(filename, 'r') as file_with_data:
        data = file_with_data.read().split('\n')
        for row in range(0, len(data)):
          matr_list.append([])
          for col in range(0, len(data[row])):
            matr_list[row].append(float(data[row][col]))
          vect_list.append(float(data[row][-1]))
    else:
      data = input().split(separator)
      matr_list.append([])
      dim = len(data)
      for col in range(0, dim - 1):
        matr_list[0].append(float(data[col]))
      vect_list.append(float(data[-1]))
      for row in range(1, dim):
        data = input().split(separator)
        matr_list.append([])
        for col in range(0, dim - 1):
          matr_list[row].append(float(data[col]))
        vect_list.append(float(data[dim - 1]))
  elif input_type == 'interactive':
    if need_file:
      with open(filename, 'r') as file_with_data:
        data = file_with_data.read().split('\n')
        if data[-1] == '':
          del data[-1]
        dim = int(data[0])
        del data[0]
        for row in range(0, dim):
          data[row] = data[row].split(' ')
          matr_list.append([float(data[row][col]) for col in range(0, dim)])
        data[-1] = data[-1].split(' ')
        vect_list = [float(data[-1][num]) for num in range(0, dim)]
    else:
      dim = int(input())
      for row in range(0, dim):
        matr_list.append([])
        line = input().split(' ')
        matr_list[row] = [float(line[col]) for col in range(0, dim)]
      data = input().split(' ')
      vect_list = [float(data[num]) for num in range(0, dim)]
  elif input_type == 'JSON':
    if need_file:
      with open(filename, 'r') as file_with_data:
        data = file_with_data.read()
    else:
      data = input()
    matr_list = json.loads(data)
    if type(data) != list:
      return json_error
    for row in range(0, len(data)):
      if tepy(data[row]) != list:
        return json_error
      vect_lsit.append(matr_list[row][-1])
      del matr_list[row][-1]
  return matr_list, vect_list, 'OK'

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
