# Quality Change: norm or exception? Measurement, Analysis and Detection of Quality Change in Wikipedia

This work sheds light on English Wikipedia article quality life cycle from the perspective of quality classes (i.e., FA, A, GA, B, C, Start and Stub) and proposes a novel unsupervised page level approach to detect quality switch, which further can help in automatic content monitoring in Wikipedia. The work is published in the 25th ACM Conference On Computer-Supported Cooperative Work And Social Computing (CSCW), 2022.

### Organization of the folder ###

1. Extract Revision History- The folder contains codes for downloading complete revision history and corresponding quality classes of Wikipedia articles and their talk pages.
2. Sample Dataset- The folder includes the list of features as described in the paper for a sample set of Wikipedia articles.
3. CPD algorithms- The folder enlists codes for implementing different Change Point Detection (CPD) algorithms.
4. ORES analysis- The folder contains codes for comparing the quality change points as detected by ORES with our proposed method of CPD algorithms for the same.


### To generate output ###

Please look into the individual folders for running the codes and producing results. 

If you find this work helpful in your research then please cite 

```
@article{10.1145/3512959,
author = {Das, Paramita and Guda, Bhanu Prakash Reddy and Seelaboyina, Sasi Bhushan and Sarkar, Soumya and Mukherjee, Animesh},
title = {Quality Change: Norm or Exception? Measurement, Analysis and Detection of Quality Change in Wikipedia},
year = {2022},
publisher = {Association for Computing Machinery},
volume = {6},
number = {CSCW1},
url = {https://doi.org/10.1145/3512959},
doi = {10.1145/3512959},
journal = {Proc. ACM Hum.-Comput. Interact.},
articleno = {112}
}

```

