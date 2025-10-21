from scipy.special import ellipk, ellipe
from scipy.optimize import fsolve
from scipy.interpolate import griddata
import math
import csv
import numpy as np
import os

#####################
#This appendix defines a series of functions useful for demining contact parameters.
#####################

def equation(g2, costheta): # non-linear equation to solve
    e = 1 - 1 / g2
    E = ellipe(e) # the complete elliptic integral of the second kind
    K = ellipk(e) # the complete elliptic integral of the first kind
    num = (g2 + 1) * E - 2 * K
    den = (g2 - 1) * E
    return num / den - costheta

def Cp(csv_file,g_query, nu_query):  # creepage coefficient (To Change)

    '''
    This function is used to perform interpolations on the data obtained from Kalker's work.
    The aim is to approximate the values of C22, C33 and C21 (the creepage coefficients). 
    The function takes as parameters a table of values in .csv format and interpolates these data to obtain the value of the desired creepage coefficient.

    '''
    nu_liste=[]
    nu, g, C = [], [], []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)  # Skip header if present
        ligne = next(reader)
        nu_liste = [float(ligne[p]) for p in range(1,len(ligne))] # save nu 
        print(nu_liste)
        
        for row in reader:
            for k in range(len(nu_liste)):
                g.append(float(row[0]))
                nu.append(nu_liste[k])
                C.append(float(row[k+1]))

    nu = np.array(nu)
    g = np.array(g)
    C = np.array(C)

    # Create a grid for interpolation
    gi = np.linspace(np.min(g), np.max(g), 100)
    nui = np.linspace(np.min(nu), np.max(nu), 100)
    GI, NUI = np.meshgrid(gi, nui)

    # Interpolate
    C_query = griddata(points=(g, nu), values=C, xi=(g_query, nu_query), method='linear')
    print(f"Interpolated value at ({g_query}, {nu_query}) = {C_query}")
    return C_query

def getParameters(Rw,Rrt,nu,E,F0): # Numerical resolution of the non-linear equation associated with the wheel-rail contact to determine the contact parameters
    Ep = E/(1-nu**2)
    G=E/2*(1+nu)
    R0 = 1/((1/2)*(1/Rw + 1/Rrt))

    #Target value for cos(theta)
    cos_t = -(R0/2)*(1/Rw - 1/Rrt)

    # Choice of an initial estimate for g^2
    g2_initial_guess = 2.0

    # Résolution numérique
    g2 = fsolve(equation, g2_initial_guess, args=(cos_t,))

    # Contact parameters
    g = np.sqrt(g2[0])
    e=1-1/(g**2)
    epsi = 4*ellipk(e)*((np.pi/(2*g**2*ellipe(e)))**(1/3))/np.pi
    chi = 1 + (nu/(1-nu))*(1/4 + (1/math.pi)*math.atan(g))**(1/3)
    sigma2 = ((2*ellipe(e))/(np.pi*g))**(1/3)
    sigma1 = sigma2*g
    Kh = 1/((epsi/2)*(2/(3*(Ep**2)*F0*R0))**(1/3))
    Kl = Kh/chi
    a_f = sigma1*((3*F0*R0/(2*Ep))**(1/3))
    b_f = a_f/g
    c= np.sqrt(a_f*b_f)
    C22 = Cp(os.path.join(os.path.dirname(__file__),'c22.csv'),g,nu)

    print('--- Resultats ---')
    print('F0 [N]: ', F0)
    print('Rw [m]: ', Rw)
    print('g [/]: ', g)
    print('cos_t [/]: ', cos_t)
    print('epsi/2 [/]: ', epsi/2)
    print('kh [N/m]: ', Kh)
    print('kl [N/m]: ', Kl)
    print('C22 [/]: ', C22)
    # print('Rwt : ', R_f)
    print('a [m]: ', a_f)
    print('b [m]: ', b_f)

    return g, a_f, b_f, c, C22, Kh, Kl


def interpolate_values(target,path_data):
    """
    Interpolates the values in columns 1, 3 and 4 according to the 2ᵉ column.
    """

    with open(path_data) as f :
        Extract_data = f.readlines()

    data=[[],[],[],[]]

    for p in range (1,len(Extract_data)):
        temp = Extract_data[p].split(',')
        for t in range (4):
            data[t].append(float(temp[t]))
    # Column extraction
    col1 = np.array(data[0])  # 1st column
    col2 = np.array(data[1])  # 2snd column (values to search)
    col3 = np.array(data[2])  # 3rd column
    col4 = np.array(data[3])  # 4th column
    
    # Check if the value is outside the limits and return the extreme values
    if target <= col2[0]:
        return col1[0], col3[0], col4[0]
    if target >= col2[-1]:
        return col1[-1], col3[-1], col4[-1]

    # Linear interpolation
    g = np.interp(target, col2, col1)
    sigma_1 = np.interp(target, col2, col3)
    sigma_2 = np.interp(target, col2, col4)

    return g, sigma_1, sigma_2