from math import sqrt, exp

"""
S - current price of underlying asset
K - strike price of underlying asset
T - time to maturity/expiry (in years)
r - continuous compounding risk free interest rate
v - implied volatility
N - maximum number of steps
putCall - Put = 1, Call = 2

"""
"""
u - The Factor by which the price rises assuming it rises
d - The Factor by which the price falls assuming it falls
pu - the probability of price rising
pd - the probability of price falling
disc - Discount Factor
"""
def u(T,v,N):
    return exp(v*sqrt(T/N))
def d(T,v,N):
    return 1/u(T,v,N)
def pu(T,r,v,N):
    return (exp(r*T/N)-d(T,v,N))/(u(T,v,N)-d(T,v,N))
def pd(T,r,v,N):
    return (1-pu(T,r,v,N))
def disc(T,r,N):
    return exp(-r*T/N)

def binomialOptionPricing(S,K,T,r,v,N, putCall):
    Steps = [0]*(N+1)
    C = [0]*(N+1)

    Steps[0]=S*(d(T,v,N))**N

    for j in range(1, N+1):
        Steps[j] = Steps[j-1]*(u(T,v,N)/d(T,v,N))
    
    for j in range(1, N+1):
        if putCall == 1: #Put
            C[j]=max(K-Steps[j],0)
        elif putCall == 2: #Call
            C[j]=max(Steps[j]-K,0)
    
    for i in range(N,0,-1):
        for j in range(0,i):
            C[j]=disc(T,r,N)*(pu(T,r,v,N)*C[j+1]+pd(T,r,v,N)*C[j])

    return C[0]