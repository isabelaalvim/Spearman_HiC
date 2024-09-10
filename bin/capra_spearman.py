import numpy as np
import argparse
import scipy.stats as stats

def bin_matrix(matrix, bin_size):
    """Bin the matrix into windows of size bin_size, cropping excess data to fit binning"""
    num_bins = min(matrix.shape[0], matrix.shape[1]) // bin_size
    cropped_matrix = matrix[:num_bins * bin_size, :num_bins * bin_size]
    
    binned_matrix = np.zeros((num_bins, num_bins))
    
    for i in range(num_bins):
        for j in range(num_bins):
            binned_matrix[i, j] = np.mean(cropped_matrix[i * bin_size:(i + 1) * bin_size, 
                                                        j * bin_size:(j + 1) * bin_size])
    return binned_matrix, num_bins

def calculate_spearman_per_window(matrix1, matrix2, num_bins):
    """Calculate Spearman correlation for each window"""
    spearman_correlations = []
    
    for i in range(num_bins):
        for j in range(num_bins):
            # Correlation for the specific bin (i, j)
            spearman_corr, _ = stats.spearmanr(matrix1[i, j], matrix2[i, j])
            spearman_correlations.append(((i, j), spearman_corr))
    
    return spearman_correlations

def load_matrix(file_path):
    """Load the matrix from a file with tab delimiter"""
    return np.loadtxt(file_path, delimiter='\t')

def main():
    parser = argparse.ArgumentParser(description="Compare 2D matrices using Spearman's correlation for each window.")
    parser.add_argument('--matrix1', type=str, required=True, help="Path to the first matrix file (CSV format).")
    parser.add_argument('--matrix2', type=str, required=True, help="Path to the second matrix file (CSV format).")
    parser.add_argument('--bin_size', type=int, default=100000, help="Size of the bins in base pairs.")
    
    args = parser.parse_args()
    
    # Load matrices
    matrix1 = load_matrix(args.matrix1)
    matrix2 = load_matrix(args.matrix2)
    
    # Bin the matrices
    binned_matrix1, num_bins = bin_matrix(matrix1, args.bin_size)
    binned_matrix2, _ = bin_matrix(matrix2, args.bin_size)
    
    # Calculate Spearman correlation for each window
    spearman_correlations = calculate_spearman_per_window(binned_matrix1, binned_matrix2, num_bins)
    
    # Print results
    for window, spearman_corr in spearman_correlations:
        print(f"Window {window}: Spearman correlation = {spearman_corr}")

if __name__ == '__main__':
    main()

