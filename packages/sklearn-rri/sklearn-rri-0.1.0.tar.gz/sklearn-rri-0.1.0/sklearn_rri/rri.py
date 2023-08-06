"""Reflective Random Indexing (RRI) algorithm implementation."""
import math
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import normalize
from sklearn.random_projection import sparse_random_matrix
from sklearn.utils.extmath import safe_sparse_dot
from sklearn.utils.validation import check_array, check_random_state, \
    check_is_fitted


class ReflectiveRandomIndexing(BaseEstimator, TransformerMixin):
    """
    Dimensionality reduction using Reflective Random Indexing (RRI).

    This transformer performs dimensionality reduction by means of RRI.
    It can work both with numpy.ndarray and scipy.sparse matrices efficiently.

    Parameters
    ----------
    n_components : int, default = None
        Desired dimensionality of output data.
        if n_components is not set all components are kept::

            n_components == min(n_samples, n_features)

    n_iter : int, default = 3
        Number of iterations (aka reflections) to be performed.

    seed : int, default = 'auto'
        Random indexing seed value (number of non-zero values in every index
        vector). If seed = 'auto', the value is set to sqrt(n_features).

    norm : bool, default = True
        Indicates whether the context vectors should be normalized after every
        reflection step.

    dense_components : bool, default = False
        Indicates whether the estimated components matrix should be sparse (by
        default) or dense.

    random_state : int or RandomState instance, default = None
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    Attributes
    ----------
    components_ : array, shape (n_components, n_features)
        Estimated components.

    References
    ----------
    Reflective Random Indexing and Indirect Inference:
        A Scalable Method for Discovery of Implicit Connections,
        Trevor Cohen, Roger Schaneveldt, and Dominic Widdows, 2010.
        https://www.ncbi.nlm.nih.gov/pubmed/19761870

    Examples
    --------
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
    """

    def __init__(self, n_components=None, n_iter=3, seed='auto', norm=True,
                 dense_components=False, random_state=None):
        self.n_components = n_components
        self.n_iter = n_iter
        self.seed = seed
        self.norm = norm
        self.dense_components = dense_components
        self.random_state = random_state

    def fit(self, X, y=None):
        """Fit RRI model on training data X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Training data, where n_samples in the number of samples and
            n_features is the number of features.
        y : (ignored)

        Returns
        -------
        self : object
            Returns the transformer object.
        """
        X = check_array(X, accept_sparse='csr')
        random_state = check_random_state(self.random_state)
        if self.seed == 'auto':
            seed = round(math.sqrt(X.shape[1]))
        elif isinstance(self.seed, int) and self.seed > 0:
            seed = self.seed
        else:
            raise ValueError("seed parameter must be a non-negative integer.")
        if self.n_components is None:
            n_components = min(X.shape)
        elif isinstance(self.n_components,
                        (int, np.integer)) and self.n_components > 0:
            n_components = self.n_components
        else:
            raise ValueError("n_components parameter must be a non-negative "
                             "integer.")

        # generate index vectors
        if self.n_iter % 2 == 0:
            v_components = sparse_random_matrix(X.shape[1], n_components,
                                                density=1 / seed,
                                                random_state=random_state)
            if self.dense_components:
                v_components = v_components.toarray()
            u_components = None
        else:
            u_components = sparse_random_matrix(X.shape[0], n_components,
                                                density=1 / seed,
                                                random_state=random_state)
            if self.dense_components:
                u_components = u_components.toarray()
            v_components = None

        # reflectively train context vectors
        for _ in range(self.n_iter):
            if v_components is None:
                v_components = safe_sparse_dot(X.T, u_components)
                u_components = None
                if self.norm:
                    normalize(v_components, copy=False)
            else:
                u_components = safe_sparse_dot(X, v_components)
                v_components = None
                if self.norm:
                    normalize(u_components, copy=False)

        self.components_ = v_components
        return self

    def transform(self, X):
        """Perform dimensionality reduction on X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            New data, where n_samples in the number of samples and
            n_features is the number of features.

        Returns
        -------
        X_new : array, shape (n_samples, n_components)
            Reduced version of X. This will always be a dense array.
        """
        check_is_fitted(self, ['components_'])
        X = check_array(X, accept_sparse='csr')
        return safe_sparse_dot(X, self.components_)

    def inverse_transform(self, X):
        """Transform X back to its original space.

        Returns an array X_original whose transform would be X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_components)
            New data, where n_samples in the number of samples and
            n_features is the number of features.

        Returns
        -------
        X_original : array, shape (n_samples, n_features)
            Note that this is always a dense array.
        """
        check_is_fitted(self, ['components_'])
        X = check_array(X, accept_sparse='csr')
        return safe_sparse_dot(X, self.components_.T)
