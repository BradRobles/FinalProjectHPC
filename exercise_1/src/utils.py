import numpy as np
from scipy.io import mmread
import scipy.sparse as sp

def generate_dense_matrices(size, seed=42):
    np.random.seed(seed)
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    return A, B

def validate_result(C_test, C_true, tol=1e-8):
    return np.allclose(C_test, C_true, atol=tol)

def load_sparse_matrix(filepath):
    sparse_coo = mmread(filepath)
    return sparse_coo.tocsr()
