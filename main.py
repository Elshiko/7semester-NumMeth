#! /usr/bin/python3.3
import matrix
import vector
import seidel
import array

a = [[15, 2, -1, -1],[1, -10, -1, -2],[2, 1, 12, 1], [1, 1, 1, 11]]
A = matrix.matrix(a)
V = vector.vector([22, -14, -10, -20])
c = seidel.seidel()
sol = c.find_solution(A, V, 1e-1)
sol.print()

#0.01x1 + 0.02x2 + 0.03x3 = 0
#0.04x1 + 0.05x2 + 0.06x3 = 0.03
#0.07x1 + 0.08x2 + 0.09x3 = 0.06
#x1 = 3
#x2 = -3
#x3 = 1
