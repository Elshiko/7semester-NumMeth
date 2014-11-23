#! /usr/bin/python3.3
from matplotlib import pyplot
import sys
import os

def show_help():
  print('help --> show this message\n'
        'dimensions=X-Y --> collect time/iteration statistics for square matrix from XxX to YxY\n'
        'precision=Z --> precision of calculations, 10^-Z\n'
        'method=METHOD --> testing method, possible values : SEIDEL\n')

exist_args = ['help', 'dimensions', 'precision', 'method']

params = {'dimensions' : '2-15', 'precision' : '10', 'method' : 'SEIDEL'}

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

dims = params['dimensions'].split('-')
from_dim = int(dims[0])
to_dim = int(dims[1]) + 1

os.popen('rm results.dat')
for dim in range(from_dim, to_dim):
  os.popen('./problem_gen.py dimension=' + str(dim) + ' 1>test_matrix_dim_' + str(dim) + '.json')
  os.popen('./main.py input_type=JSON input_file=test_matrix_dim_' + str(dim) + '.json ' +
           'precision=' + params['precision'] + ' method=' + params['method'] + ' output_type=JSON >>results.dat')
