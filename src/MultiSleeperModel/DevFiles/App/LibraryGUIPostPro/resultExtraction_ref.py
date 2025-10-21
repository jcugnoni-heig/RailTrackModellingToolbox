import os
import json
import numpy as np
import re
from decimal import Decimal # used in an 'exec' command, thus not considered used by the editor
import matplotlib.pyplot as plt
from matplotlib import ticker
from math import log10

class SimulationResults:
    def __init__(self, p_folder):
        self.folder = p_folder
        self.name = os.path.basename(self.folder)

        paramFile = os.path.join(self.folder, 'parameters.json')
        if os.path.exists(paramFile) == False:
            print('File parameters.json not found for ' + self.name + '.')
            self.parameters = None
            self.paramFile = None
        else:
            with open(paramFile, 'r') as f:
                txt = f.read()
            f.close()
            self.parameters = json.loads(txt)
            self.paramFile = paramFile

        acousticFile = os.path.join(self.folder, 'Outputs', 'acousticResults.txt')
        if os.path.exists(acousticFile) == False:
            print('File acousicResults.txt not found for ' + self.name + '.')
            self.acousticFile = None
        else:
            self.acousticFile = acousticFile

        accelFile = os.path.join(self.folder, 'Outputs', 'FRF.txt')
        if os.path.exists(accelFile) == False:
            print('File FRF.txt not found for ' + self.name + '.')
            self.accelFile = None
        else:
            self.accelFile = accelFile

        self.AI = {}
        self.VI = {}

        # Reference acoustic pressure (20 µPa)
        self.p_ref = 20e-6

        self.GetAccelFRFs()
        self.GetAcousticFRFs()
        self.ComputeIndicators()

    def GetAccelFRFs(self):
        if self.accelFile is None:
            self.frequency = None
            self.FRF_railClose = None
            self.FRF_railFar = None
            self.FRF_sleeper1 = None
            return

        with open(self.accelFile, 'r') as f:
            lines = f.readlines()
        f.close()

        nSlp = self.parameters['nSlp']
        self.enough_sleeper = True
        if nSlp < 100:
            print('Warning: The number of sleepers to compute the acoustic indicators must be 100 at least.')
            self.enough_sleeper = False

        headers = lines[0].split('\t')
        slpForce = self.parameters['slpForce']
        pat_railClose_Y = 'E' + str(slpForce) + "_nRai[1-4]_Y "
        pat_railFar_Y = 'E' + str(slpForce+20) + "_nRai[1-4]_Y "
        pat_sleeper = 'E' + str(slpForce) + "_nSlp_Y "

        indices_railCloseY = []
        indices_railFarY = []
        indices_sleeper = []

        for i, header in enumerate(headers):
            x1 = re.search(pat_railClose_Y, header)
            x2 = re.search(pat_railFar_Y, header)
            x3 = re.search(pat_sleeper, header)
            if x1:
                indices_railCloseY.append(i)
            if x2:
                indices_railFarY.append(i)
            if x3:
                indices_sleeper.append(i)
        
        frequency = []
        FRF_railClose = []
        FRF_railFar = []
        FRF_sleeper1 = []

        for line in lines[1:]:
            arr = line.split('\t')
            try:
                frequency.append(float(arr[0]))
            except:
                print('Problem reading ' + self.accelFile + '.')
                return
            
            temp = 0
            for index in indices_railCloseY:
                # example : ((E201_nRai1_Y [g/N])^2 + (E201_nRai1_Z [g/N])^2)^0.5
                temp += (float(arr[index])**2 + float(arr[index+2])**2)**(1/2.0)# index+2 because one value over two is the phase 
            FRF_railClose.append(temp/len(indices_railCloseY))

            temp = 0
            for index in indices_railFarY:
                temp += (float(arr[index])**2 + float(arr[index+2])**2)**(1/2.0)# index+2 because one value over two is the phase
            FRF_railFar.append(temp/len(indices_railFarY))

            temp = 0
            for index in indices_sleeper:
                temp += abs(float(arr[index]))
            FRF_sleeper1.append(temp/len(indices_sleeper))

        self.frequency = np.array(frequency)
        self.FRF_railClose = np.array(FRF_railClose)
        self.FRF_railFar = np.array(FRF_railFar)
        self.FRF_sleeper1 = np.array(FRF_sleeper1)

        [self.FRF_railClose_3rdOct, self.freq_3rdOct] = Utils.ThirdOctaveBand(self.frequency, self.FRF_railClose)
        [self.FRF_railFar_3rdOct, temp] = Utils.ThirdOctaveBand(self.frequency, self.FRF_railFar)
        [self.FRF_sleeper1_3rdOct, temp] = Utils.ThirdOctaveBand(self.frequency, self.FRF_sleeper1)

    def GetAcousticFRFs(self):
        if self.acousticFile is None:
            self.FRF_pressTot1 = None
            self.FRF_pressRai1 = None
            self.FRF_pressSlp1 = None
            self.FRF_pressTot2 = None
            self.FRF_pressTot3 = None
            return
        
        if self.parameters['acMeshDim'] == '2D':
            print("Post-processing of acoustic indicators when the pressures are calculated over 2D mesh is not supported.")
            return

        with open(self.acousticFile, 'r') as f:
            lines = f.readlines()
        f.close()

        nCols = len(lines[0].split('\t'))
        nNodes = nCols // 3
        FRF_pressTot1 = []
        FRF_pressTot2 = []
        FRF_pressTot3 = []
        FRF_pressRai1 = []
        FRF_pressSlp1 = []

        for line in lines[1:]:
            arr = line.split('\t')
            
            pTot1 = 0
            pTot2 = 0
            pTot3 = 0
            pRai1 = 0
            pSlp1 = 0

            try:
                for i in range(3):
                    pTot1 += float(arr[3*i+1])
                    pTot2 += float(arr[3*i+10])
                    pTot3 += float(arr[3*i+19])
                    pRai1 += float(arr[3*i+2])
                    pSlp1 += float(arr[3*i+3])
            except:
                print('Problem reading ' + self.acousticFile + '.')
                return
            
            pTot1 /= nNodes
            pTot2 /= nNodes
            pTot3 /= nNodes
            pRai1 /= nNodes
            pSlp1 /= nNodes
            FRF_pressTot1.append(pTot1)
            FRF_pressTot2.append(pTot2)
            FRF_pressTot3.append(pTot3)
            FRF_pressRai1.append(pRai1)
            FRF_pressSlp1.append(pSlp1)

        self.FRF_pressTot1 = np.array(FRF_pressTot1)
        self.FRF_pressTot2 = np.array(FRF_pressTot2)
        self.FRF_pressTot3 = np.array(FRF_pressTot3)
        self.FRF_pressRai1 = np.array(FRF_pressRai1)
        self.FRF_pressSlp1 = np.array(FRF_pressSlp1)

        [self.FRF_pressTot1_3rdOct, self.freq_3rdOct] = Utils.ThirdOctaveBand(self.frequency, self.FRF_pressTot1)
        [self.FRF_pressTot2_3rdOct, temp] = Utils.ThirdOctaveBand(self.frequency, self.FRF_pressTot2)
        [self.FRF_pressTot3_3rdOct, temp] = Utils.ThirdOctaveBand(self.frequency, self.FRF_pressTot3)
        [self.FRF_pressRai1_3rdOct, temp] = Utils.ThirdOctaveBand(self.frequency, self.FRF_pressRai1)
        [self.FRF_pressSlp1_3rdOct, temp] = Utils.ThirdOctaveBand(self.frequency, self.FRF_pressSlp1)

    def PlotFRFs(self, p_thirdOct=True):
        if p_thirdOct:
            x = self.freq_3rdOct

            y1 = self.FRF_railClose_3rdOct
            y2 = self.FRF_railFar_3rdOct
            y3 = self.FRF_sleeper1_3rdOct

            y4 = self.FRF_pressTot1_3rdOct
            y5 = self.FRF_pressRai1_3rdOct
            y6 = self.FRF_pressSlp1_3rdOct
            y7 = self.FRF_pressTot2_3rdOct
            y8 = self.FRF_pressTot3_3rdOct
        else:
            x = self.frequency

            y1 = self.FRF_railClose
            y2 = self.FRF_railFar
            y3 = self.FRF_sleeper1

            y4 = self.FRF_pressTot1
            y5 = self.FRF_pressRai1
            y6 = self.FRF_pressSlp1
            y7 = self.FRF_pressTot2
            y8 = self.FRF_pressTot3

        fig, axes = plt.subplots(nrows=1, ncols=2, num=self.name + p_thirdOct*" 3rd octave", figsize=(10, 5))
        plt.subplots_adjust(wspace=0.35, )

        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific('%.2e')
        formatter.set_powerlimits((0,0)) 


        plt.subplot(1, 2, 1)
        plt.plot(x, y1, label = 'Rail acceleration (0.6m)')
        plt.plot(x, y2, label = 'Rail acceleration (12m)')
        plt.plot(x, y3, label = '1st sleeper vertical acceleration')
        plt.legend()
        plt.title('Vibration FRFs')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Accelerance [g/N]')
        plt.yscale("log")
        # plt.margins(0.05, 0.05)
        ax = plt.gca()
        ax.yaxis.set_major_formatter(formatter)
        if p_thirdOct:
            plt.xscale("log")
            # plt.xticks(x)

        plt.subplot(1, 2, 2)
        plt.plot(x, y4, label = 'Total pressure (1)')
        plt.plot(x, y5, label = 'Rail pressure (1)')
        plt.plot(x, y6, label = 'Sleeper pressure (1)')
        plt.plot(x, y7, label = 'Total pressure (2)')
        plt.plot(x, y8, label = 'Total pressure (3)')
        plt.legend()
        plt.title('Acoustic FRFs')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Pressure [Pa/N]')
        plt.yscale("log")
        # plt.margins(0.05, 0.05)
        ax = plt.gca()
        ax.yaxis.set_major_formatter(formatter)
        if p_thirdOct:
            plt.xscale("log")
            # plt.xticks(x)
    
    def Mean(self, p_FRF, p_fMin, p_fMax):
        if p_FRF is None:
            return None
        
        i_fMin = np.where(self.frequency >= p_fMin)
        i_fMin = i_fMin[0][0]
        i_fMax = np.where(self.frequency <= p_fMax)
        i_fMax = i_fMax[0][-1]
        return np.mean(p_FRF[i_fMin:i_fMax+1])
    
    def integrate_spectrum(self, x, y, f_min, f_max):
        """
        Integrates an acoustic level spectrum between f_min and f_max using the trapezoidal method.

        Parameters:
        - x : array (frequencies in Hz)
        - y : array (A-weighted levels in dB)
        - f_min : float (minimum frequency in Hz)
        - f_max : float (maximum frequency in Hz)

        Returns:
        - Integral of the spectrum
        """


        mask = (x >= f_min) & (x <= f_max)
        x_filtered = x[mask]
        y = np.array(y)
        y_filtered = y[mask]

        if len(x_filtered) < 2:
            raise ValueError("Not enough points in the selected interval to integrate.")

        integral = np.trapz(y_filtered, x_filtered)
        
        return integral/(f_max-f_min)

    def apply_A_weighting_linear(self, frequency, pressure):
        """
        Apply A-weighting to an acoustic pressure signal while keeping it in the linear domain.
        The A-weighting correction is automatically interpolated for the given frequencies.

        Parameters:
        - frequency (numpy array): Frequency values in Hz.
        - pressure (numpy array): Acoustic pressure in Pa/N.

        Returns:
        - pressure_weighted (numpy array): A-weighted acoustic pressure in Pa/N.
        """  

        # Standard frequencies for A-weighting (ISO 226)
        freq_A = np.array([10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])  # Hz
        A_correction = np.array([-70.4, -50.4, -26.2, -20.6, -10.1, -3.2, 0, 1.2, -1.1, -6.6, -22.2])  # dB

        A_correction_interpolated = np.interp(frequency, freq_A, A_correction)

        pressure_dB = 20 * np.log10(np.abs(pressure) / self.p_ref)

        pressure_dB_weighted = pressure_dB + A_correction_interpolated

        pressure_weighted = self.p_ref * 10**(pressure_dB_weighted / 20)

        return pressure_weighted

    def integrate_spatial(self, p1, p2, p3, x_positions=[-20, -10, 0, 10, 20]):
        """
        Integrates an acoustic spectrum spatially using the trapezoidal method.

        Parameters:
        - p1 : array (A-weighted levels at x=0m)
        - p2 : array (A-weighted levels at x=±10m)
        - p3 : array (A-weighted levels at x=±20m)
        - x_positions : list (measurement positions, default [-20, -10, 0, 10, 20])

        Returns:
        - Spatial integral 
        """
        # Reconstruct the acoustic field spatially (symmetry assumption)
        p_spatial = np.array([p3, p2, p1, p2, p3])  # Acoustic pressures at [-20, -10, 0, 10, 20]

        # Perform numerical integration over the spatial axis
        integral_spatial = np.trapz(p_spatial, x_positions)
        
        return integral_spatial/(x_positions[-1]-x_positions[0])

    def Max(self, p_FRF, p_fMin, p_fMax):
        if p_FRF is None:
            return None
        
        i_fMin = np.where(self.frequency >= p_fMin)
        i_fMin = i_fMin[0][0]
        i_fMax = np.where(self.frequency <= p_fMax)
        i_fMax = i_fMax[0][-1]
        return np.max(p_FRF[i_fMin:i_fMax+1])
    
    def Divide(self, p_num, p_den):
        if p_num is None or p_den is None or p_den == 0:
            return None
        return p_num/p_den
    
    def ComputeIndicators(self): 
        ## Acoustic indicators
        # Total noise
        self.AI['Press_tot1_integrated'] = 20*log10(self.integrate_spectrum(self.frequency, self.FRF_pressTot1, 300, 1500)/self.p_ref)
        self.AI['Press_tot2_integrated'] = 20*log10(self.integrate_spectrum(self.frequency, self.FRF_pressTot2, 300, 1500)/self.p_ref)
        self.AI['Press_tot3_integrated'] = 20*log10(self.integrate_spectrum(self.frequency, self.FRF_pressTot3, 300, 1500)/self.p_ref)

        self.AI['Press_tot1_integrated_dBA'] = 20*log10(self.integrate_spectrum(self.frequency, self.apply_A_weighting_linear(self.frequency, self.FRF_pressTot1), 300, 1500)/self.p_ref)
        self.AI['Press_tot2_integrated_dBA'] = 20*log10(self.integrate_spectrum(self.frequency, self.apply_A_weighting_linear(self.frequency, self.FRF_pressTot2), 300, 1500)/self.p_ref)
        self.AI['Press_tot3_integrated_dBA'] = 20*log10(self.integrate_spectrum(self.frequency, self.apply_A_weighting_linear(self.frequency, self.FRF_pressTot3), 300, 1500)/self.p_ref)
        
        if self.enough_sleeper:
            #track noise : first a spatial integration over the "microphones" then a spectral integration.
            self.FRF_pressTot = []
            for i in range(len(self.FRF_pressTot1)):
                self.FRF_pressTot.append(self.integrate_spatial(self.FRF_pressTot1[i], self.FRF_pressTot2[i],self.FRF_pressTot3[i]))
            
            self.FRF_pressTotdB = 20*np.log10(np.array(self.FRF_pressTot)/self.p_ref)

            self.AI['Track_noise'] = 20*log10(self.integrate_spectrum(self.frequency, self.FRF_pressTot, 300, 1500)/self.p_ref)
            self.AI['Track_noise_dBA'] = 20*log10(self.integrate_spectrum(self.frequency, self.apply_A_weighting_linear(self.frequency, self.FRF_pressTot), 300, 1500)/self.p_ref)

            # Rail noise
            self.AI['Press_rai1_integrated'] = 20*log10(self.integrate_spectrum(self.frequency, self.FRF_pressRai1, 300, 1500)/self.p_ref)
            self.AI['Press_rai1_integrated_dBA'] = 20*log10(self.integrate_spectrum(self.frequency, self.apply_A_weighting_linear(self.frequency, self.FRF_pressRai1), 300, 1500)/self.p_ref)
            
            # Sleeper noise
            self.AI['Press_slp1_integrated'] = 20*log10(self.integrate_spectrum(self.frequency, self.FRF_pressSlp1, 300, 1500)/self.p_ref)
            self.AI['Press_slp1_integrated_dBA'] = 20*log10(self.integrate_spectrum(self.frequency, self.apply_A_weighting_linear(self.frequency, self.FRF_pressSlp1), 300, 1500)/self.p_ref)
            
        else:
            self.AI['Track_noise'] = 0
            self.AI['Track_noise_dBA'] = 0
            self.AI['Press_rai1_integrated'] = 0
            self.AI['Press_rai1_integrated_dBA'] = 0
            self.AI['Press_slp1_integrated'] = 0
            self.AI['Press_slp1_integrated_dBA'] = 0

        ## Vibration indicators
        # Rail close to excitation
        self.VI['Acce_railClose_LF_integrated'] = self.integrate_spectrum(self.frequency, self.FRF_railClose, 100, 300)
        self.VI['Acce_railClose_HF_integrated'] = self.integrate_spectrum(self.frequency, self.FRF_railClose, 300, 1500)

        # Rail far from excitation
        self.VI['Acce_railFar_LF_integrated'] = self.integrate_spectrum(self.frequency, self.FRF_railFar, 100, 300)
        self.VI['Acce_railFar_HF_integrated'] = self.integrate_spectrum(self.frequency, self.FRF_railFar, 300, 1500)

        # Rail Decay
        self.VI['RailDecay_LF'] = 20*log10(self.Divide(self.VI['Acce_railClose_LF_integrated'], self.VI['Acce_railFar_LF_integrated']))
        self.VI['RailDecay_HF'] = 20*log10(self.Divide(self.VI['Acce_railClose_HF_integrated'], self.VI['Acce_railFar_HF_integrated']))

        # Sleeper
        self.VI['Acce_sleeper_LF_integrated'] = self.integrate_spectrum(self.frequency, self.FRF_sleeper1, 100, 300)
        self.VI['Acce_sleeper_HF_integrated'] = self.integrate_spectrum(self.frequency, self.FRF_sleeper1, 300, 1500)
        self.VI['Acce_sleeper_LF_max'] = self.Max(self.FRF_sleeper1, 100, 300)
        self.VI['Acce_sleeper_HF_max'] = self.Max(self.FRF_sleeper1, 300, 1500)

    def __str__(self):
        txt = 'Name:\t' + self.name + '\n'
        txt += 'Parameter file:\t' + self.paramFile + '\n'
        txt += 'Directory:\t' + self.folder + '\n'
        txt += 'Accel file:\t' + self.accelFile + '\n'
        txt += 'Acoustic file:\t' + self.acousticFile + '\n'
        txt += str(len(self.frequency)) + ' frequencies from ' + str(self.frequency[0]) + ' Hz to ' + str(self.frequency[-1]) + ' Hz\n'
        txt += 'Acoustic indicators:\n'
        for key in self.AI.keys():
            value = self.AI[key]
            txt += '\t' + key + ' = ' + str(value) + ' dB\n'
        txt += 'Vibration indicators:\n'
        for key in self.VI.keys():
            value = self.VI[key]
            txt += '\t' + key + ' = ' + str(value) + '\n'
        txt += '\n'
        return txt
    
    def setIndicator(self,Press1,Press2,Press3,freq):
        self.FRF_pressTot1 = Press1
        self.FRF_pressTot2 = Press2
        self.FRF_pressTot3 = Press3
        self.frequency = freq
        return
    
    def write_Indicator(self,Press1,Press2,Press3,PressTot,freq,path_folder):

        fichier = open(path_folder +'\Res.txt','w')
        fichier.write('\n------------------------------')
    
        for key,value in self.AI.items():
            ligne= key + " : " + str(value)
            fichier.write('\n'+ligne)
        for key,value in self.VI.items():
            ligne= key + " : " + str(value)
            fichier.write('\n'+ligne)

        fichier.write('\n------------------------------')
        ligne='Press_tot1_integrated_with_contact_forces [dB] : ' + str(20*np.log10(self.integrate_spectrum(np.array(freq),Press1[0],300,1500)/self.p_ref))
        fichier.write('\n'+ligne)
        ligne='Press_tot2_integrated_with_contact_forces [dB] : ' + str(20*np.log10(self.integrate_spectrum(np.array(freq),Press2[0],300,1500)/self.p_ref))
        fichier.write('\n'+ligne)
        ligne='Press_tot3_integrated_with_contact_forces [dB] : ' + str(20*np.log10(self.integrate_spectrum(np.array(freq),Press3[0],300,1500)/self.p_ref))
        fichier.write('\n'+ligne)
        ligne='Press_tot1_integrated_with_contact_forces [dBA] : ' + str(20*np.log10(self.integrate_spectrum(np.array(freq),Press1[1],300,1500)/self.p_ref))
        fichier.write('\n'+ligne)
        ligne='Press_tot2_integrated_with_contact_forces [dBA] : ' + str(20*np.log10(self.integrate_spectrum(np.array(freq),Press2[1],300,1500)/self.p_ref))
        fichier.write('\n'+ligne)
        ligne='Press_tot3_integrated_with_contact_forces [dBA] : ' + str(20*np.log10(self.integrate_spectrum(np.array(freq),Press3[1],300,1500)/self.p_ref))
        fichier.write('\n'+ligne)

        fichier.write('\n' +str(20*np.log10(max(PressTot[0])/self.p_ref)))
        fichier.write('\n' + 'Track_noise_with_contact_forces [dB] : ' + str(20*log10(self.integrate_spectrum(np.array(freq), PressTot[0], 300, 1500)/self.p_ref)))
        fichier.write('\n' + 'Track_noise_with_contact_forces [dBA] : ' + str(20*log10(self.integrate_spectrum(np.array(freq), PressTot[1], 300, 1500)/self.p_ref)))
        
        fichier.close()
        return

class Utils:

    @staticmethod
    def ThirdOctaveBand(p_freqs, p_FRF):
        freqs = []
        vals = []

        bands = [
                [9, 10, 11],
                [11, 12.5, 14],
                [14, 16, 18],
                [18, 20, 22],
                [22, 25, 28],
                [28, 31.5, 35],
                [35, 40, 45],
                [45, 50, 56],
                [56, 63, 71],
                [71, 80, 89.1],
                [89.1, 100, 112],
                [112, 125, 141],
                [141, 160, 178],
                [178, 200, 224],
                [224, 250, 282],
                [282, 315, 355],
                [355, 400, 447],
                [447, 500, 562],
                [562, 630, 708],
                [708, 800, 891],
                [891, 1000, 1122],
                [1122, 1250, 1413],
                [1413, 1600, 1778],
                [1778, 2000, 2239],
                [2228, 2500, 2805],
                [2805, 3150, 3534],
                [3534, 4000, 4488]
                ]
        
        for band in bands:
            fMin = band[0]
            fMid = band[1]
            fMax = band[2]            

            if p_freqs[0] > fMin or p_freqs[-1] < fMax:
                continue

            freqsInBand = [f for f in p_freqs if f>=fMin and f<fMax]
            valsInBand = [p_FRF[i] for i,f in enumerate(p_freqs) if f>=fMin and f<fMax]
            meanVal = np.trapz(valsInBand, freqsInBand)/(fMax-fMin)
            
            freqs.append(fMid)
            vals.append(meanVal)

        return [np.array(vals), np.array(freqs)]
        

    @staticmethod
    def PrintNumpyArray(p_array, p_nDecimals):
        txt = ''
        for line in p_array:
            for val in line:
                if val is None:
                    # txt += 'None      '
                    txt += 'None' + ' '*(p_nDecimals + 4)
                else:
                    command = "txt += '%." + str(p_nDecimals) + "E' % Decimal(str(val)) + '  '"
                    # txt += str(val)
                    exec(command)
                    # txt += '%.2E' % Decimal(str(val)) + '  '
            txt += '\n'
        print(txt)


    @staticmethod
    def PlotFRFs(p_simuList):

        fig1, axes1 = plt.subplots(3,1, num='FRF1')
        # plt.subplots_adjust(wspace=0.35, )

        fig2, axes2 = plt.subplots(3,1, num='FRF2')

        for simu in p_simuList:
            plt.figure('FRF1')
            plt.subplot(3,1,1)
            plt.plot(simu.freq_3rdOct, 20*np.log10(simu.FRF_railClose_3rdOct), label=simu.name)
            plt.subplot(3,1,2)
            plt.plot(simu.freq_3rdOct, 20*np.log10(simu.FRF_railFar_3rdOct), label=simu.name)
            plt.subplot(3,1,3)
            plt.plot(simu.freq_3rdOct, 20*np.log10(simu.FRF_sleeper1_3rdOct), label=simu.name)

            plt.figure('FRF2')
            plt.subplot(3,1,1)
            plt.plot(simu.freq_3rdOct, 20*np.log10(simu.FRF_pressTot1_3rdOct), label=simu.name)
            plt.subplot(3,1,2)
            plt.plot(simu.freq_3rdOct, 20*np.log10(simu.FRF_pressTot2_3rdOct), label=simu.name)
            plt.subplot(3,1,3)
            plt.plot(simu.freq_3rdOct, 20*np.log10(simu.FRF_pressTot3_3rdOct), label=simu.name)


        xTicks = simu.freq_3rdOct
        xTicksLabels = ['{0:.5g}'.format(val) for val in xTicks]

        for i in range(2):
            plt.figure('FRF' + str(i+1))
            
            plt.subplot(3,1,1)
            plt.plot([300, 300], plt.gca().get_ylim(), 'k--', label=None)
            plt.xscale('log')
            plt.ylabel('FRF [dB]', fontsize=11)
            plt.minorticks_off()
            plt.xticks(xTicks, [])
            plt.grid(True)
            plt.legend()

            plt.subplot(3,1,2)
            plt.plot([300, 300], plt.gca().get_ylim(), 'k--', label=None)
            plt.xscale('log')
            plt.ylabel('FRF [dB]', fontsize=11)
            plt.minorticks_off()
            plt.xticks(xTicks, [])
            plt.grid(True)
            plt.legend()

            plt.subplot(3,1,3)
            plt.plot([300, 300], plt.gca().get_ylim(), 'k--', label=None)
            plt.xscale('log')
            plt.ylabel('FRF [dB]', fontsize=11)
            plt.xlabel('Frequency [Hz]', fontsize=11)
            plt.minorticks_off()
            plt.xticks(xTicks, xTicksLabels, rotation = 45, ha="center")
            plt.grid(True)
            plt.legend()

        plt.figure('FRF1')
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.suptitle('Accelerance FRFs', fontsize=14)
        plt.subplot(3,1,1)
        plt.title('Rail acceleration (0.6m)')
        plt.subplot(3,1,2)
        plt.title('Rail acceleration (12m)')
        plt.subplot(3,1,3)
        plt.title('Sleeper acceleration')

        plt.figure('FRF2')
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.suptitle('Acoustic pressure FRFs', fontsize=14)
        plt.subplot(3,1,1)
        plt.title('Point 1 (0m)')
        plt.subplot(3,1,2)
        plt.title('Point 2 (10m)')
        plt.subplot(3,1,3)
        plt.title('Point 3 (20m)')


################################################################

# indicators = SimulationResults("MUC70\Accoustic")
# lIST = indicators.FRF_pressTot
# print(lIST)

#fichier = open('MUC70_res.txt','a')

'''
for key,value in indicators.AI.items():
    ligne= key + " : " + str(value)
    print(ligne)
    fichier.write('\n'+ligne)
for key,value in indicators.VI.items():
    ligne= key + " : " + str(value)
    print(ligne)
    fichier.write('\n'+ligne)

    '''
'''
List = indicators.FRF_pressTot

print(List)
print(indicators.frequency)
fichier.close()'''