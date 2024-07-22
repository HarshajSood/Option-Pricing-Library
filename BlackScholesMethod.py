from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame

"""
S - current price of underlying asset
K - strike price of underlying asset
T - time to maturity/expiry (in years)
r - continuous compounding risk free interest rate
v - implied volatility

N() - Normal Distribution
N(d1) - the probability of receiving the underlying asset at option expiration 
N(d2) - Risk adjusted probability that the option will be exercised

First Order Greeks
Delta - sensitivity of the value of the derivative to the underlying price
Theta - sensitivity of the value of the derivative to the passage of time 
Vega - sensitivity of the value of the derivative to the volatility
Rho - sensitivity of the value of the derivative to the interest rate

Second Order Greeks
Gamma -  the rate of change in the delta with respect to changes in the underlying price
Vanna -  the rate of change in the delta with respect to changes in the volatility
Volga - the rate of change of volga with respect to the volatility (second order senstivity)
"""
def d1(S,K,T,r,v):
    return(log(S/K)+(r+v**2/2.)*T)/v*sqrt(T)
def d2(S,K,T,r,v):
    return d1(S,K,T,r,v)-v*sqrt(T)

def blackScholesCall(S,K,T,r,v):
    return S*norm.cdf(d1(S,K,T,r,v))-K*exp(-r*T)*norm.cdf(d2(S,K,T,r,v))
def blackScholesPut(S,K,T,r,v):
    return K*exp(-r*T)-S+bs_call(S,K,T,r,v)

## define the First Order Call Greeks
def callDelta(S,K,T,r,v):
    return norm.cdf(d1(S,K,T,r,v))
def callVega(S,K,T,r,v):
    return 0.01*(S*norm.pdf(d1(S,K,T,r,v))*sqrt(T))
def callTheta(S,K,T,r,v):
    return 0.01*(-(S*norm.pdf(d1(S,K,T,r,v))*v)/(2*sqrt(T)) - r*K*exp(-r*T)*norm.cdf(d2(S,K,T,r,v)))
def callRho(S,K,T,r,v):
    return 0.01*(K*T*exp(-r*T)*norm.cdf(d2(S,K,T,r,v)))

## define Second Order Call Greeks
def callGamma(S,K,T,r,v):
    return norm.pdf(d1(S,K,T,r,v))/(S*v*sqrt(T))

## Define First Order Put Greeks
def putDelta(S,K,T,r,v):
    return -norm.cdf(-d1(S,K,T,r,v))
def putVega(S,K,T,r,v):
    return 0.01*(S*norm.pdf(d1(S,K,T,r,v))*sqrt(T))
def putTheta(S,K,T,r,v):
    return 0.01*(-(S*norm.pdf(d1(S,K,T,r,v))*v)/(2*sqrt(T)) + r*K*exp(-r*T)*norm.cdf(-d2(S,K,T,r,v)))
def putRho(S,K,T,r,v):
    return 0.01*(-K*T*exp(-r*T)*norm.cdf(-d2(S,K,T,r,v)))
## Define Second Order Put Greeks
def putGamma(S,K,T,r,v):
    return norm.pdf(d1(S,K,T,r,v))/(S*v*sqrt(T))