sklearn-rri
===========

Python package providing scikit-learn compatible classifier based on Reflective
Random Indexing (RRI) [1].

Documentation
-------------
The documentation is hosted on http://sklearn-rri.readthedocs.io/

Installation
------------
Latest from the `source <https://github.com/cmick/sklearn-rri>`_::

    git clone https://github.com/cmick/sklearn-rri.git
    cd sklearn-rri
    python setup.py install

Using `PyPI <https://pypi.python.org/pypi/sklearn-rri>`_::

    pip install sklearn-rri

Dependencies
------------
sklearn-rri requires:

- NumPy (>= 1.11.0)
- SciPy (>= 0.16.0)
- scikit-learn (>= 0.17.0)

Examples
--------
.. code :: pycon

    >>> from sklearn_rri import ReflectiveRandomIndexing
    >>> from sklearn.random_projection import sparse_random_matrix
    >>> X = sparse_random_matrix(100, 100, density=0.01, random_state=42)
    >>> rri = ReflectiveRandomIndexing(50, random_state=42)
    >>> rri.fit(X)
    ReflectiveRandomIndexing(n_components=50, n_iter=3, norm=True,
            random_state=42, seed='auto')
    >>> rri.transform(X)
    <100x50 sparse matrix of type '<class 'numpy.float64'>'
            with 1154 stored elements in Compressed Sparse Row format>

References
----------
[1] Trevor Cohen, Roger Schaneveldt, and Dominic Widdows,, Reflective Random
Indexing and Indirect Inference: A Scalable Method for Discovery of Implicit
Connections, 2010. https://www.ncbi.nlm.nih.gov/pubmed/19761870