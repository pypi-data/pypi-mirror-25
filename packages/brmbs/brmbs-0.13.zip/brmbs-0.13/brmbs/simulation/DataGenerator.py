import numpy as np
from numba import jit
from scipy.special import comb
import scipy.optimize as optimize


###################################################################

### Polynomial data generator

###################################################################

class TestFunctionGenerator():
    def __init__(self, coeffs):
        '''coeffs: highest order to lowest order'''
        self.coeffs = coeffs
        self.degree = len(coeffs) - 1
        
    def get_poly(self):
        def tmp(x):
            return (((x.reshape(-1, 1))**np.arange(self.degree, -1, -1)).dot(self.coeffs.reshape(-1, 1))).squeeze()
        return tmp
        
    def get_first_derivative(self):
        def tmp(x):
            weighted_coeffs = self.coeffs[:-1] * np.arange(self.degree, 0, -1)
            return (((x.reshape(-1, 1))**np.arange(self.degree - 1, -1, -1)).dot(weighted_coeffs.reshape(-1, 1))).squeeze()
        return tmp
		

###################################################################

### Binomial tree generator

###################################################################
		
#return interst rate of each node
@jit
def generateBTR(r0,drift,sigma,n,year): 
    n_level = n * year
    BT = np.zeros((n_level, n_level))
    BT[0][0] = r0
    deltaT=1/n
    for i in range(1, n_level):
        BT[:, i] = BT[:, i - 1] * np.exp(drift*deltaT+sigma*np.sqrt(deltaT))
        BT[i][i] = BT[i - 1][i - 1] * np.exp(drift*deltaT-sigma*np.sqrt(deltaT))
    return BT

#return discount rate between each deltaT
@jit
def generateBT(r0,drift,sigma,n,year): 
    BTR = generateBTR(r0,drift,sigma,n,year)
    deltaT=1/n
    return np.exp(-BTR*deltaT)

@jit
def discountedValue(BT,n):
    result = BT[:n, n - 1]
    for i in np.arange(n-1,0,-1):
        result = 0.5 * (result[:-1] + result[1:]) * BT[:i, i - 1]
    return result[0]

'''
r0=current continous conpouding short rate
drift,sigma=parameters in model
n=numer of steps in year
year=matirity
cFrq=how many times of coupon payment per year
c=coupon rate
principle=face value
'''
@jit
def vanillaBond(r0,drift,sigma,n,year,cFrq,c,principle):
    BT=generateBT(r0,drift,sigma,n,year)
    price=principle*discountedValue(BT,year*n) 
    for t in np.array(range(1,cFrq*year+1))/cFrq:
        price+=(c/cFrq)*principle*discountedValue(BT,int(t*n))  
    return price

@jit
def callableBond(r0,drift,sigma,n,year,cFrq,c,principle,callPrice,callTime):
    
    BTRt=generateBTR(r0,drift,sigma,n,callTime)
    BTt=generateBT(r0,drift,sigma,n,callTime)
    
    newR=BTRt[:, n*callTime - 1].squeeze()
    len_newR = len(newR)
    
    price=0
    count=0
    for r in newR:
        p1=min(vanillaBond(r,drift,sigma,n,year-callTime,cFrq,c,principle),callPrice)
        price+=p1*discountedValue(BTt,callTime*n)*comb(len_newR-1, count)/(2**(len(newR)-1))
        count+=1
        
    for t in np.arange(1,cFrq*callTime+1)/cFrq:
        price+=(c/cFrq)*principle*discountedValue(BTt,int(t*n))  
    return price

def ytm(price,c,principle,cFrq,year):
    
    freq = float(cFrq)
    periods = year*freq
    coupon = c*principle/cFrq
    dt = [(i+1)/freq for i in range(int(periods))]
    ytm_func = lambda y: sum([coupon/(1+y/freq)**(freq*t) for t in dt]) + principle/(1+y/freq)**(freq*year) - price
    
    return optimize.newton(ytm_func, 0.03)

def generateSimulatedBDTPrice(drift = 0.01, sigma = 0.4, n = 6, year = 30, cFrq = 2, c = 0.03, principle = 100, callPrice = 101, callTime = 3, start = 0, end = 0.2, step = 0.0001):
	y=[]
	price=[]
	priceC=[]
	for r in np.arange(0, 0.2, 0.0001):
		p=vanillaBond(r,drift,sigma,n,year,cFrq,c,principle)
		y.append(ytm(p,c,principle,cFrq,year))
		price.append(p)
		priceC.append(callableBond(r,drift,sigma,n,year,cFrq,c,principle,callPrice,callTime))
		
	return y, price, priceC