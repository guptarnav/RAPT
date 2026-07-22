import numpy as np

def fit_static_ols(x, y):
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    X = np.column_stack((x_arr, np.ones(len(x_arr))))
    beta, alpha = np.linalg.solve(X.T @ X, X.T @ y_arr)
    return beta, alpha