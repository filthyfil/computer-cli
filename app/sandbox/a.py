from sympy import symbols, integrate

x = symbols('x')
expression = 3 * x**5
integral = integrate(expression, x)

print(integral)
