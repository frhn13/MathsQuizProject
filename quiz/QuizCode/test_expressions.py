import random
from sympy import symbols, simplify, factor, expand

x = symbols("x")

expanded = 6*x**2 + 29*x + 35
factorised = (3*x + 7)*(2*x + 5)

print(factor(expanded))
