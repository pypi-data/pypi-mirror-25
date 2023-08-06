import numpy as np
from sklearn.utils.estimator_checks import check_estimator
from sklearn.random_projection import gaussian_random_matrix
from sklearn_rri.rri import ReflectiveRandomIndexing


def test_classifier():
    return check_estimator(ReflectiveRandomIndexing)


def test_rri():
    x = gaussian_random_matrix(100, 1, random_state=42)
    rri = ReflectiveRandomIndexing(random_state=42)
    x_transformed = rri.inverse_transform(rri.fit_transform(x))
    assert np.allclose(abs(x), abs(x_transformed))
