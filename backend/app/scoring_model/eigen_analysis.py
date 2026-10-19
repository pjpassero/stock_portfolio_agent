import numpy as np

cov_matrix = np.array([
    [0.04, 0.018, 0.012],
    [0.018, 0.09, 0.025],
    [0.012, 0.025, 0.06]
])

eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

print("Eigenvalues:")
print(eigenvalues)

print("Eigenvectors:")
print(eigenvectors)