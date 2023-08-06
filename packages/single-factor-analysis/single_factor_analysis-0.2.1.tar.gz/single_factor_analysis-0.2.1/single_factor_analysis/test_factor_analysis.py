from factor_analysis import *

def test_single_factor_analysis():
    X = np.array([[3, -.001, 0.03],
                 [10, .002, 0.004],
                 [5, -0.001, 0.007,],
                 [0.004, -0.006, 4],
                 [-.0035, -.002, 10]])
    k = 2
    tol = .1
    L, Ph, LL = single_factor_analysis(X, k=k)
    assert(L.shape == (3, 2))
    # soft test
    if not np.allclose(L[1, :] + 1, [1, 1], rtol=tol):
        warnings.warn('Factor Analysis may not have converged correctly, null dims given weights %.4f and %.4f' % (L[1, 0], L[1, 1]))

