# 3D divergence index with Spearman's correlation

### References:
[Reconstructing the 3D genome organization of Neanderthals reveals that chromatin folding shaped phenotypic and sequence divergence]
- [github]

[Machine learning reveals the diversity of human 3D
2 chromatin contact patterns]

[Reconstructing the 3D genome organization of Neanderthals reveals that chromatin folding shaped phenotypic and sequence divergence]: https://www.biorxiv.org/content/10.1101/2022.02.07.479462v1.full
[github]: https://github.com/emcarthur/neanderthal-3D-genome/tree/main
[Machine learning reveals the diversity of human 3D
2 chromatin contact patterns]: https://www.biorxiv.org/content/10.1101/2023.12.22.573104v1

### Scripts:
- compare_straw_files.py: Spearman's correlation for genomic windows
- compare_straw_files_sparse.py: adjusted for sparse data
- capra_spearman_mydata.py: Spearman calculated in a similar way to Capra Neanderthal 3D genome paper
- compare_straw_files_sparse.py: adjusted for sparse data
- check_sparsity.py: check if the data of each window is too sparse
- make_toy_hicdata.py: make not sparse toy data

### Input
Input was generated using [Straw] to extract flattened matrix from .hic files generated with [HiC-Pro].

[Straw]: https://github.com/aidenlab/straw
[HiC-Pro]: https://github.com/nservant/HiC-Pro
