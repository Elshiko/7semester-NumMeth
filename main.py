#! /usr/bin/python3.3
from matrix import matrix
from vector import vector
from seidel import seidel
from implicit import implicit
from matplotlib import pyplot
import io_lib
import json
import sys

exist_args = ['help', 'input_file', 'input_type', 'output_type',
              'output_file', 'precision', 'separator', 'iterations', 'amount',
              'method', 'silent', 'statistics']

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
      elif arg[0] == '--silent' and len(arg) == 1:
        params['silent'] = 'y'
      else:
        raise Exception('Invalid parameter ' + str(arg))
  return params

def set_default(params):
  if 'help' not in params:
    params['help'] = 'n'
  if 'precision' not in params:
    params['precision'] = 9
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
  if 'method' not in params:
    params['method'] = 'SEIDEL'
  if 'silent' not in params:
    params['silent'] = 'n'
  if 'statistics' not in params:
    params['statistics'] = 1

def print_help():
  print('--help --> print this information\n'
  '--input_file=PATH --> read equation from that file\n'
  'Deafault mode = read from stdin\n'
  '--output_file=PATH --> print answer to that file\n'
  'Deafault mode = print to stdout\n'
  '--input_type=FORMAT --> read equation as you choose\n'
  '--output_type=FORMAT --> print equation as you choose\n'
  'FORMAT = \'JSON\', or \'interactive\', or \'CSV\'\n'
  'JSON & CSV consist of N lines of N+1 element, matrix N*N and column of free terms\n'
  'interactive format: N - dim of matrix, N lines of N elements, 1 line of N elements(free terms)\n'
  '--precision=X --> X is a number, precision of calculation 10^-X\n'
  '--separator=S --> S is separator in .csv file\n'
  '--iterations=Z --> Z is number of iterations\n'
  '--amount=Z --> amount of numbers after . in double\n'
  '--method=METHOD --> choose the way of solving problem\n'
  'METHOD = \'SEIDEL\' or \'IMPLICIT\'\n'
  '--silent --> turn off printing number of iterations\n'
  '--statistics=X --> every X iterations set one point on chart, 0 = OFF, default = 1')

try:
  params = parse_params()
except Exception as error_msg:
  print(error_msg)
  exit(1)
set_default(params)
precision = 10 ** (-1 * int(params['precision']))
iterations = int(params['iterations'])
params['amount'] = int(params['amount'])
silent = True if params['silent'] == 'y' else False
interval = int(params['statistics'])
if params['help'] == 'y':
  print_help()
  exit(0)
else:
  matr_list = []
  vect_list = []
  try:
    if 'input_file' in params:
      matr_list, vect_list = io_lib.read(params['input_file'], params['input_type'],
          params['separator'], matr_list, vect_list, True)
    else:
      matr_list, vect_list = io_lib.read('', params['input_type'],
          params['separator'], matr_list, vect_list, False)
  except Exception as error_msg:
    print(error_msg)
    exit(1)
  matr = matrix(matr_list)
  vect = vector(vect_list)
  try:
    if params['method'] == 'SEIDEL':
      solver = seidel()
      statistics, solution = solver.use_seidel(matr, vect, precision, iterations, silent, interval)
    else:
      solver = implicit()
      statistics, solution = solver.use_implicit(matr, vect, precision, iterations, silent, interval)
  except Exception as error_msg:
    print(error_msg)
    exit(1)
  if 'output_file' in params:
    io_lib.write(params['output_file'], params['output_type'],
        params['separator'], solution, True, params['amount'])
  else:
    io_lib.write('', params['output_type'],
        params['separator'], solution, False, params['amount'])
    if params['statistics'] != '0':
      pyplot.plot(statistics[0], statistics[1], 'r--')
      max_error = statistics[1][0]
      for error in statistics[1]:
        max_error = max(max_error, error)
      pyplot.axis([1, interval * len(statistics[0]), 0, max_error * 1.2])
      pyplot.show()
