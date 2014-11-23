#! /usr/bin/python3.3
import random
import sys

def show_help():
  print('dimension=X --> dimension of matrix\n'
        'lower_limit=X --> lower limit of numbers in matrix\n'
        'upper_limit=X --> upper limit of numbers in matrix\n'
        'matrix_type=TYPE --> type of matrix : RANDOM, default\n'
        'RANDOM - matrix with diagonal dominance\n'
        'help --> show this message\n')

def gen_random(n, low, up):
  matr_list = []
  delta = up - low
  for row in range(n):
    matr_list.append([])
    for col in range(n):
      matr_list[-1].append(random.random())
      if col == row:
        matr_list[-1][-1] *= 10
      matr_list[-1][-1] = (matr_list[-1][-1] / 10 * delta) + low
    matr_list[-1].append(random.random())
    matr_list[-1][-1] = (matr_list[-1][-1] / 10 * delta) + low
  print(matr_list)

exist_args = ['dimension', 'lower_limit', 'upper_limit', 'matrix_type']

params = {}
params['dimension'] = 10
params['lower_limit'] = 0
params['upper_limit'] = 100
params['matrix_type'] = 'RANDOM'

for raw_arg in sys.argv:
  if raw_arg == sys.argv[0]:
    continue
  if raw_arg == 'help':
    show_help()
    exit(0)
  arg = raw_arg.split('=')
  if arg[-1] == '':
    arg = arg[:-1]
  if len(arg) != 2 or arg[0] not in exist_args:
    print('Invalid argument \'' + raw_arg + '\'')
  else:
    params[arg[0]] = arg[1]
params['dimension'] = int(params['dimension'])
params['lower_limit'] = int(params['lower_limit'])
params['upper_limit'] = int(params['upper_limit'])

if params['upper_limit'] <= params['lower_limit']:
  print('Incorrect limits')
  eixt(1)

if params['matrix_type'] == 'RANDOM':
  gen_random(params['dimension'], params['lower_limit'], params['upper_limit'])
else:
  print('Incorrect type')
