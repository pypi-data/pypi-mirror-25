from matplotlib import pyplot as plt
import numpy as np
from brmbs.model.OrthogonalRegression import *

def simulate_poly_fit(poly, poly_1st_derivative, degree_of_data, degree_of_fit, start = -20, end = 20, step = 0.01, noise_loc = 0, noise_scale = 5, window = 200):
    x = np.arange(start, end, step)
    y = poly(x)
    yn = y + np.random.normal(loc = noise_loc, scale = noise_scale, size = len(x))  # generate data with noise

    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot(111)
    ax.plot(x, y, c = 'orange')
    ax.scatter(x, yn, s = 0.3, c = 'green')
    ax.set_title('Plot 1 : Original Data')
    
    # transform X to orthogonal basis
    reg_X, a, b = orth_base(norm_base(x), degree_of_data)
    coef = np.array(fitting_OLS(yn, reg_X))
    yt = np.sum(coef * reg_X, axis = 1)
    
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot(111)
    ax.plot(x, y, c = 'orange')
    ax.scatter(x, yt, s = 0.3, c = 'green')
    ax.set_title('Plot 2 : Fit entire data with polynomial regression')
    
    # fit data with rolling window
    pure_X = x
    pure_Y = yn
    
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot(111)
    ax.plot(x, y, c = 'orange', label = 'Theoretical value')
    for i in range((len(pure_X) - window)):
        reg_X = pure_X[i:i + window]
        reg_Y = pure_Y[i:i + window]
        reg_X_new, a, b = orth_base(norm_base(reg_X), degree_of_fit)
        coef = np.array(fitting_OLS(reg_Y, reg_X_new))
        fitted_Y = reg_X_new.dot(coef.reshape(-1, 1))
        ax.plot(reg_X, fitted_Y, c = 'green', alpha = 0.01)
    ax.set_title('Plot 3 : Rolling window fitted data vs. Theoretical value ')
    ax.legend()
    
    # test duration (first derivative) generated from orthogonal regression
    d = poly_1st_derivative(x)
    
    dt = regression_poly_wind(window, x, yn, degree_of_fit, duration_from_ortho_poly_fit, X_transformed = False, calc_derivative = True)

    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot(111)
    ax.plot(x, d, c = 'orange', label = 'Theoretical Duration')
    ax.scatter(x[window:], dt, s = 0.3, c = 'green', label = 'Fitted Duration')
    ax.set_title('Plot 4 : Theoretical Duration vs. Fitted Duration... ')
    ax.legend()