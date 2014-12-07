from math import *

def compute(func, x):
  """generate function values"""
  func = func.replace('$x', str(x))
  return eval(func)

def compute_coef_a(func_val):
  """simply clone list"""
  return func_val[:]

def compute_lambda_sigma(func_val, h):
  """calculate list of lambda and list of sigma, need to calculate list of C"""
  lmbd = [0]
  sigma = [0]
  sigma.append(-h[1]/(2*h[0] + 2*h[1]))
  lmbd.append((2*(func_val[2] - func_val[1])/h[1] - 3*(func_val[1] - func_val[0])/h[0])/(2*h[0] + 2*h[1]))
  for ind in range(3, len(func_val)):
    zn = 2*h[ind-2] + 2*h[ind-1] + h[ind-2]*sigma[-1]
    sigma.append(-h[ind-1]/zn)
    tmp = 3*(func_val[ind] - func_val[ind-1])/h[ind-1] - 3*(func_val[ind-1] - func_val[ind-2])/h[ind-2] - h[ind-2]*lmbd[-1]
    tmp /= zn
    lmbd.append(tmp)
  return lmbd, sigma

def compute_coef_c(lmbd, sigma):
  c = [0.0]
  lmbd = lmbd[::-1]
  sigma = sigma[::-1]
  for i in range(len(sigma)):
    c.append(c[-1]*sigma[i] + lmbd[i])
  return c[::-1]

def compute_coef_d(c, h):
  d = [0.0]
  for i in range(len(h)):
    d.append((c[i + 1] - c[i])/h[i])
  return d

def compute_coef_b(c, f, h):
  b = [0.0]
  for i in range(1, len(f)):
    df = (f[i] - f[i-1])/h[i-1]
    b.append(df + 2*h[i-1]*c[i]/3 + h[i-1]*c[i-1]/3)
  return b

def interpolate(x, xk, a, b, c, d):
  dx = x - xk
  value = a + b*dx + c*(dx**2) + d*(dx**3)
  return value

def do_interpolation(func, num_of_nodes, left_bound, right_bound, graph, check_points, h_list = []):
  """interpolation of function, return list of pack of coefficients of cubic spline"""
  #h[k] = x[k+1] - x[k]
  #in book h[k] = x[k] - x[k - 1]
  h = (right_bound - left_bound) / (num_of_nodes - 1)
  left_bound = float(left_bound)
  right_bound = float(right_bound)
  list_of_nodes = []
  func_values = []
  fx = compute(func, left_bound)
  list_of_nodes.append(left_bound)
  func_values.append(fx)
  if h_list == []:
    h_list = [h] * (num_of_nodes - 1)
  for i in range(1, num_of_nodes):
    fx = compute(func, left_bound + i * h)
    list_of_nodes.append(left_bound + i * h)
    func_values.append(fx)

  coef_a = compute_coef_a(func_values)
  #x ** 2, x = [1, 2, 3, 4, 5]. Test OK.
  lmbd, sigma = compute_lambda_sigma(func_values, h_list)

  coef_c = compute_coef_c(lmbd, sigma)
  coef_d = compute_coef_d(coef_c, h_list)
  coef_b = compute_coef_b(coef_c, func_values, h_list)

  x = []
  res_func_values = []
  interpolated_values = []
  x.append(left_bound)
  res_func_values.append(func_values[0])
  interpolated_values.append(func_values[0])
  cur_x = left_bound
  max_delta = 0
  for i in range(0, len(h_list)):
    for cnt in range(1, check_points + 1):
      x_to_comp = cur_x + cnt / check_points * h_list[i]
      x.append(x_to_comp)
      res_func_values.append(compute(func, x_to_comp))
      interpolated_values.append(interpolate(x_to_comp, cur_x + h_list[i], coef_a[i+1], coef_b[i+1], coef_c[i+1], coef_d[i+1]))
      max_delta = max(max_delta, abs(res_func_values[-1] - interpolated_values[-1]))
    cur_x += h_list[i]
  return x, res_func_values, interpolated_values, max_delta
