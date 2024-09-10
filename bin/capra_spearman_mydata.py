import numpy as np
import pandas as pd
import scipy.stats as stats

def load_matrix(file_path):
    """Load the matrix from a tab-delimited file"""
    data = pd.read_csv(file_path, sep='\t', header=None)
    matrix = pd.pivot_table(data, index=0, columns=1, values=2, fill_value=0).values
    return matrix

def calculate_spearman_per_window(matrix1, matrix2):
    """Calculate Spearman correlation for each matching bin"""
    num_rows, num_cols = matrix1.shape
    spearman_correlations = []

    # Iterate through each bin in the matrix
    for i in range(num_rows):
        for j in range(num_cols):
            if matrix1[i, j] != 0 or matrix2[i, j] != 0:  # Only calculate for non-zero bins
                spearman_corr, _ = stats.spearmanr([matrix1[i, j]], [matrix2[i, j]])
                spearman_correlations.append(((i, j), spearman_corr))
    
    return spearman_correlations

def main():
    matrix1_file = '../hicompare/input/reps/hicpro/final/allpng/allpng_chr12_50000.txt'
    matrix2_file = '../hicompare/input/reps/hicpro/final/alleur/alleur_chr12_50000.txt'

    # Load matrices
    matrix1 = load_matrix(matrix1_file)
    matrix2 = load_matrix(matrix2_file)
    
    # Ensure the matrices have the same shape
    min_rows = min(matrix1.shape[0], matrix2.shape[0])
    min_cols = min(matrix1.shape[1], matrix2.shape[1])
    matrix1 = matrix1[:min_rows, :min_cols]
    matrix2 = matrix2[:min_rows, :min_cols]

    # Calculate Spearman correlation for each window
    spearman_correlations = calculate_spearman_per_window(matrix1, matrix2)
    
    # Output results
    for window, spearman_corr in spearman_correlations:
        print(f"Window {window}: Spearman correlation = {spearman_corr}")

if __name__ == '__main__':
    main()

