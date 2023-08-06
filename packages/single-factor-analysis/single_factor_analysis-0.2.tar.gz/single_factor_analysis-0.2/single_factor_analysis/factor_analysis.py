import warnings
import numpy as np

def single_factor_analysis(X, k=5, cycles=100, tol=.001):
    """ Fit Factor Analysis model using EM

    Iterative Expectation-Maximization algorithm that stops once
    a proportional change less than the specified tolerance in
    the log likelihood or the specified number of cycles has been
    reached. Return matrices are strictly real-valued.

    Parameters
    ----------
    X : array_like, shape (n_samples, n_features)
        A 2-D data matrix real-valued
    k : int, optional
        Number of factors (default 5)
    cycles : int, optional
        Maximum number of cycles of EM (default 100)
    tol : float, optional
        Tolerance value (default 0.001)

    Returns
    -------
    Lambda : array_like
        A 2-D ndarray containing the factor loading matrix (Lambda)
    Psi : array_like
        A 2-D ndarray containing the diagonal uniquenesses matrix
    lkhd_list : list
        List of log likelihood values during iterations.
        Generally follows a positive logarithmic curve. 

    Notes
    -----
    Based upon the algorithm initially described in:
    http://www.cs.toronto.edu/~fritz/absps/tr-96-1.pdf

    """

    n_samples, n_features = X.shape

    # X assumed to be zero mean 
    row_mean = np.mean(X, axis=0)
    X -= row_mean[np.newaxis, :] # subtract mean of row
    # X'*X followed by element-wise division by n_samples
    XX = X.T.dot(X) / n_samples
    XX_diag = np.diag(XX)

    cov_X = np.cov(X, rowvar=False) #shape n_features by n_features
    scale = np.linalg.det(cov_X) ** (1 / n_features)
    Psi = np.diag(cov_X)

    # Start Lambda at random values
    Lambda = np.random.randn(n_features, k) * np.sqrt(scale / k)

    I = np.eye(k)

    const = -n_features / 2 * np.log(2 * np.pi)

    log_lkhd = 0 
    lkhd_list = []
    for i in range(cycles):
        # compute expectation
        Psi_diag = np.diag(1 / Psi) # diag of element-wise ** -1
        PsiLambda = Psi_diag.dot(Lambda)
        # solve matrix inversion
        M = Psi_diag - PsiLambda.dot(np.linalg.inv(I +\
                Lambda.T.dot(PsiLambda))).dot(PsiLambda.T)
        M_det = np.sqrt(np.linalg.det(M))
        Beta = Lambda.T.dot(M)
        # first moment of factors
        XXBeta_prime = XX.dot(Beta.T) 
        # compute second moment of factors
        ZZ = I - Beta.dot(Lambda) + Beta.dot(XXBeta_prime)

        # compute log likelihood 
        last_log_lkhd = log_lkhd
        log_lkhd = n_samples * const + n_samples * np.log(M_det) - 0.5 * n_samples * np.sum(np.diag(M.dot(XX)))
        lkhd_list.append(log_lkhd)

        # compute maximization 
        # update Lambda
        Lambda = XXBeta_prime.dot(np.linalg.inv(ZZ))
        # update Psi
        Psi = XX_diag - np.diag(Lambda.dot(XXBeta_prime.T))

        if i == 0:    
            log_lkhd_init = log_lkhd
        elif (log_lkhd < last_log_lkhd):     
            warnings.warn('Local decrease in log likelihood')
        elif ((log_lkhd - log_lkhd_init) < (1 + tol) *\
                (last_log_lkhd - log_lkhd_init)):
            break
    else:
        warnings.warn('Factor analysis did not converge for tol : %.4f, you may want to increase the cycles' % tol)

    return Lambda, Psi, lkhd_list

