

import scipy as sp
import scipy.linalg as alg


# Sleeper Parameters

# From Joel and Maurice FE model
E = 46.3e9 # Young's modulus
v = 0.20 # Poisson's ration
G = E/2/(1+v) # Shear modulus
kappa = 10*(1+v)/(12+11*v) # Shear coefficient; rectangular section: k=10*(1+v)/(12+11*v); circular section: k=6*(1+v)/(7+6*v)
n = 0.002 # Loss factor (0.016)
rho = 2435.6 # Density

L = 2.6 # Sleeper length
mass = 286 # Sleeper mass
A = mass/L/rho
m = mass/L # mass per unit length = section mass

a = 15e-2
b = 18e-2 # trapezoid cross section dimensions at sleeper center
h = 17e-2
Ic = h*(16*h**2*a*b+4*h**2*b**2+4*h**2*a**2+3*a**4+6*a**2*b**2+6*a**3*b+6*a*b**3+3*b**4)/(144*(a+b))

a = 27e-2
b = 30e-2 # trapezoid cross section dimensions at sleeper ends
h = 21e-2 
Ie = h*(16*h**2*a*b+4*h**2*b**2+4*h**2*a**2+3*a**4+6*a**2*b**2+6*a**3*b+6*a*b**3+3*b**4)/(144*(a+b))

I = (Ie+Ic)/2 # Average second moment of area
I = sp.sqrt(Ie*Ic) # Geometrical average second moment of area
I = Ic

EI = E*I*(1+1j*n)
GAK = G*A*kappa*(1+1j*n)
rI = rho*I


# Load parameter

yF = 2.075   # Excitation position along sleeper
F = 1


def GenerateTF(allf, BallastStiffness):
    
    if isinstance(BallastStiffness, complex): 
        S = sp.ones(len(allf))*BallastStiffness
    else:
        S = BallastStiffness
        
    allw = 2*sp.pi*allf
    allw2 = allw**2
    
    alls = sp.zeros(len(allf), dtype=complex)
    alla = sp.zeros(len(allf), dtype=complex)
    allb = sp.zeros(len(allf), dtype=complex)
    
    for i, f in enumerate(allf):
        
        I = Ic*(max(allf)-f)/max(allf) + (Ie+Ic)/2*f/max(allf) # Change cross section depedning on frequency to counteract inertia at sleeper ends
        EI = E*I*(1+1j*n)
        GAK = G*A*kappa*(1+1j*n)
        rI = rho*I
    
        alls[i] = S[i] - m*allw2[i]
        alla[i] = alls[i]/GAK - rI*allw2[i]/EI
        allb[i] = alls[i]/EI*(1 - rI*allw2[i]/GAK)
    
    
    dis = alla**2 - 4*allb
    sqd = sp.sqrt(dis)
    l1 = (-alla-sqd)/2
    l2 = (-alla+sqd)/2
    
    k1 = -sp.sqrt(l1)
    k2 = +sp.sqrt(l1)
    k3 = -sp.sqrt(l2)
    k4 = +sp.sqrt(l2)
    
    kn1 = []
    kn2 = []
    
    for i, f in enumerate(allf):
            
        kn = []
        for k in [k1[i], k2[i], k3[i], k4[i]]:
            if sp.imag(k) < 0:
                kn.append(k)
        kn1.append(kn[0])
        kn2.append(kn[1])
        
    kn1 = sp.array(kn1)
    kn2 = sp.array(kn2)
    
    phi1 = 1j*kn1*GAK/(rI*allw2 - GAK - EI*kn1**2)
    phi2 = 1j*kn2*GAK/(rI*allw2 - GAK - EI*kn2**2)
        
    
    # Forced response
    
    Kmphi1 = 1j*kn1-phi1
    Kmphi2 = 1j*kn2-phi2
    
    expm1yF = sp.exp(-1j*kn1*yF)
    expm2yF = sp.exp(-1j*kn2*yF)
    
    expp1yF = sp.exp(1j*kn1*yF)
    expp2yF = sp.exp(1j*kn2*yF)
    
    expm1Ly = sp.exp(-1j*kn1*(L-yF))
    expm2Ly = sp.exp(-1j*kn2*(L-yF))
    
    expp1Ly = sp.exp(1j*kn1*(L-yF))
    expp2Ly = sp.exp(1j*kn2*(L-yF))
    
    phiK1 = 1j*phi1*kn1
    phiK2 = 1j*phi2*kn2
    
    TF = sp.zeros(len(allf), dtype=complex)
    
    for i, f in enumerate(allf):
    
        M = sp.zeros((8,8), dtype=complex)
        
        M[0,0] = Kmphi1[i]*expm1yF[i]    #
        M[0,1] = Kmphi2[i]*expm2yF[i]    # Shear force = 0 at y = -yF
        M[0,2] = -Kmphi1[i]*expp1yF[i]   #
        M[0,3] = -Kmphi2[i]*expp2yF[i]   #
        
        M[1,0] = phiK1[i]*expm1yF[i]   #
        M[1,1] = phiK2[i]*expm2yF[i]   # Bending moment = 0 at y = -yF
        M[1,2] = phiK1[i]*expp1yF[i]   #
        M[1,3] = phiK2[i]*expp2yF[i]   #
        
        M[2,:] = [1, 1, 1, 1, -1, -1, -1, -1]  # Continuity of displacement at y = 0
        
        M[3,0] = phi1[i]    # 
        M[3,1] = phi2[i]    #
        M[3,2] = -phi1[i]   #
        M[3,3] = -phi2[i]   # Continuity of rotation at y = 0
        M[3,4] = -phi1[i]   #
        M[3,5] = -phi2[i]   #
        M[3,6] = phi1[i]    #
        M[3,7] = phi2[i]    #
        
        M[4,0] = phiK1[i]    #
        M[4,1] = phiK2[i]    #
        M[4,2] = phiK1[i]    #
        M[4,3] = phiK2[i]    # Continuity of bending moment at y = 0
        M[4,4] = -phiK1[i]   #
        M[4,5] = -phiK2[i]   #
        M[4,6] = -phiK1[i]   #
        M[4,7] = -phiK2[i]   #
        
        M[5,0] = 1j*kn1[i]          #
        M[5,1] = 1j*kn2[i]          #
        M[5,2] = -1j*kn1[i]         #
        M[5,3] = -1j*kn2[i]         # Equilibrium of forces at y = 0 
        M[5,4] = -1j*kn1[i]         # Corrected to calculate receptance to force caused by rail deflection
        M[5,5] = -1j*kn2[i]         #
        M[5,6] = 1j*kn1[i]          #
        M[5,7] = 1j*kn2[i]          #
        
        M[6,4] = Kmphi1[i]*expp1Ly[i]    #
        M[6,5] = Kmphi2[i]*expp2Ly[i]    # Shear force = 0 at y = L-yF
        M[6,6] = -Kmphi1[i]*expm1Ly[i]   #
        M[6,7] = -Kmphi2[i]*expm2Ly[i]   #
        
        M[7,4] = phiK1[i]*expp1Ly[i]   #
        M[7,5] = phiK2[i]*expp2Ly[i]   # Bending moment = 0 at y = L-yF
        M[7,6] = phiK1[i]*expm1Ly[i]  #
        M[7,7] = phiK2[i]*expm2Ly[i]  #
        
        Fv = [0, 0, 0, 0, 0, F/GAK, 0, 0]  # F = 1N in force equilibrium equation
        
        [A1, A2, A3, A4, A5, A6, A7, A8] = alg.solve(M, Fv)
        TF[i] = A1 + A2 + A3 + A4  
    
    return TF


    