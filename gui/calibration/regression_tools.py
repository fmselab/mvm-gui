import numpy as np

def check_data(x, y, cov_th=10):
    '''
    Checks if the data has a covariance 
    bigger than cov_th, and returns the 
    data split in x and y
    
    arguments:
    - x: a list with the data x values
    - y: a list with the data y values
    - cov_th: threshold to use for the covariance
    
    returns:
    True if the covariance condition is satisfied
    '''
    
    cov = np.cov(x,y)
    print(cov)
    
    if np.abs(cov[1,1]) > cov_th and np.abs(cov[0,1]) > cov_th:
        return True  

    return False

def data_regression(x, y, deg=4, full=True):
    '''
    Performs the data regression with a 
    polynomial of order deg.
    
    arguments:
    - x: a list with the data x values
    - y: a list with the data y values
    - deg: the order of the polynomial
    
    returns:
    - a list with the polynomial coefficients
    - the chi squared
    - the p-value
    '''
    if check_data(x, y):
        coeff = np.polyfit(x, y, deg=deg)
        print(coeff)
        chi_squared = np.sum((np.polyval(coeff, x) - y) ** 2)
        # p_value = 1 - stats.chi2.cdf(chi_squared, len(x)-deg)

        if full: return np.flip(coeff), chi_squared
        else:    return np.flip(coeff)
    else:
        return []