nanomath
========

This module provides a few simple math and statistics functions for
other scripts processing Oxford Nanopore sequencing data

|Twitter URL| |install with conda| |Build Status| |Code Health|

FUNCTIONS
---------

-  Calculate read N50 from a set of lengths ``getN50(readlenghts)``
-  Remove extreme length outliers from a dataset
   ``removeLengthOutliers(dataframe, columname)``
-  Calculate the average Phred quality of a read ``aveQual(qualscores)``
-  Write out the statistics report after calling readstats function
   ``writeStats(dataframe, outputname)``
-  Compute a number of statistics, return a dictionary
   ``readstats(dataframe)``

INSTALLATION
------------

.. code:: bash

    pip install nanomath

| or
| |install with conda|

::

    conda install -c bioconda nanomath

STATUS
------

|Build Status| |Code Health|

.. |Twitter URL| image:: https://img.shields.io/twitter/url/https/twitter.com/wouter_decoster.svg?style=social&label=Follow%20%40wouter_decoster
   :target: https://twitter.com/wouter_decoster
.. |install with conda| image:: https://anaconda.org/bioconda/nanomath/badges/installer/conda.svg
   :target: https://anaconda.org/bioconda/nanomath
.. |Build Status| image:: https://travis-ci.org/wdecoster/nanomath.svg?branch=master
   :target: https://travis-ci.org/wdecoster/nanomath
.. |Code Health| image:: https://landscape.io/github/wdecoster/nanomath/master/landscape.svg?style=flat
   :target: https://landscape.io/github/wdecoster/nanomath/master
