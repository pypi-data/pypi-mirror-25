.. image:: https://travis-ci.org/Y-oHr-N/kenchi.svg?branch=master
    :target: https://travis-ci.org/Y-oHr-N/kenchi

.. image:: https://ci.appveyor.com/api/projects/status/5cjkl0jrxo7gmug0/branch/master?svg=true
    :target: https://ci.appveyor.com/project/Y-oHr-N/kenchi/branch/master

.. image:: https://coveralls.io/repos/github/Y-oHr-N/kenchi/badge.svg?branch=master
    :target: https://coveralls.io/github/Y-oHr-N/kenchi?branch=master

.. image:: https://codeclimate.com/github/Y-oHr-N/kenchi/badges/gpa.svg
    :target: https://codeclimate.com/github/Y-oHr-N/kenchi

.. image:: https://badge.fury.io/py/kenchi.svg
    :target: https://badge.fury.io/py/kenchi

.. image:: https://readthedocs.org/projects/kenchi/badge/?version=latest
    :target: http://kenchi.readthedocs.io/en/latest/?badge=latest

kenchi
======

This is a set of python modules for anomaly detection.

Requirements
------------

-  Python (>=3.5)
-  matplotlib (>=2.0.2)
-  numpy (>=1.11.2)
-  pandas (>=0.20.3)
-  scipy (>=0.18.1)
-  scikit-learn (>=0.18.0)

Installation
------------

You can install via pip.

::

    pip install kenchi

Usage
-----

.. code:: python

    >>> import numpy as np
    >>> from kenchi.outlier_detection import GaussianOutlierDetector
    >>> train_size   = 1000
    >>> test_size    = 100
    >>> n_outliers   = 10
    >>> n_features   = 10
    >>> rnd          = np.random.RandomState(0)
    >>> mean         = np.zeros(n_features)
    >>> cov          = np.eye(n_features)
    >>> # Generate the training data
    >>> X_train      = rnd.multivariate_normal(
    ...     mean     = mean,
    ...     cov      = cov,
    ...     size     = train_size
    ... )
    >>> # Generate the test data that contains outliers
    >>> X_test       = np.concatenate((
    ...     rnd.multivariate_normal(
    ...         mean = mean,
    ...         cov  = cov,
    ...         size = test_size - n_outliers
    ...     ),
    ...     rnd.uniform(-10.0, 10.0, size=(n_outliers, n_features))
    ... ))
    >>> # Fit the model according to the given training data
    >>> det          = GaussianOutlierDetector().fit(X_train)
    >>> # Detect if a particular sample is an outlier or not
    >>> det.detect(X_test)
    array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1], dtype=int32)

License
-------

The MIT License (MIT)

Copyright (c) 2017 Kon
