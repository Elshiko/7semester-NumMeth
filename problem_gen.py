#! /usr/bin/python3.3
import random
import sys

def gen(n):
  n = int(n)
  matr_list = []
  for row in range(n):
    matr_list.append([])
    for col in range(n):
      matr_list[row].append(random.random())
      if col == row:
        matr_list[row][row] *= 100
    matr_list[row].append(random.random())
  print(matr_list)

n = sys.argv[1]
gen(n)

