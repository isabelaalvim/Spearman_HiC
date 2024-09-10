import numpy as np
import pandas as pd

def load_matrix(file_path):
    """Load the matrix from a tab-delimited file"""
    data = pd.read_csv(file_path, sep='\t', header=None)
    matrix = pd.pivot_table(data, index=0, columns=1, values=2, fill_value=0).values
    return matrix

def check_sparsity_per_window(matrix, window_size=1000000):
    """Check the proportion of non-zero values in each window"""
    num_rows, num_cols = matrix.shape
    sparsity_results = []
    
    for i in range(num_rows):
        for j in range(num_cols):
            total_elements = 1  # Each window represents one element in your binning
            non_zero_elements = 1 if matrix[i, j] != 0 else 0
            sparsity_ratio = (total_elements - non_zero_elements) / total_elements
            sparsity_results.append(((i, j), sparsity_ratio))
            print(f"Window {i},{j}: {sparsity_ratio:.2%} sparse")
    
    return sparsity_results

matrix1 = load_matrix('../hicompare/input/reps/hicpro/final/alleur/alleur_chr1_50000.txt')
matrix2 = load_matrix('../hicompare/input/reps/hicpro/final/allpng/allpng_chr1_50000.txt')

print("Sparsity for matrix 1:")
check_sparsity_per_window(matrix1)

print("Sparsity for matrix 2:")
check_sparsity_per_window(matrix2)

