from sympy import symbols, integrate

x = symbols('x')
expr = 3 * x**2
integral = integrate(expr, x)

print(integral)
