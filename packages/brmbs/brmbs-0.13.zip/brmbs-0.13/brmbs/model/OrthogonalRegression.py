import numpy as np
import pandas as pd
import datetime as dt
import statsmodels.api as sm

import rpy2
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects import r
pandas2ri.activate()

def norm_base(x):
    return (2*x-np.min(x)-np.max(x))/(np.max(x)-np.min(x))
	
def orth_base(x_n,degree):
    #Creating matrix given the required degree
    Z=np.zeros((len(x_n), degree + 1))
    a=np.zeros(degree+1)
    b=np.zeros(degree)
    Z[:,0]=1
    b[0]=0
    a[0]=0
    a[1]=np.mean(x_n)
    Z[:,1]=2*(x_n-a[0])
    for i in range(2,degree+1):
        a[i-1]=np.sum(np.multiply(x_n,np.multiply(Z[:,i-1],Z[:,i-1])))/np.sum(np.multiply(Z[:,i-1],Z[:,i-1]))
        b[i-1]=np.sum(np.multiply(Z[:,i-1],Z[:,i-1]))/np.sum(np.multiply(Z[:,i-2],Z[:,i-2]))
        Z[:,i]=2*np.multiply((x_n-a[i-1]),Z[:,i-1])-b[i-1]*Z[:,i-2]
    return Z.squeeze(),a,b
	
def fitting_OLS(reg_Y,reg_X):
    mod = sm.OLS(reg_Y, reg_X)
    res = mod.fit()
    return res.params
	
def duration_from_ortho_poly_fit(X, Y, deg, rate, delta = 0.0001, X_transformed = True, calc_derivative = False):
    if not X_transformed:
        reg_X, a, b = orth_base(norm_base(X), deg)
    else:
        reg_X = X

    coef = np.array(fitting_OLS(Y, reg_X))

    rate_plus = rate + delta
    rate_minus = rate - delta
    
    x_plus,a,b = orth_base(np.array([rate_plus]), deg)
    x_minus,a,b = orth_base(np.array([rate_minus]), deg)
    
    price_plus = np.sum(coef * x_plus)
    price_minus = np.sum(coef * x_minus)

    sign = (1 if calc_derivative else -1)
    
    return sign * (price_plus - price_minus) / (delta * 2)

stats = importr('stats')
def duration_from_r_poly_fit(X, Y, deg, rate, delta = 0.001, X_transformed = True, calc_derivative = False):
    
    new_Y = pandas2ri.py2ri(Y)
    new_X = pandas2ri.py2ri(X)

    poly = stats.poly(new_X, degree=deg)
    df = pd.DataFrame(np.matrix(poly))
    new_df=pandas2ri.py2ri(df)

    ls_fit = r.lsfit(new_df, new_Y)
    coeff = np.array(ls_fit[0])
    
    coef = np.array(fitting_OLS(Y, X))
    
    rate_plus = rate + delta
    rate_minus = rate - delta
    
    price_plus = np.sum(coef * rate_plus**np.arange(deg + 1))
    price_minus = np.sum(coef * rate_minus**np.arange(deg + 1))
    
    return (1 if calc_derivative else -1) * (price_plus - price_minus) / (delta * 2)

def regression_poly_wind(wind, X, Y, deg, ploy_fit_func, X_transformed = True, calc_derivative = False):
    if(len(X) != len(Y)):
        raise Exception('X and Y should have same length')
    if(len(X) < wind):
        raise Exception('Rolling window size should be larger than data size')
    
    beta = []
    pure_X = X
    pure_Y = Y

    for i in range((len(X)-wind)):
        reg_X = pure_X[i:i + wind]
        reg_Y = pure_Y[i:i + wind]
        beta.append(ploy_fit_func(reg_X, reg_Y, deg, reg_X[-1], X_transformed = X_transformed, calc_derivative = calc_derivative))
        
    return beta
	
def calc_duration_method_1(collapse_without_order, TBAs):
	default_window = 60
	degree = 1

	poly_duration_without_order = {}
	for c, period_list in collapse_without_order.items():
		dat = TBAs[c]
		default_start_date = min(dat.index)
		
		cur_list = []
		for p in period_list:
			window = default_window
			
			reg_start_date = p.startDate - dt.timedelta(days = window)
			if reg_start_date < default_start_date:
				reg_start_date = default_start_date
			
			rolling_period = len(dat[reg_start_date:p.endDate]['price'])
			if rolling_period < window:
				window = rolling_period // 2 + 1
			
			
			rates_raw = dat[reg_start_date:p.endDate]['MTGFNCL']
			
			# version 1 of poly fit: see above
			
			# normalize X
			rates = norm_base(rates_raw)
			# transform X to orthogonal basis
			reg_X, a, b = orth_base(rates, degree)
			betas = regression_poly_wind(window, reg_X, dat[reg_start_date:p.endDate]['price'], degree, duration_from_ortho_poly_fit)
			cur_list.append(pd.DataFrame({'Duration': betas}, index = rates.index[window:]))
			
			cur_list.append(pd.DataFrame({'Duration': betas}, index = rates_raw.index[window:]))
			
		poly_duration_without_order[c] = cur_list
		
	return poly_duration_without_order