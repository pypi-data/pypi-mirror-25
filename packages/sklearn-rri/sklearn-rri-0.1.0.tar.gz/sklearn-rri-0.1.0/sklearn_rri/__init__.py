"""
scikit-learn compatible classifier based on Reflective Random Indexing.

Installation
------------
Latest from the `source <https://github.com/cmick/sklearn-rri>`_::

    git clone https://github.com/cmick/sklearn-rri.git
    cd sklearn-rri
    python setup.py install

Using `PyPI <https://pypi.python.org/pypi/sklearn-rri>`_::

    pip install sklearn-rri

Usage example
-------------
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
Reflective Random Indexing and Indirect Inference:
    A Scalable Method for Discovery of Implicit Connections,
    Trevor Cohen, Roger Schaneveldt, and Dominic Widdows, 2010.
    https://www.ncbi.nlm.nih.gov/pubmed/19761870
"""
from ._version import __version__
from .rri import ReflectiveRandomIndexing
