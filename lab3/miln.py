from math import *
def calculate(func, x, y):
  """calculate f(x, y)"""
  func = func.replace('$x', str(x))
  func = func.replace('$y', str(y))
  return eval(func)

def solve(func, cond, interval, h, rank):
  """y[i] = y[i-2] + 2 * h * f(x[i-1], y[i-1])
     y[i] = y[i-3] + 3*h/4*(-3*f[i-3]+8*f[i-2]-f[i-1])"""
  eps = 1e-6
  left_bound = interval[0]
  right_bound = interval[1]
  x0 = cond[0]
  y0 = cond[1]
  x_list = []
  y_list = []
  if left_bound < x0:
    x_list.append(x0)
    y_list.append(y0)
    for step in range(rank - 1):
      if x_list[-1] - h < left_bound + eps:
        break
      x_list.append(x_list[-1] - h)
      y_list.append(y_list[-1] - h*calculate(func, x_list[-1], y_list[-1]))
    while x_list[-1] - h > left_bound - eps:
      first_y = 0
      if rank == 2:
        first_y = y_list[-2] - 2*h*calculate(func, x_list[-1], y_list[-1])
      elif rank == 3:
        first_y = y_list[-3] - 3*h*(-3*calculate(func, x_list[-3], y_list[-3])
                                    +8*calculate(func, x_list[-2], y_list[-2])
                                    -calculate(func, x_list[-1], y_list[-1]))/4
      elif rank == 4:
        first_y = y_list[-4] - 4*h*(2*calculate(func, x_list[-1], y_list[-1])
                                    -calculate(func, x_list[-2], y_list[-2])
                                    +2*calculate(func, x_list[-3], y_list[-3]))/3
      else:
        first_y = y_list[-5] - 25*h*(193*calculate(func, x_list[-5], y_list[-5])
                                     -550*calculate(func, x_list[-4], y_list[-4])
                                     +648*calculate(func, x_list[-3], y_list[-3])
                                     -454*calculate(func, x_list[-2], y_list[-2])
                                     +127*calculate(func, x_list[-1], y_list[-1]))/144
      real_y = y_list[-2] - h*(calculate(func, x_list[-1] + h, first_y)
                               +4*calculate(func, x_list[-1], y_list[-1])
                               +calculate(func, x_list[-2], y_list[-2]))/3
      x_list.append(x_list[-1] - h)
      y_list.append(real_y)
    x_list = x_list[:0:-1]
    y_list = y_list[:0:-1]
  x_list.append(x0)
  y_list.append(y0)
  for step in range(rank - 1):
    if x_list[-1] + h > right_bound + eps:
      break
    y_list.append(y_list[-1] + h*calculate(func, x_list[-1], y_list[-1]))
    x_list.append(x_list[-1] + h)
  while x_list[-1] + h <= right_bound + eps:
    if rank == 2:
      first_y = y_list[-2] + 2*h*calculate(func, x_list[-1], y_list[-1])
    elif rank == 3:
      first_y = y_list[-3] + 3*h*(-3*calculate(func, x_list[-3], y_list[-3])
                                  +8*calculate(func, x_list[-2], y_list[-2])
                                  -calculate(func, x_list[-1], y_list[-1]))/4
    elif rank == 4:
      first_y = y_list[-4] + 4*h*(2*calculate(func, x_list[-1], y_list[-1])
                                  -calculate(func, x_list[-2], y_list[-2])
                                  +2*calculate(func, x_list[-3], y_list[-3]))/3
    else:
        first_y = y_list[-5] + 25*h*(193*calculate(func, x_list[-5], y_list[-5])
                                     -550*calculate(func, x_list[-4], y_list[-4])
                                     +648*calculate(func, x_list[-3], y_list[-3])
                                     -454*calculate(func, x_list[-2], y_list[-2])
                                     +127*calculate(func, x_list[-1], y_list[-1]))/144
    real_y = y_list[-2] + h*(calculate(func, x_list[-1] + h, first_y)
                             +4*calculate(func, x_list[-1], y_list[-1])
                             +calculate(func, x_list[-2], y_list[-2]))/3
    x_list.append(x_list[-1] + h)
    y_list.append(real_y)
  return x_list, y_list
