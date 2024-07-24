from math import sqrt, exp
import numpy as np

"""
S - current price of underlying asset
K - strike price of underlying asset
T - time to maturity/expiry (in years)
r - continuous compounding risk free interest rate
v - implied volatility
N - maximum number of steps
OT - OptionType - Put = 1, Call = 2
"""

"""
u - The Factor by which the price rises assuming it rises
d - The Factor by which the price falls assuming it falls
m - The Fator by which price remains stable/ middle path 
pu - the probability of price rising
pd - the probability of price falling
pm - the probability of price remaining stable
disc - Discount Factor
"""

def dt(T,N):
    return T/N

def dx(T,v,N):
    return v*sqrt(dt(T,N))

def s2(r,v):
    return r- ((v**2)/2)

def discount(T,r,N):
    return exp(-r*dt(T,N))

#constant1
def c1(T,r,v,N):
    return (((v**2)*dt(T,N))+((s2(r,v)*dt(T/N))**2))/(dx(T,v,N)**2)
#constant2
def c2(T,r,v,N):
    return s2(r,v)*dt(T,N)/dx(T,v,N)

#Probabilities
def pu(T,r,v,N):
    return discount(T,r,N)*(1/2)*(c1(T,r,v,N)+c2(T,r,v,N))
def pm(T,r,v,N):
    return discount(T,r,N)*(1-c1(T,r,v,N))
def pd(T,r,v,N):
    return discount(T,r,N)*(1/2)*(c1(T,r,v,N)-c2(T,r,v,N))

def TrinomialTreeMethod(S,K,T,r,v,N,OT):
    steps = np.zeroes((2*N+1,1))
    steps[0] = s*exp(N*dx(T,v,N))
    for j in range(1, 2*N+1):
        steps[j] = exp(-dx(T,v,N))*steps[j-1]

    CPValues = np.zeroes((2*N+1, N+1))

    for j in range(0, 2*N+1):
        if OT==1:
            CPValues[j,N] = max(steps[j]-K, 0)
        elif OT==2:
            CPValues[j,N] = max(K-steps[j], 0)
    
    for j in range(N-1, -1, -1):
        for i in range(N-j, N+j+1):
            CPValues[i,j]=discount(T,r,N)*(pu(T,r,v,N)*CPValues[i-1,j+1]+pm(T,r,v,N)*CPValues[i,j+1]+pd(T,r,v,N)*CPValues[i+1,j+1])
    
    price = CPValues[N,0]
    return price


