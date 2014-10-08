#! /usr/bin/python3.3
from matrix import matrix
from vector import vector
from seidel import seidel
import io_lib
import json
import sys

exist_args = ['help', 'input_file', 'input_type', 'output_type',
              'output_file', 'precision', 'separator', 'iterations', 'amount']

def parse_params():
  params = {}
  for arg in sys.argv:
    if arg[0:2] == '--':
      arg = arg.split('=')
      if len(arg) == 2:
        value = arg[1]
        arg = arg[0][2:len(arg[0])]
        if arg in params:
          return params, 'Doubled parameter ' + arg
        elif arg not in exist_args:
          return params, 'Invalid parameter ' + arg
        else:
          params[arg] = value
      elif arg[0] == '--help' and len(arg) == 1:
        params['help'] = 'y'
      else:
        return params, 'Invalid parameter ' + str(arg)
  return params, 'OK'

def set_default(params):
  if 'help' not in params:
    params['help'] = 'n'
  if 'precision' not in params:
    params['precision'] = 1e-9
  if 'input_type' not in params:
    params['input_type'] = 'interactive'
  if 'output_type' not in params:
    params['output_type'] = 'interactive'
  if 'separator' not in params:
    params['separator'] = ','
  if 'iterations' not in params:
    params['iterations'] = 10 ** 6
  if 'amount' not in params:
    params['amount'] = 10

def print_help():
  print('--help --> print this information')
  print('--input_file=$PATH --> read equation from that file')
  print('Deafault mode = read from stdin')
  print('--output_file=$PATH --> print answer to that file')
  print('Deafault mode = print to stdout')
  print('--input_type=FORMAT --> read equation as you choose')
  print('--output_type=FORMAT --> print equation as you choose')
  print('FORMAT = \'JSON\', or \'interactive\', or \'CSV\'')
  print('JSON & CSV consist of N lines of N+1 element, matrix N*N and column of free terms')
  print('interactive format: N - dim of matrix, N lines of N elements, 1 line of N elements(free terms)')
  print('--precision=X --> X is a number, precision of calculation')
  print('--separator=S --> S is separator in .csv file')
  print('--iterations=Z --> Z is number of iterations')
  print('--amount=Z --> amount of numbers after . in double')

error = 'OK'
params, error = parse_params()
if error != 'OK':
  print(error)
else:
  set_default(params)
  precision = params['precision']
  iterations = params['iterations']
  params['amount'] = int(params['amount'])
  if params['help'] == 'y':
    print_help()
    exit(0)
  else:
    matr_list = []
    vect_list = []
    if 'input_file' in params:
      matr_list, vect_list, error = io_lib.read(params['input_file'], params['input_type'],
          params['separator'], matr_list, vect_list, True)
    else:
      matr_list, vect_list, error = io_lib.read('', params['input_type'],
          params['separator'], matr_list, vect_list, False)
    if error != 'OK':
      print(error)
      exit(0)
    matr = matrix(matr_list)
    vect = vector(vect_list)
    solver = seidel()
    solution, error = solver.find_solution(matr, vect, precision, iterations)
    if error != 'OK':
      print(error)
      exit(0)
    if 'output_file' in params:
      io_lib.write(params['output_file'], params['output_type'],
          params['separator'], solution, True, params['amount'])
    else:
      io_lib.write('', params['output_type'],
          params['separator'], solution, False, params['amount'])

  #a = [[15, 2, -1, -1],[1, -10, -1, -2],[2, 1, 12, 1], [1, 1, 1, 11]]
  #A = matrix.matrix(a)
  #V = vector.vector([22, -14, -10, -20])
  #c = seidel.seidel()
  #sol, error = c.find_solution(A, V, 1e-1)
  #if error != "OK":
  #  print(error)
  #else:
  #  sol.print()
