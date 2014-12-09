#! /usr/bin/python3.3
import math
import sys
import spline
import matplotlib.pyplot as pplot

def show_help():
  print('help --> show this message\n'
        'func=\'EXPR\' --> function for interpolation, argument x must be $x in input\n'
        'nodes=Z --> Z - number of nodes\n'
        'interval=A-B --> interval of interpolation [A;B]\n'
        'graph=C --> y - enable charts, n - disable\n'
        'check_points=X --> number of points between X[k] and X[k + 1]\n'
        'silent=y/n --> enable/disable silent mode, :::All char except \'y\' = \'n\'\n'
        'chart=TYPE --> set chart type DELTA or BOTH, DELTA_PERCENT')

exist_args = ['func', 'nodes', 'interval', 'graph', 'check_points', 'silent', 'chart']
params = {'func' : '$x', 'nodes' : '2', 'interval' : '0-1', 'graph' : 'y', 'check_points' : '10', 'silent' : 'n', 'chart' : 'DELTA'}

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

params['nodes'] = int(params['nodes'])
params['interval'] = params['interval'].split('-')
if len(params['interval']) != 2:
  print('Incorrect interval')
  exit(1)
params['interval'][0] = float(params['interval'][0])
params['interval'][1] = float(params['interval'][1])
if params['graph'] == 'y':
  params['graph'] = True
else:
  params['graph'] = False
params['check_points'] = int(params['check_points'])
if params['silent'] == 'y':
  params['silent'] = True
else:
  params['silent'] = False

x, func, interpolated, max_delta = spline.do_interpolation(params['func'], params['nodes'], params['interval'][0], params['interval'][1], params['graph'], params['check_points'])

if not params['silent']:
  pattern = '{0:.10f}'
  print('Maximum delta between real and interpolated functions = ' + str(max_delta))
  print('All values of x, real function and interpolation')
  zipped = zip(x, func, interpolated)
  for xval, f, i in zipped:
    print(pattern.format(xval), end = '')
    print('  :  ', end = '')
    print(pattern.format(f), end = '')
    print('   -   ', end = '')
    print(pattern.format(i))

if params['chart'] == 'BOTH':
  pplot.plot(x, func, 'bs', x, interpolated, 'g^')
  pplot.xlabel('x')
  pplot.ylabel('function values')
  pplot.show()
elif params['chart'] == 'DELTA':
  all_delta = list(map(lambda a, b: abs(a - b), func, interpolated))
  pplot.plot(x, all_delta, 'b--')
  pplot.xlabel('x')
  pplot.ylabel('value of delta')
  pplot.show()
else:
  function = lambda a, b: 100 * abs((a - b)/a)
  all_delta = list(map(function, func, interpolated))
  pplot.plot(x, all_delta, 'b--')
  pplot.xlabel('x')
  pplot.ylabel('delta/function value (%)')
  pplot.show()
