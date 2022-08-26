# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 14:56:18 2021

@author: mob
"""


import scipy as sp
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.io

font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)


def runSimu(Name, Freq, RailPadStiffness, SleeperTF):
    
    # Check for constant or frequency dependent rail pad stiffness 
    
    if isinstance(RailPadStiffness, complex): 
        Kp = np.ones(len(Freq))*RailPadStiffness
    else:
        Kp = RailPadStiffness
    
    # Angular frequencies and square values

    allw = Freq*2*sp.pi
    allw2 = allw**2
    
    # Rail Parameters

    EI = 6.42e6
    GA = 6.17e8
    kappa = 0.4
    GAK = GA*kappa
    rI = 0.240
    mr = 60
    
    nr = 0.02 # add constant damping
    EI = EI*(1+1j*nr)
    GAK = GAK*(1+1j*nr)
    
    # Compute wavenumbers of the free rail
    
    alla = -rI*allw2/EI/(1+1j*nr) - mr*allw2/GAK/(1+1j*nr)
    allb = mr*allw2*(rI*allw2/GAK/(1+1j*nr) - 1)/EI/(1+1j*nr)
    
    dis = alla**2 - 4*allb
    sqd = np.sqrt(dis)
    l1 = (-alla-sqd)/2
    l2 = (-alla+sqd)/2
    
    k1 = -np.sqrt(l1)
    k2 = +np.sqrt(l1)
    k3 = -np.sqrt(l2)
    k4 = +np.sqrt(l2)
    
    kn1 = []
    kn2 = []
    
    for i, f in enumerate(Freq):
            
        kn = []
        for k in [k1[i], k2[i], k3[i], k4[i]]:
            if np.imag(k) < 0:
                kn.append(k)
        kn1.append(kn[0])
        kn2.append(kn[1])
        
    kn1 = np.array(kn1)
    kn2 = np.array(kn2)
    
    # Sleepers and Excitation postition
        
    nsleep = 200
    spacing = 0.6
    SleepPos = np.linspace(0, nsleep*spacing, nsleep+1)
    xF0 = 60.3 # Excitation at half span between sleepers, in the middle of the track
    
    dx0 = abs(SleepPos-np.repeat(xF0, len(SleepPos))) # postion difference between sleepers and excitation point
    dsleep = abs(np.repeat(SleepPos, len(SleepPos))-np.tile(SleepPos, len(SleepPos))) # postion difference between all sleepers 


    print("wavenumbers done")
    
    
    # Receptance Matrix and Force Vector at each frequency
    
    def areceptance(dx, kn1, kn2, omega, EI, GAK, rI, mr):
        
        C1 = (GAK - rI*omega**2)/EI
        C2 = -rI*omega**2/EI - mr*omega**2/GAK
        
        e1 = (kn1**2 + C1)/(4*kn1**3 + 2*C2*kn1)
        e2 = (kn2**2 + C1)/(4*kn2**3 + 2*C2*kn2)
        
        alpha = -1j*(e1*sp.exp(-1j*kn1*dx) + e2*sp.exp(-1j*kn2*dx))/GAK
    
        return alpha
        
    vareceptance = sp.vectorize(areceptance, excluded=['kn1', 'kn2', 'omega', 'EI', 'GAK', 'rI', 'mr'])
    
    
    dsleep = np.array(np.hsplit(dsleep, len(SleepPos)))
    
    C1 = (GAK - rI*allw2)/EI
    C2 = -rI*allw2/EI - mr*allw2/GAK
    
    e1 = (kn1**2 + C1)/(4*kn1**3 + 2*C2*kn1)
    e2 = (kn2**2 + C1)/(4*kn2**3 + 2*C2*kn2)
    
    """
    E1 = np.repeat(e1[:,np.newaxis], len(SleepPos), axis=1)
    E2 = np.repeat(e2[:,np.newaxis], len(SleepPos), axis=1)
    Kn1 = np.repeat(kn1[:,np.newaxis], len(SleepPos), axis=1)
    Kn2 = np.repeat(kn2[:,np.newaxis], len(SleepPos), axis=1)
    
    dx0 = np.repeat(dx0[np.newaxis,:], len(Freq), axis=0)
    aF0 = -1j*(E1*np.exp(-1j*Kn1*dx0) + E2*np.exp(-1j*Kn2*dx0))/GAK
    
    E1 = np.repeat(E1[:,:,np.newaxis], len(SleepPos), axis=2)
    E2 = np.repeat(E2[:,:,np.newaxis], len(SleepPos), axis=2)
    KN1 = np.repeat(Kn1[:,:,np.newaxis], len(SleepPos), axis=2)
    KN2 = np.repeat(Kn2[:,:,np.newaxis], len(SleepPos), axis=2)
    
    dsleep = np.repeat(dsleep[np.newaxis,:,:], len(Freq), axis=0)
    aVec = -1j*(E1*np.exp(-1j*KN1*dsleep) + E2*np.exp(-1j*KN2*dsleep))/GAK
    
    tmp = 1/Kp + SleeperTF
    Tmp = np.repeat(tmp[:,np.newaxis], len(SleepPos), axis=1)
    TMP = np.repeat(Tmp[:,:,np.newaxis], len(SleepPos), axis=2)
    EYE = np.repeat(sp.eye(len(SleepPos))[np.newaxis,:,:], len(Freq), axis=0)
    aMat = EYE + aVec/TMP

        
    print("TF Matrix and Forces done")
    
            
    # Receptance computation at sleeper positions
        
    R = np.linalg.solve(aMat, aF0)
    Fj = R/Tmp
    Fj = np.swapaxes(Fj,0,1)
    """
    
    
    """ new for frequency dependent rail pads"""
    allf = Freq
    
    aF0 = sp.zeros((len(SleepPos), len(allf)), dtype=complex) # alphas for force on sleeper
    dx0 = abs(SleepPos-sp.repeat(xF0, len(SleepPos))) # postion difference between sleepers and excitation point
    
    aMat = sp.zeros((len(SleepPos), len(SleepPos), len(allf)), dtype=complex) # alphas for all sleepers
    dsleep = abs(sp.repeat(SleepPos, len(SleepPos))-sp.tile(SleepPos, len(SleepPos))) # postion difference between all sleepers 
    
    for i, f in enumerate(allf):
        
        w = 2*sp.pi*f
        
        Sp = Kp[i]
        
        aF0[:, i] = vareceptance(dx0[:], kn1[i], kn2[i], w, EI, GAK, rI, mr)
        
        aVec = vareceptance(dsleep[:], kn1[i], kn2[i], w, EI, GAK, rI, mr)
        aVec *= 1/(1/Sp + SleeperTF[i])
        
        aMat[:, :, i] = sp.eye(len(SleepPos)) + sp.hsplit(aVec, len(SleepPos)) 
    
    
    
        
    print('Matrix and Force Vectors computation is over')
    print(' ')
    
            
    # Receptance computation at sleeper positions
    
    R = sp.zeros((len(SleepPos), len(allf)), dtype=complex)
    Fj = sp.zeros((len(SleepPos), len(allf)), dtype=complex)
    
    for i, f in enumerate(allf):
        
        Sp = Kp[i]
        
        R[:, i] = sp.linalg.solve(aMat[:, :, i], aF0[:, i])
        Fj[:,i] = R[:, i]/(1/Sp + SleeperTF[i])  
        
        


    """ added section finished """
    
    
    
    
        
    print("TF at Sleepers done")
    
    # Mobility computation
    
    # virtual sensor locations for TDR calculations according to ISO standard
    # around 40m span starting in the middle of the track, in between sleepers
    positionTDR = sp.array([0,0.15,0.30,0.45,0.6,0.75,0.9,1.05,1.2,1.35,1.5,1.8,2.1,2.4,3,3.6,\
                            4.2,4.8,6,7.2,9.6,12,14.4,18,21.6,25.2,28.8,32.4,39.6])+60.3
        
    
    dx = []
    for i, x in enumerate(positionTDR):
        if i == 0:
            dx.append((positionTDR[1]-x)/2)
        if i > 0 and i < len(positionTDR)-1:
            dx.append((x-positionTDR[i-1])/2 + (positionTDR[i+1]-x)/2)
        if i == len(positionTDR)-1:
            dx.append(x-positionTDR[i-1])
    
    dp0 = abs(positionTDR-sp.repeat(xF0, len(positionTDR)))
    dps0 = abs(sp.tile(sp.array([positionTDR]).transpose(), (1, len(SleepPos)))-\
               sp.tile(SleepPos, (len(positionTDR), 1)))
    
    mob = sp.zeros((len(Freq), len(positionTDR)), dtype=complex) # mobility (speed TF)
    acc = sp.zeros((len(Freq), len(positionTDR)), dtype=complex) # accelerance (acceleration TF)
    
    for i, f in enumerate(Freq):         
        alphas = -1j*(e1[i]*sp.exp(-1j*kn1[i]*dps0[:]) + e2[i]*sp.exp(-1j*kn2[i]*dps0[:]))/GAK
        mob[i, :] = 1j*allw[i]*(vareceptance(dp0[:], kn1[i], kn2[i], allw[i], EI, GAK, rI, mr) - sp.dot(alphas, Fj[:, i]))
        acc[i, :] = 1j*allw[i]*mob[i, :]
        
    print("Mobility done")
    
    
    # TDR calculation
    
    TDR = []
    
    for i, f in enumerate(Freq):
        
        mobSum = 0.0
        
        for j, x in enumerate(dx):
            mobSum += (abs(mob[i, j])**2/abs(mob[i,0])**2)*x
        TDR.append(10*sp.log10(sp.exp(1))/mobSum)
        
    print("TDR done")
    
    
    # Rail Direct Acoustic Radiation
    
    rho0 = 1.2
    yRail = positionTDR
    rwidth = 0.072
    d = 7.5 + rwidth/2
    
    rstep = []
    for q, p in enumerate(positionTDR):
        if q == 0:
            rstep.append(positionTDR[q+1]-p) # extended area at left end
        elif q == len(positionTDR)-1:
            rstep.append(p-positionTDR[q-1]) # extended area at right end
        else:
            rstep.append((p-positionTDR[q-1])/2 + (positionTDR[q+1]-p)/2)
        
    dS = rwidth*sp.array(rstep)
    
    pRail = sp.zeros((len(positionTDR), len(Freq)), dtype=complex)
    k0 = allw/343
                    
    for q, x in enumerate(yRail):
            
        rRail = sp.sqrt(d**2+x**2)
        pRail[q, :] = 1j*Freq*rho0*dS[q]*sp.exp(-1j*k0*rRail)*mob[:,q]/rRail
            
    pTotal = pRail[0] + 2*sp.sum(pRail[1:], axis=0) # behind + in front of excitation
    pdB = 20*np.log10(abs(pTotal)/20e-6)
    
    
    # Plot results and save figures
    
    fig = plt.figure(1, figsize=(16,9))
    ax = plt.subplot(111)
    ax.grid('on', which='both', ls='--')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Rail Accelerance [m/s^2/N]')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(Freq, abs(acc[:,0]), color='b')
    fig.savefig(Name+"_TF.png")
    
    
    fig = plt.figure(2, figsize=(16,9))
    ax = plt.subplot(111)
    ax.grid('on', which='both', ls='--')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('TDR [dB/m]')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(Freq, TDR, color='b')
    fig.savefig(Name+"_TDR.png")
    
    fig = plt.figure(3, figsize=(16,9))
    ax = plt.subplot(111)
    ax.grid('on', which='both', ls='--')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Sound Pressure TF [Pa/N]')
    ax.set_xscale('log')
    ax.set_yscale('linear')
    ax.plot(Freq, abs(pdB), color='b')
    fig.savefig(Name+"_TF_Sound_Pressure_@7m.png")
    
    # Save results in text file
    
    file = open(Name+"_Results.txt", 'w')
    file.write("Frequencies [Hz]    Rail Acc TF [m/s^2/N]    TDR [dB/m]    Sound Presure [Pa]\n")
    for i, f in enumerate(Freq):
        file.write("{}    {}    {}    {}\n".format(f, acc[i,0], TDR[i], pTotal[i]))
    file.close()
    
    
    
    
    
    
    
    
    
