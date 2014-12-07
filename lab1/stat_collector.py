#! /usr/bin/python3.3
from matplotlib import pyplot
import sys
import os
from datetime import datetime, timedelta
import time
import subprocess
import numpy

def get_timedelta(time):
  buf = time.split('-')
  buf = buf[1][1:].split(':')
  h = int(buf[0])
  m = int(buf[1])
  buf = buf[2].split('.')
  s = int(buf[0])
  ms = int(buf[1])
  m += h * 60
  s += m * 60
  ms += s * (10 ** 6)
  return ms


def show_help():
  print('help --> show this message\n'
        'dimensions=X-Y --> collect time/iteration statistics for square matrix from XxX to YxY\n'
        'precision=Z --> precision of calculations, 10^-Z\n'
        'method=METHOD --> testing method, possible values : SEIDEL\n'
        'iterations=X --> number of test on one dimension\n'
        'type=Y --> type of output, TIME or ITERATIONS')

exist_args = ['help', 'dimensions', 'precision', 'method', 'iterations', 'type']

params = {'dimensions' : '2-15', 'precision' : '10', 'method' : 'SEIDEL', 'iterations' : '10', 'type' : 'TIME'}

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
iterations = int(params['iterations'])

iter_results = []
dim_results = []
time_results = []
for dim in range(from_dim, to_dim):
  res_iter = 0
  time = 0
  for test_num in range(iterations):
    filename = 'test_matrix_dim_' + str(dim) + '.json'
    with open(filename, 'w') as out_file:
      call_list = []
      call_list.append('./problem_gen.py')
      call_list.append('dimension=' + str(dim))
      subprocess.call(call_list, stdin=None, stdout=out_file)
    with open('results.tmp', 'w') as result_file:
      call_list = []
      call_list.append('./main.py')
      call_list.append('--input_type=JSON')
      call_list.append('--input_file=test_matrix_dim_' + str(dim) + '.json')
      call_list.append('--precision=' + params['precision'])
      call_list.append('--method=' + params['method'])
      call_list.append('--output_type=JSON')
      call_list.append('--statistics=0')
      call_list.append('1>>results.dat')
      subprocess.call(call_list, stdout=result_file)
    call_list = ['rm', filename]
    subprocess.call(call_list)
    with open('results.tmp', 'r') as result_file:
      buf = result_file.read()
      buf = buf.split('\n')
      time += get_timedelta(buf[1])
      res_iter += int(buf[0].split(' ')[-1])
    subprocess.call(['rm', 'results.tmp'])
  time /= iterations
  res_iter /= iterations
  iter_results.append(res_iter)
  time_results.append(time)
  dim_results.append(dim)
if params['type'] == 'ITERATIONS':
  pyplot.plot(dim_results, iter_results, 'r--')
  pyplot.ylabel('iterations')
  pyplot.xlabel('matrix dimension')
  pyplot.show()
else:
  pyplot.plot(dim_results, time_results, 'r--')
  pyplot.ylabel('time')
  pyplot.xlabel('matrix dimension')
  pyplot.show()
