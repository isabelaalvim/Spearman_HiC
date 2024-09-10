#!/usr/bin/env python

import argparse
import numpy as np
from scipy import stats

def read_straw_output(file_path, resolution, start, end):
    """
    Reads the straw output from a text file and converts it into a sparse matrix format.
    The file is expected to have three columns: row, col, and contact_value.
    """
    print(f"Reading contact matrix from {file_path} for region {start}-{end} at {resolution} resolution...")
    
    # Initialize a 2D numpy array to hold the contact matrix data
    size = (end - start) // resolution
    contact_matrix = np.zeros((size, size))
    
    # Read the file and fill the matrix
    with open(file_path, 'r') as f:
        for line in f:
            row, col, value = line.strip().split()
            row = int(row)
            col = int(col)
            value = float(value)
            
            # Adjust row/col indices to the matrix's start position and resolution
            row_idx = (row - start) // resolution
            col_idx = (col - start) // resolution
            
            # Fill in the matrix
            if 0 <= row_idx < size and 0 <= col_idx < size:
                contact_matrix[row_idx, col_idx] = value
    
    return contact_matrix

def compute_spearman(matrix1, matrix2, threshold=3):
    """
    Computes the Spearman correlation between two flattened contact matrices.
    Skips correlation calculation if one or both matrices contain too few non-zero values.
    """
    matrix1_flat = matrix1.flatten()
    matrix2_flat = matrix2.flatten()

    # Remove zero-contact entries
    valid_idx = (matrix1_flat > 0) & (matrix2_flat > 0)
    matrix1_filtered = matrix1_flat[valid_idx]
    matrix2_filtered = matrix2_flat[valid_idx]

    # Check if there are enough valid points for correlation calculation
    if len(matrix1_filtered) < threshold or len(matrix2_filtered) < threshold:
        return np.nan  # Return NaN if not enough data points
    
    # Compute Spearman correlation
    spearman_corr, _ = stats.spearmanr(matrix1_filtered, matrix2_filtered)
    return spearman_corr

def process_chromosome(file1, file2, resolution, chrom_length, bin_size, output_file, threshold=3):
    """
    Processes the entire chromosome by dividing it into bins and computing
    the Spearman correlation for each bin. Results are written to a text file.
    """
    with open(output_file, 'w') as out_file:
        out_file.write("Start\tEnd\tSpearmanCorrelation\n")
        
        # Iterate through chromosome in bins
        for start in range(0, chrom_length, bin_size):
            end = start + bin_size
            if end > chrom_length:
                end = chrom_length

            print(f"Processing bin: {start}-{end}")
            
            try:
                # Read straw output and convert to matrices
                matrix1 = read_straw_output(file1, resolution, start, end)
                matrix2 = read_straw_output(file2, resolution, start, end)

                # Compute Spearman correlation
                spearman_corr = compute_spearman(matrix1, matrix2, threshold)
                print(f"Spearman correlation for bin {start}-{end}: {spearman_corr}")

                # Write the result to the file
                out_file.write(f"{start}\t{end}\t{spearman_corr}\n")
            except Exception as e:
                print(f"Error processing bin {start}-{end}: {e}")
                out_file.write(f"{start}\t{end}\tError\n")

def main(args):
    # Set the default bin size to the resolution if not specified
    if args.bin_size is None:
        args.bin_size = args.resolution
    
    # Process the chromosome and output results
    process_chromosome(args.file1, args.file2, args.resolution, args.chrom_length, args.bin_size, args.output, args.threshold)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare contact maps from two straw output files across the entire chromosome using Spearman correlation.")
    parser.add_argument("--file1", required=True, help="Path to the first straw output text file")
    parser.add_argument("--file2", required=True, help="Path to the second straw output text file")
    parser.add_argument("--resolution", type=int, required=True, help="Resolution of the contact maps (e.g., 10000 for 10kb resolution)")
    parser.add_argument("--chrom_length", type=int, required=True, help="Length of the chromosome in base pairs")
    parser.add_argument("--bin_size", type=int, help="Size of each bin in base pairs (default: same as resolution)")
    parser.add_argument("--output", required=True, help="Output text file to write the Spearman correlations for each bin")
    parser.add_argument("--threshold", type=int, default=3, help="Minimum number of non-zero contact values for correlation calculation")
    
    args = parser.parse_args()
    main(args)

