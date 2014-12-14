def calculate(func, x, y):
  """calculate f(x, y)"""
  func = func.replace('$x', str(x))
  func = func.replace('$y', str(y))
  return eval(func)

def use_rank_two(func, cond, interval, precision):
  pass

def use_rank_three(func, cond, interval, precision):
  pass

def use_rank_four(func, cond, interval, precision):
  eps = 1e-6
  h = 0.01
  left_bound = interval[0]
  right_bound = interval[1]
  x0 = cond[0]
  y0 = cond[1]
  x_list = []
  y_list = []
  if left_bound < x0:
    x_list.append(x0)
    y_list.append(y0)
    for step in range(3):
      if x_list[-1] - h < left_bound + eps:
        break
      x_list.append(x_list[-1] - h)
      y_list.append(y_list[-1] + h*calculate(func, x_list[-1], y_list[-1]))
    while x_list[-1] - h > left_bound - eps:
      first_y = y_list[-4] + 4*h*(2*calculate(func, x_list[-1], y_list[-1])
                                  -calculate(func, x_list[-2], y_list[-2])
                                  +2*calculate(func, x_list[-3], y_list[-3]))/3
      real_y = y_list[-2] + h*(calculate(func, x_list[-1] + h, first_y)
                               +4*calculate(func, x_list[-1], y_list[-1])
                               +calculate(func, x_list[-2], y_list[-2]))/3
      x_list.append(x_list[-1] - h)
      y_list.append(real_y)
    x_list = x_list[:0:-1]
    y_list = y_list[:0:-1]
  x_list.append(x0)
  y_list.append(y0)
  for step in range(3):
    if x_list[-1] + h > right_bound + eps:
      break
    y_list.append(y_list[-1] + h*calculate(func, x_list[-1], y_list[-1]))
    x_list.append(x_list[-1] + h)
  while x_list[-1] + h <= right_bound + eps:
    first_y = y_list[-4] + 4*h*(2*calculate(func, x_list[-1], y_list[-1])
                                -calculate(func, x_list[-2], y_list[-2])
                                +2*calculate(func, x_list[-3], y_list[-3]))/3
    real_y = y_list[-2] + h*(calculate(func, x_list[-1] + h, first_y)
                             +4*calculate(func, x_list[-1], y_list[-1])
                             +calculate(func, x_list[-2], y_list[-2]))/3
    x_list.append(x_list[-1] + h)
    y_list.append(real_y)


  return x_list, y_list

def use_rank_five(func, cond, interval, precision):
  pass
