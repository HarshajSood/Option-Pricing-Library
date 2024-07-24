from math import log, sqrt, pi, exp
from scipy.stats import norm

"""
S - current price of underlying asset
K - strike price of underlying asset
T - time to maturity/expiry (in years)
r - continuous compounding risk free interest rate
q - dividend yield
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
def d1(S,K,T,r,q,v):
    return(log(S/K)+(r-q+v**2/2.)*T)/v*sqrt(T)
def d2(S,K,T,r,q,v):
    return d1(S,K,T,r,q,v)-v*sqrt(T)

def blackScholesCall(S,K,T,r,q,v):
    return exp(-q*T)*S*norm.cdf(d1(S,K,T,r,q,v))-K*exp(-r*T)*norm.cdf(d2(S,K,T,r,q,v))
def blackScholesPut(S,K,T,r,q,v):
    return K*exp(-r*T)*norm.cdf(-d2(S,K,T,r,q,v)) - exp(-q*T)*S*norm.cdf(-d1(S,K,T,r,q,v))


## First Order Greeks
def callDelta(S,K,T,r,q,v):
    return  exp(-q*T)*norm.cdf(d1(S,K,T,r,q,v))
def putDelta(S,K,T,r,q,v):
    return -exp(-q*T)*norm.cdf(-d1(S,K,T,r,q,v))
def Vega(S,K,T,r,q,v):
    return (S*norm.pdf(d1(S,K,T,r,q,v))*exp(-q*T)*sqrt(T))
def callTheta(S,K,T,r,q,v):
    return -(exp(-q*T)*S*norm.pdf(d1(S,K,T,r,q,v))*v)/(2*sqrt(T)) - r*K*exp(-r*T)*norm.cdf(d2(S,K,T,r,q,v))+q*exp(-q*T)*S*norm.cdf(d1(S,K,T,r,q,v))
def putTheta(S,K,T,r,q,v):
    return -(exp(-q*T)*S*norm.pdf(d1(S,K,T,r,q,v))*v)/(2*sqrt(T)) + r*K*exp(-r*T)*norm.cdf(-d2(S,K,T,r,q,v))-q*exp(-q*T)*S*norm.cdf(-d1(S,K,T,r,q,v))
def callRho(S,K,T,r,q,v):
    return K*T*exp(-r*T)*norm.cdf(d2(S,K,T,r,q,v))
def putRho(S,K,T,r,q,v):
    return -K*T*exp(-r*T)*norm.cdf(-d2(S,K,T,r,q,v))

## Second Order Greeks
def Gamma(S,K,T,r,q,v):
    return norm.pdf(d1(S,K,T,r,q,v))/(S*v*sqrt(T))
def Vanna(S,K,T,r,q,v):
    return -exp(-q*T)*norm.pdf(d1(S,K,T,r,q,v))*d2(S,K,T,r,q,v)/v
def Volga(S,K,T,r,q,v):
    return -exp(-q*T)*sqrt(T)*S*norm.pdf(d1(S,K,T,r,q,v))*d1(S,K,T,r,q,v)*d2(S,K,T,r,q,v)/v