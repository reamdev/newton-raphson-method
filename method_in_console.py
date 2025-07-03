from math import *

# Funcion
def f(x):
    func = cos(x)-x**3
    return func

# Derivada de la funcion
def df(x):
    func = -sin(x)-3*x**2
    return func

def newton_raphson_method(x0, tol, n):
    for k in range(n):
        x1 = x0 - f(x0)/df(x0)
        if abs(x1 - x0)<tol:
            print('x', k+1, '=', x1, end=' ')
            print('Es una buena aproximacion de la raiz')
            return
        x0 = x1
        print('x', k+1, '=', x1)

# newton_raphson_method(pi, 1e-6, 10)
newton_raphson_method(pi, 0.0000001, 10)

