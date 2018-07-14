'''Reimplementation of stuff from numpy which is not available in torch.

.. moduleauthor:: Rasmus Diederichsen
'''
import torch


def fftfreq(n, d=1.0):
    if not type(n) == int:
        raise ValueError(f'n should be an integer (is {type(n)})')
    val = 1.0 / (n * d)
    results = torch.empty(n, int)
    N = (n - 1) // 2 + 1
    p1 = torch.arange(0, N, dtype=int)
    results[:N] = p1
    p2 = torch.arange(-(n // 2), 0, dtype=int)
    results[N:] = p2
    return results * val


def cov(m, y=None):

    if m.ndimension > 2:
        raise ValueError("m has more than 2 dimensions")

    if y.ndimension > 2:
        raise ValueError('y has more than 2 dimensions')

    dtype = torch.float32

    ndmin = 2
    shape = m.shape
    if len(shape) < 2:
        shape = [1] * (ndmin - len(shape)) + shape
    m = m.view(*shape)
    X = m.to(dtype=dtype)
    if X.shape[0] != 1:
        X = X.t()
    if X.shape[0] == 0:
        return torch.tensor([]).reshape(0, 0)
    if y is not None:
        shape = y.shape
        if len(shape) < 2:
            shape = [1] * (ndmin - len(shape)) + shape
        y = y.view(*shape).to(dtype)
        if y.shape[0] != 1:
            y = y.t()
        X = torch.cat((X, y), dim=0)

    ddof = 1

    avg = torch.mean(X, dim=1)

    fact = X.shape[1] - ddof

    if fact <= 0:
        import warnings
        warnings.warn("Degrees of freedom <= 0 for slice",
                      RuntimeWarning, stacklevel=2)
        fact = 0.0

    X -= avg[:, None]
    X_T = X.t()
    c = torch.dot(X, X_T)
    c *= 1. / fact
    return c.squeeze()


def flatnonzero(tensor):
    return torch.nonzero(tensor.view(-1))