#! /usr/bin/python3.3
import matrix
import vector
import seidel
import array

a = [[15, 2, -1, -1],[1, -10, -1, -2],[2, 1, 12, 1], [1, 1, 1, 11]]
A = matrix.matrix(a)
V = vector.vector([22, -14, -10, -20])
c = seidel.seidel()
sol, error = c.find_solution(A, V, 1e-1)
if error != "OK":
  print(error)
else:
  sol.print()
