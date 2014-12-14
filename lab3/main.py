#! /usr/bin/python3.3
import math
import sys
import miln
import matplotlib.pyplot as pplot

def show_help():
  print('help --> show this message\n'
        'func=\'EXPR\' --> equation, argument x must be $x in input, y must be $y, func = y\'\n'
        'condition=x%y, where x = x0, y = y(x0)\n'
        'interval=A%B --> interval of solving [A;B]\n'
        'graph=C --> y - enable charts, n - disable\n'
        'silent=y/n --> enable/disable silent mode, :::All char except \'y\' = \'n\'\n'
        'answer=\'EXPR\' --> function y(x), x -> $x\n'
        'chart=TYPE --> set chart type DELTA or BOTH, DELTA_PERCENT, SOLVE !!!if there is no answer, than will be SOLVE chart\n'
        'precision=Z --> eps = 1e-Z')

def calculate(func, x):
  """calculate y=f(x)"""
  func = func.replace('$x', str(x))
  return eval(func)

exist_args = ['func', 'condition', 'interval', 'graph', 'answer', 'silent', 'chart', 'precision']
params = {'func' : '$x', 'condition' : '0%0', 'interval' : '0%1', 'graph' : 'y', 'answer' : '$x*$x/2', 'silent' : 'n', 'chart' : 'BOTH', 'precision' : '4'}


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
if params['graph'] == 'y':
  params['graph'] = True
else:
  params['graph'] = False
if params['silent'] == 'y':
  params['silent'] = True
else:
  params['silent'] = False
params['precision'] = 10 ** (-1*int(params['precision']))

#x_rank2, y_rank2 = miln.use_rank_two(params['func'], params['condition'], params['interval'], params['precision'])
#x_rank3, y_rank3 = miln.use_rank_three(params['func'], params['condition'], params['interval'], params['precision'])
x_rank4, y_rank4 = miln.use_rank_four(params['func'], params['condition'], params['interval'], params['precision'])
#x_rank5, y_rank5 = miln.use_rank_five(params['func'], params['condition'], params['interval'], params['precision'])
zp = zip(x_rank4, y_rank4)
pr = lambda a: print(str(a[0]) + '     :     ' + str(a[1]) + '     -      ' + str(calculate(params['answer'], a[0])))
ans = list(map(pr, zp))
