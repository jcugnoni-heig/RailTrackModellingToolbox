import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from scipy.signal import savgol_filter
from LibraryGUIPostPro.anx import *
import re


roughness=[]
Lyz=[]
Lyy=[]
Lzz=[]
Lzy=[]

############################

class Solid: # Defines a contact solid (Rail or Wheel)
    def __init__(self, Rw, Rwt,desciption):
        self.Rw = Rw 
        self.Rwt = Rwt
        self.info = desciption # indicates the solid type
        self.mobility=[[],[],[],[]] # initialise mobility
        self.freq=[]

    def SetMobility (self,orientation,angle,liste): # Implements mobility values

        '''
        Takes into account mobility for the wheel and acceleration for the rail.
        The acceleration data are integrated to obtain the mobility.
        The values are transformed into complex exponential form.

        '''

        Freq = []
        Magnitude = []
        phase = []
        Y=[] # Mobility

        
        for k in range(1,len(liste)): 
            Freq.append(float(liste[k][0]))
            Magnitude.append(float(liste[k][1]))
            phase.append(float(liste[k][2])+angle) 
            if(self.info =='roue'):
                Y.append(Magnitude[k-1]*cmath.exp(1j*phase[k-1]))
            if(self.info =='rail'):
                Y.append(Magnitude[k-1]*cmath.exp(1j*phase[k-1]/180*math.pi)*9.81/(2j*math.pi*Freq[k-1])) # The script takes the accelerancy values for the rail as input. It converts these values into mobility
                

        # Modifies the orientation and implements the values
        if(orientation == 'YY'):
            self.mobility[0] = Y
        if(orientation == 'YZ'):
            self.mobility[1] = Y
        if(orientation == 'ZZ'):
            self.mobility[2] = Y
        if(orientation == 'ZY'):
            self.mobility[3] = Y
        
        self.freq = Freq
    
    def Cut_Mobility(self,solid_obj):
        p1 = max(self.freq[0], solid_obj.freq[0])
        p2  = min(self.freq[-1], solid_obj.freq[-1])

        indice1 = [i for i, element in enumerate(self.freq) if p1 <= element <= p2]
        indice2 = [i for i, element in enumerate(solid_obj.freq) if p1 <= element <= p2]

        self.freq = self.freq[indice1[0]:indice1[-1]+1]
        solid_obj.freq = solid_obj.freq[indice2[0]:indice2[-1]+1]

        for k in range(4):
            self.mobility[k]=self.mobility[k][indice1[0]:indice1[-1]+1]
            solid_obj.mobility[k]=solid_obj.mobility[k][indice2[0]:indice2[-1]+1]

        return indice1[0],indice1[-1]+1,indice2[0],indice2[-1]+1
         
    def interpolation(self,freq): # interpolation of mobilities associated with solid on a new frequency band
        for p in range(4):
            A = list(np.interp(freq,self.freq,abs(np.array(self.mobility[p])))) # classic interpolation on amplitude parameters

            f_interp = PchipInterpolator(self.freq, np.angle(np.array(self.mobility[p]))) # use the PCHIP method to limit noise from over-oscillation effects.
            phi = list(savgol_filter(f_interp(freq), window_length=11, polyorder=2)) # smoothes the data using a Savitzky-Golay filter
            self.mobility[p]=[0]*len(freq)

            for t in range(len(self.mobility[p])):
                self.mobility[p][t]=A[t]*np.exp(1j*phi[t]) 
            
        self.freq = freq
    
    def setRail_mobility(self,FRFZ,FRFY,grpNodes): # Extracts lateral and vertical accelerancy from a .txt file and implements it in the script. They are expressed as g/N

        Lyy,Lyz,Lzy,Lzz = [],[],[],[]

        # Reads the .txt file from the harmonic simulation

        with open(FRFY) as f :
                    Extract_FRF = f.readlines()

        Tabl = Extract_FRF[0].split('	')

        for k in range(len(Tabl)):
            if(Tabl[k]==grpNodes +'_Y'+' [g/N]'):
                  indiceY=k
            if(Tabl[k]==grpNodes +'_Z'+' [g/N]'):
                  indiceZ=k

        for p in range(len(Extract_FRF)):
             temp = Extract_FRF[p].split('	')
             Lyy.append([temp[0],temp[indiceY],temp[indiceY+1]])
             Lyz.append([temp[0],temp[indiceZ],temp[indiceZ+1]])

        with open(FRFZ) as f :
                    Extract_FRF = f.readlines()

        Tabl = Extract_FRF[0].split(']	')

        for k in range(len(Tabl)):
            if(Tabl[k]==grpNodes+'_Y'+' [g/N]'):
                  indiceY=k
            if(Tabl[k]==grpNodes+'_Z'+' [g/N]'):
                  indiceZ=k

        for p in range(len(Extract_FRF)):
             temp = Extract_FRF[p].split('	')
             Lzy.append([temp[0],temp[indiceY],temp[indiceY+1]])
             Lzz.append([temp[0],temp[indiceZ],temp[indiceZ+1]])

             
        # Redirect the axes     
        self.SetMobility('ZZ',0,Lyy)
        self.SetMobility('YZ',0,Lzy)
        self.SetMobility('ZY',0,Lyz)
        self.SetMobility('YY',0,Lzz)

    
    def setWheel_mobility(self,w_path): # Extracts lateral and vertical mobility of the whell from a .csv file and implements it in the script. They are expressed as mm/sN

        # Reads the files containing the wheel data.
        Lxx,Lxz,Lzx,Lzz = [],[],[],[]
        Mx, Mz = [], []
       
        for k in range(len(w_path)):

            Mobiliy_mag = [[],[],[]]
            Mobiliy_phase = [[],[],[]]
            freq_wheel = []

            print('Reading the wheel files ' + str(k) + '/2')

            with open(w_path[k], "r", encoding="utf-8") as f:
                lines = f.readlines()

            freq = None
            node = None

            for i, line in enumerate(lines):
                # Frequency detection
                match_freq = re.search(r"FREQ:\s*([\d.E+-]+)", line)
                if match_freq:
                    freq = float(match_freq.group(1))
                    freq_wheel.append(freq)
                    continue

                # Detection of a node with DX, DY, DZ
                match_node = re.match(r"\s*N(\d+)\s+([\d.E+-]+)\s+([\d.E+-]+)\s+([\d.E+-]+)", line)
                if match_node and freq is not None:
                    node = "N" + match_node.group(1)
                    dx_real, dy_real, dz_real = map(float, match_node.groups()[1:])
                    continue

                # Take the imaginary part
                if node and re.match(r"\s+[\d.E+-]+\s+[\d.E+-]+\s+[\d.E+-]+", line):
                    dx_img, dy_img, dz_img = map(float, line.split())

                    # Add the magnetude
                    Mobiliy_mag[0].append(2*np.pi*freq*np.abs(dx_real+1j*dx_img))
                    Mobiliy_mag[1].append(2*np.pi*freq*np.abs(dy_real+1j*dy_img))
                    Mobiliy_mag[2].append(2*np.pi*freq*np.abs(dz_real+1j*dz_img))

                    # Add the phase
                    Mobiliy_phase[0].append(np.angle(1j*dx_real-dx_img))
                    Mobiliy_phase[1].append(np.angle(1j*dy_real-dy_img))
                    Mobiliy_phase[2].append(np.angle(1j*dz_real-dz_img))
                    node = None  

                    if(k==0):
                         Lxx = [[freq_wheel[p], Mobiliy_mag[0][p], Mobiliy_phase[0][p]] for p in range(len(freq_wheel))]
                         Lxz = [[freq_wheel[p], Mobiliy_mag[2][p], Mobiliy_phase[2][p]] for p in range(len(freq_wheel))]
                         Mx = [Mobiliy_mag[0][1:].copy(),Mobiliy_phase[0][1:].copy(),Mobiliy_mag[2][1:].copy(),Mobiliy_phase[2][1:].copy()] # Mxx, Mxz
                    else:
                         Lzx = [[freq_wheel[p], Mobiliy_mag[0][p], Mobiliy_phase[0][p]] for p in range(len(freq_wheel))]
                         Lzz = [[freq_wheel[p], Mobiliy_mag[2][p], Mobiliy_phase[2][p]] for p in range(len(freq_wheel))]
                         Mz = [Mobiliy_mag[0][1:].copy(),Mobiliy_phase[0][1:].copy(),Mobiliy_mag[2][1:].copy(),Mobiliy_phase[2][1:].copy()] # Mzx, Mzz


        # Redirect the axes if neccesary  
        self.SetMobility('YY',0,Lxx)
        self.SetMobility('YZ',0,Lxz)
        self.SetMobility('ZY',0,Lzx)
        self.SetMobility('ZZ',0,Lzz)

        return Mx, Mz

        #Lxx,Lxz,Lzx,Lzz = [],[],[],[]

def Mobility_Matrix(Contact,iteration):
    return np.array([[Contact.mobility[0][iteration],Contact.mobility[1][iteration]],[Contact.mobility[3][iteration],Contact.mobility[2][iteration]]])

def Contact_Load(Solid_Rail,Solid_Wheel,path_roughness,para,vtrain,Rw,Rwt,Rrt,F0):

    '''
    Compute Contact Forces according to the Thomson's equations

    '''
    
    E = para["ERail"]
    E=E*1e6
    nu = para["nuRail"]

    vtrain=vtrain/3.6 # mm/s

    Ep = E/(1-nu**2)
    G=E/2*(1+nu)

    a, b , g, c, C22 ,Kh, Kl  = getParameters(Rw,Rrt,nu,E,F0)

    Solid_Rail.Cut_Mobility(Solid_Wheel)

    # retrieves roughness data if implemented, otherwise expresses values per unit of meter
    try:
        temp_R =[[],[]]
        with open(path_roughness) as f :
            ligne_R = f.readlines()

        for k in range(1,len(ligne_R)):
            temp=ligne_R[k].split(';')
            temp_R[0].append(float(temp[0]))
            temp_R[1].append(float(temp[1]))

        roughness=np.interp(Solid_Wheel.freq,temp_R[0],temp_R[1])
        echec=False
    except:
        echec=True
        roughness=[1]*len(Solid_Wheel.freq)
    
    
    Solid_Rail.interpolation(Solid_Wheel.freq)
    #Solid_Wheel.interpolation(Solid_Rail.freq)
    freq=np.array(Solid_Rail.freq)
    WaveNumber=2*math.pi*freq/vtrain

    Mobilite_ContactZ = 2j*math.pi*freq/Kh
    Mobilite_ContactY = vtrain/(G*c**2*C22) + 2j*math.pi*freq/Kl

    #In principle, a contact filter is required to calculate the contact forces. 
    #For the moment, the H filter is commented on, but it will soon be possible to integrate it into the equations.
    
    # H = 1/(1+(math.pi/4)*(WaveNumber*a)**3) # Filter
    # H = np.exp(H*np.log(10)/20)

    H = np.ones(freq.shape)
    
    Yr = np.array(Solid_Rail.mobility)
    print(Yr.shape)
    Yw = np.array(Solid_Wheel.mobility)
    print(Yw.shape)


    L1=np.array([[1]*len(Solid_Wheel.freq),[0]*len(Solid_Wheel.freq),[0]*len(Solid_Wheel.freq),[0]*len(Solid_Wheel.freq)])
    L2=np.array([[0]*len(Solid_Wheel.freq),[0]*len(Solid_Wheel.freq),[1]*len(Solid_Wheel.freq),[0]*len(Solid_Wheel.freq)])
    Yc = Mobilite_ContactY*L1 + Mobilite_ContactZ*L2

    Y = Yr + Yw + Yc
    
    Fy = -2j*np.pi*freq*Y[1,:]/(Y[2,:]*Y[0,:]-Y[3,:]*Y[1,:])*H 
    Fz = 2j*np.pi*freq*Y[0,:]/(Y[2,:]*Y[0,:]-Y[3,:]*Y[1,:])*H

    Fy_phase=np.zeros(len(Solid_Wheel.freq))
    Fz_phase=np.zeros(len(Solid_Wheel.freq))
    Fy_amp=np.zeros(len(Solid_Wheel.freq))
    Fz_amp=np.zeros(len(Solid_Wheel.freq))

    for n in range(len(Solid_Wheel.freq)):
        Fy_phase[n] = cmath.phase(Fy[n])
        Fz_phase[n] = cmath.phase(Fz[n])
        Fy_amp[n] = abs(Fy[n])*roughness[n]
        Fz_amp[n] = abs(Fz[n])*roughness[n]   
    
    return Fy_amp,Fy_phase,Fz_amp,Fz_phase,H,WaveNumber,echec