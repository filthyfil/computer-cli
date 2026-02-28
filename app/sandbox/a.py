import sympy as sp

# Define the matrix
matrix = sp.Matrix([
    [1, 0, -2],
    [-3, 1, 4],
    [2, -3, 4]
])

# Calculate the inverse
inverse_matrix = matrix.inv()

print(inverse_matrix)
