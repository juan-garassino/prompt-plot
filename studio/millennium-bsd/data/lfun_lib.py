import numpy as np, math
CURVES={'11a1':([0,-1,1,-10,-20],11),'37a1':([0,0,1,-1,0],37),'389a1':([0,1,1,-2,0],389),'5077a1':([0,0,1,-7,6],5077)}
def primes(n):
    s=np.ones(n+1,bool); s[:2]=False
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
def count(ai,p):
    a1,a2,a3,a4,a6=ai
    if p==2:
        n=1
        for X in range(2):
            for Y in range(2):
                if (Y*Y+a1*X*Y+a3*Y-(X**3+a2*X*X+a4*X+a6))%2==0: n+=1
        return n
    x=np.arange(p,dtype=np.int64)
    b2=a1*a1+4*a2; b4=2*a4+a1*a3; b6=a3*a3+4*a6
    rhs=((4*x%p)*x%p*x%p + b2*x%p*x%p + 2*b4*x + b6)%p
    sq=np.zeros(p,np.int64); sq[(x*x)%p]=1
    cnt=np.where(rhs==0,1,np.where(sq[rhs]==1,2,0))
    return int(cnt.sum())+1
def ap_dict(ai,M):
    return {int(p):int(p)+1-count(ai,int(p)) for p in primes(M)}
def an_list(ai,N,M,ap=None):
    if ap is None: ap=ap_dict(ai,M)
    spf=np.zeros(M+1,np.int64)
    for p in sorted(ap):
        sl=spf[p::p]; sl[sl==0]=p
    a=[0]*(M+1); a[1]=1
    for n in range(2,M+1):
        p=int(spf[n]); m=n; k=0
        while m%p==0: m//=p; k+=1
        if N%p==0: apk=ap[p]**k
        else:
            A0,A1=1,ap[p]
            for j in range(2,k+1): A0,A1=A1,ap[p]*A1-p*A0
            apk=A1 if k>=1 else 1
        a[n]=apk*a[m]
    return a,ap
_u=np.linspace(0,12,6001); _h=_u[1]-_u[0]
_w=np.ones_like(_u); _w[1:-1:2]=4; _w[2:-1:2]=2; _w*=_h/3
def upper_gamma(av,x):
    x=np.asarray(x,float); out=np.empty_like(x)
    for i in range(0,len(x),500):
        X=x[i:i+500,None]
        ln=av*np.log(X)+av*_u[None,:]-X*np.exp(_u[None,:])
        out[i:i+500]=(np.exp(np.maximum(ln,-745))*_w[None,:]).sum(1)
    return out
class Lfun:
    def __init__(s,name,M=None):
        ai,N=CURVES[name]; s.N=N; s.ai=ai
        if M is None: M=int(70*math.sqrt(N)/(2*math.pi))+5
        s.a,s.ap=an_list(ai,N,M)
        n=np.arange(1,M+1); s.n=n; s.A=np.array(s.a[1:],float)
        s.x=2*np.pi*n/math.sqrt(N); s.c=math.sqrt(N)/(2*math.pi)
    def Lam(s,t,eps):
        t1=(s.c**t)*(s.n**-t)*upper_gamma(t,s.x)
        t2=(s.c**(2-t))*(s.n**(t-2.0))*upper_gamma(2-t,s.x)
        return float((s.A*(t1+eps*t2)).sum())
    def L(s,t,eps):
        return s.Lam(t,eps)*(2*math.pi)**t*s.N**(-t/2)/math.gamma(t)
