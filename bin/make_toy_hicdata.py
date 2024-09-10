import numpy as np
import random

def generate_toy_data(output_file, chrom_length, resolution, sparsity=0.3):
    """
    Generates toy Hi-C-like data with enough variation and saves it in a straw-like format (row, col, value).
    
    Args:
        output_file (str): The path where the toy data will be saved.
        chrom_length (int): The length of the chromosome in base pairs.
        resolution (int): The resolution (bin size) of the contact map.
        sparsity (float): The fraction of non-zero contacts in the matrix (between 0 and 1).
    """
    num_bins = chrom_length // resolution
    
    with open(output_file, 'w') as f:
        for i in range(num_bins):
            for j in range(i, num_bins):  # Only upper triangle due to symmetry
                if random.random() < sparsity:  # Randomly decide if there's a contact
                    # Generate more varied contact values
                    contact_value = np.random.choice([1, 2, 5, 10, 50, 100], p=[0.3, 0.2, 0.2, 0.1, 0.1, 0.1])
                    f.write(f"{i*resolution}\t{j*resolution}\t{contact_value}\n")

if __name__ == "__main__":
    # Parameters for toy data generation
    chrom_length = 1000000  # Length of the chromosome in base pairs (1Mb for toy data)
    resolution = 100000     # Resolution (100kb bins)
    
    # Generate toy data for two samples with more variation
    generate_toy_data('toy_sample1.txt', chrom_length, resolution, sparsity=0.3)
    generate_toy_data('toy_sample2.txt', chrom_length, resolution, sparsity=0.3)

