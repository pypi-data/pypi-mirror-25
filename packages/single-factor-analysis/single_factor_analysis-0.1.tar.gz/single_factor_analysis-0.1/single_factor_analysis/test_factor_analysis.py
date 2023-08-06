from factor_analysis import *

def test_single_factor_analysis():
    X = np.random.rand(10, 20)
    k = 10
    L, Ph, LL = single_factor_analysis(X, k=k)

