from sklearn.base import BaseEstimator, TransformerMixin


class ItemSelector(BaseEstimator, TransformerMixin):
    """Select features from dataset

    Parameters
    ----------
    indices : array-like
        Fancy indices which will be applied to the input vector.
    """

    def __init__(self, indices):
        self.indices = indices

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[:, self.indices]