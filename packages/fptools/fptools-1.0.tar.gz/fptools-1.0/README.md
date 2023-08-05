Frequent Itemset Mining
=======================
A pure python implementation of the FP-growth [1] and FPmax [2] algorithm.

Installing
----------
To build and install:
```
$ python setup.py install
```


Usage
-----
To use from the command line:
```
$ python -m fptools -h
```

To use as a python library:
```
>>> import fptools as fp
>>> itemsets = [[1,2,5], [1,4,5]]
>>> fis = [iset for iset in fp.frequent_itemsets(itemsets, 2)]
>>> mfis = [iset for iset in fp.maximal_frequent_itemsets(itemsets, 2)]
>>> fis
[[1], [5], [1, 5]]
>>> mfis
[[5, 1]]
```


Tests
-----
To run tests:
```
$ python test.py
```


Future Plans
------------
* A more complete set tests.
* Including the support levels of the output itemsets.
* Unrolling recursion and adding multithreading support.
* Adding closed itemset mining.


References
----------
[1] Han, Jiawei, Jian Pei, and Yiwen Yin. "Mining frequent patterns without candidate generation." ACM SIGMOD Record. Vol. 29. No. 2. ACM, 2000.

[2] Grahne, Gösta, and Jianfei Zhu. "High performance mining of maximal frequent itemsets." 6th International Workshop on High Performance Data Mining. 2003.
