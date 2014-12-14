#! /usr/bin/python3.3
import math
import sys
import miln
import matplotlib.pyplot as pplot
from math import *

def show_help():
  print('help --> show this message\n'
        'func=\'EXPR\' --> equation, argument x must be $x in input, y must be $y, func = y\'\n'
        'condition=x%y, where x = x0, y = y(x0)\n'
        'interval=A%B --> interval of solving [A;B]\n'
        'answer=\'EXPR\' --> function y(x), x -> $x\n'
        'step=Z --> set H')

def calculate(func, x):
  """calculate y=f(x)"""
  func = func.replace('$x', str(x))
  return eval(func)

exist_args = ['func', 'condition', 'interval', 'answer', 'step']
params = {'func' : '$x', 'condition' : '0%0', 'interval' : '0%1', 'answer' : '$x*$x/2', 'step' : '0.05', 'is_answer' : False}


for raw_arg in sys.argv:
  if raw_arg == sys.argv[0]:
    continue
  if raw_arg == 'help':
    show_help()
    exit(0)
  arg = raw_arg.split('=')
  if len(arg) != 2 or arg[0] not in exist_args:
    print('Incorrect parameter \'' + raw_arg + '\'')
  else:
    params[arg[0]] = arg[1]
    if arg[0] == 'answer':
      params['is_answer'] = True

params['condition'] = params['condition'].split('%')
if len(params['condition']) != 2:
  print('Incorrect condition')
  exit(1)
params['condition'][0] = float(params['condition'][0])
params['condition'][1] = float(params['condition'][1])
params['interval'] = params['interval'].split('%')
if len(params['interval']) != 2:
  print('Incorrect interval')
  exit(1)
params['interval'][0] = float(params['interval'][0])
params['interval'][1] = float(params['interval'][1])
if params['interval'][0] > params['interval'][1] or params['condition'][0] < params['interval'][0] or params['condition'][0] > params['interval'][1]:
  print('Incorrect interval or condition')
  exit(1)
params['step'] = float(params['step'])

x_rank2, y_rank2 = miln.solve(params['func'], params['condition'], params['interval'], params['step'], 2)
x_rank3, y_rank3 = miln.solve(params['func'], params['condition'], params['interval'], params['step'], 3)
x_rank4, y_rank4 = miln.solve(params['func'], params['condition'], params['interval'], params['step'], 4)
x_rank5, y_rank5 = miln.solve(params['func'], params['condition'], params['interval'], params['step'], 5)
x = [x_rank2, x_rank3, x_rank4, x_rank5]
y = [y_rank2, y_rank3, y_rank4, y_rank5]

dlt = lambda a, b: abs(a - b)
pplot.figure(1)
in_col = 1
in_row = 4
if params['is_answer']:
  in_row += 1
  in_col += 1
for i in range(1, 5):
  pplot.subplot(in_col, in_row, i)
  pplot.plot(x[i - 1], y[i - 1])
  pplot.xlabel('x')
  pplot.ylabel('u rank ' + str(i + 1))
if params['is_answer']:
  real = list(map(lambda a: calculate(params['answer'], a), x[0]))
  pplot.subplot(in_col, in_row, 5)
  pplot.plot(x[0], real)
  pplot.xlabel('x')
  pplot.ylabel('real function')
  for i in range(6, 10):
    pplot.subplot(in_col, in_row, i)
    pplot.plot(x[i - 6], list(map(dlt, y[i - 6], real)))
    pplot.xlabel('x')
    pplot.ylabel('abs(y_rank_' + str(i + 1) + ' - real function)')
  pplot.subplot(in_col, in_row, 10)
  pplot.plot(x[0], y[0], 'bs', x[1], y[1], 'gs', x[2], y[2], 'rs', x[3], y[3], 'g^')
  pplot.xlabel('x')
  pplot.ylabel('abs(y - real)')
pplot.show()
