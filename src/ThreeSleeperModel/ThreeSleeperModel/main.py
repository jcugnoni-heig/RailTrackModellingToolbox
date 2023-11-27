# Raphael Nardin, Heig-VD, 08.2021

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QFileDialog, QListWidgetItem #, QWidget, QVBoxLayout, QPushButton, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QObject, QThread, pyqtSignal
import os
import sys
import time
from datetime import datetime

class Harmo3sleeperGUI(QMainWindow):
	def __init__(self):
		super(Harmo3sleeperGUI, self).__init__()
		filepath=os.path.dirname(os.path.realpath(__file__))
		uiFilePath=os.path.join(filepath,'GUI.ui')
		loadUi(uiFilePath,self)
		self.setWindowTitle('harmo3sleeper GUI')
		
		self.runDlgOpened = False
		self.running = False
		self.cwd = os.getcwd()
		self.paramFilesDir = os.path.join(self.cwd, 'temp_parameters/')
		self.simulations = []
		self.padHard = ''
		self.padSoft = ''
		self.ballastE = os.path.join(self.cwd, 'Materials_properties/E_wood.csv')
		self.ballastTanD = os.path.join(self.cwd, 'Materials_properties/tanD_wood.csv')
		self.USPE = os.path.join(self.cwd, 'Materials_properties/E_sylomer.csv')
		self.USPTanD = os.path.join(self.cwd, 'Materials_properties/tanD_sylomer.csv')
		
		#txt = ['300.00\n318.60\n333.26\n344.80\n353.90\n361.07\n366.72\n371.17\n374.68\n377.45\n379.62\n381.34\n382.69\n383.76\n384.84\n386.05\n387.38\n388.87\n390.52\n392.36\n394.40\n396.66\n399.18\n401.98\n405.08\n408.53\n412.37\n416.63\n421.37\n426.63\n432.47\n438.96\n446.18\n454.19\n463.10\n472.99\n483.99\n496.20\n509.77\n524.85\n541.60\n560.19\n576.71\n591.40\n604.46\n616.07\n626.39\n635.56\n643.72\n650.97', '\n657.41\n663.14\n668.23\n672.76\n676.79\n680.36\n683.54\n686.37\n688.88\n691.12\n693.11\n694.87\n696.44\n697.84\n699.08\n700.18\n701.20\n702.31\n703.54\n704.88\n706.35\n707.97\n709.74\n711.68\n713.81\n716.15\n718.71\n721.52\n724.61\n727.99\n731.70\n735.77\n740.23\n745.13\n750.50\n756.39\n762.85\n769.94\n777.71\n786.24\n795.59\n805.84\n817.09\n829.43\n842.97\n857.81\n874.09\n891.95\n909.56\n925.47', '\n939.84\n952.81\n964.53\n975.11\n984.67\n993.31\n1001.10\n1008.15\n1014.51\n1020.25\n1025.44\n1030.12\n1034.36\n1038.18\n1041.63\n1044.75\n1047.56\n1050.11\n1052.40\n1054.48\n1056.35\n1058.04\n1059.57\n1060.95\n1062.20\n1063.33\n1064.34\n1065.42\n1066.59\n1067.87\n1069.27\n1070.79\n1072.46\n1074.27\n1076.24\n1078.40\n1080.75\n1083.32\n1086.12\n1089.17\n1092.50\n1096.13\n1100.09\n1104.41\n1109.12\n1114.26\n1119.86\n1125.97\n1132.64\n1139.91', '\n1147.85\n1156.50\n1165.94\n1176.23\n1187.45\n1199.70\n1213.06\n1227.62\n1243.51\n1260.85\n1279.14\n1295.78\n1310.91\n1324.66\n1337.17\n1348.54\n1358.88\n1368.28\n1376.83\n1384.61\n1391.68\n1398.10\n1403.95\n1409.26\n1414.09\n1418.49\n1422.48\n1426.11\n1429.42\n1432.42\n1435.15\n1437.63\n1439.89\n1441.95\n1443.81\n1445.51\n1447.05\n1448.46\n1449.73\n1450.89\n1451.95\n1453.11\n1454.70\n1456.86\n1459.80\n1463.81\n1469.28\n1476.73\n1486.88\n1500.00']
		txt = ['300.00\n308.39\n316.78\n325.17\n333.57\n341.96\n350.35\n358.74\n367.13\n375.52\n383.92\n392.31\n400.70\n409.09\n417.48\n425.87\n434.27\n442.66\n451.05\n459.44\n467.83\n476.22\n484.62\n493.01\n501.40\n509.79\n518.18\n526.57\n534.97\n543.36\n551.75\n560.14\n568.53\n576.92\n585.31\n593.71\n', '\n602.10\n610.49\n618.88\n627.27\n635.66\n644.06\n652.45\n660.84\n669.23\n677.62\n686.01\n694.41\n702.80\n711.19\n719.58\n727.97\n736.36\n744.76\n753.15\n761.54\n769.93\n778.32\n786.71\n795.10\n803.50\n811.89\n820.28\n828.67\n837.06\n845.45\n853.85\n862.24\n870.63\n879.02\n887.41\n895.80\n', '\n904.20\n912.59\n920.98\n929.37\n937.76\n946.15\n954.55\n962.94\n971.33\n979.72\n988.11\n996.50\n1004.90\n1013.29\n1021.68\n1030.07\n1038.46\n1046.85\n1055.24\n1063.64\n1072.03\n1080.42\n1088.81\n1097.20\n1105.59\n1113.99\n1122.38\n1130.77\n1139.16\n1147.55\n1155.94\n1164.34\n1172.73\n1181.12\n1189.51\n1197.90\n', '\n1206.29\n1214.69\n1223.08\n1231.47\n1239.86\n1248.25\n1256.64\n1265.03\n1273.43\n1281.82\n1290.21\n1298.60\n1306.99\n1315.38\n1323.78\n1332.17\n1340.56\n1348.95\n1357.34\n1365.73\n1374.13\n1382.52\n1390.91\n1399.30\n1407.69\n1416.08\n1424.48\n1432.87\n1441.26\n1449.65\n1458.04\n1466.43\n1474.83\n1483.22\n1491.61\n1500.00']
		self.freqBands = Simulation.SortedFrequencies(txt)
		# self.freqBands = [[300], None, None, None]
		self.killAster = 'pids=$(pgrep aster) && kill -s USR1 $pids'
		
		self.btn_addToList.clicked.connect(self.AddSimuToList)
		self.actionQuit.triggered.connect(self.closeApp)
		self.list_simu.currentItemChanged.connect(self.DisplaySimu)
		self.btn_deleteSimu.clicked.connect(self.DeleteSimu)
		self.btn_moveUp.clicked.connect(self.MoveSimuUp)
		self.btn_moveDown.clicked.connect(self.MoveSimuDown)
		self.btn_browseHardE.clicked.connect(self.BrowseHardMatE)
		self.btn_browseSoftE.clicked.connect(self.BrowseSoftMatE)
		self.btn_browseHardTanD.clicked.connect(self.BrowseHardMatTanD)
		self.btn_browseSoftTanD.clicked.connect(self.BrowseSoftMatTanD)
		self.cbb_padHard.currentIndexChanged.connect(self.padHardChange)
		self.cbb_padSoft.currentIndexChanged.connect(self.padSoftChange)
		self.btn_ballastE.clicked.connect(self.BrowseBallastE)
		self.btn_ballastTanD.clicked.connect(self.BrowseBallastTanD)
		self.btn_USPE.clicked.connect(self.BrowseUSPE)
		self.btn_USPTanD.clicked.connect(self.BrowseUSPTanD)
		self.cb_USPs.stateChanged.connect(self.DisableUSPs)
		self.btn_simulateAll.clicked.connect(self.SimulateAll)
		self.btn_freqs.clicked.connect(self.EditFreqsCPUs)
		
		self.FillComboboxMesh()
		
	def FillComboboxMesh(self):
		file = './Meshes_list.txt'
		with open(file) as f:
			lines = f.read().splitlines()
		f.close()
		
		for line in lines:
			self.cbb_padMesh.addItem(line)
		
	def AddSimuToList(self):
		if self.running == True:
			return
		# Get parameters
		workingDir = self.cwd
		simuName = self.txt_simuName.text()
		
		if len(simuName) == 0 or '/' in simuName or '\\' in simuName:
			QMessageBox.information(self, 'Error', 'Please enter a correct simulation name.', QMessageBox.Ok,)
			return
			
		for sim in self.simulations:
			if sim.simuName == simuName:
				QMessageBox.information(self, 'Error', 'This simulation name already exists.', QMessageBox.Ok,)
				return

		saveDir = self.txt_saveToDir.text()
		
		if len(saveDir) == 0:
			QMessageBox.information(self, 'Error', 'Please enter a directory to save the results.', QMessageBox.Ok,)
			return
			
		if not os.path.exists(saveDir):	
			try:
				os.makedirs(saveDir)
			except:
				QMessageBox.information(self, 'Error', 'Please enter a correct directory name to save the results.', QMessageBox.Ok,)
				return
		
		USPs = self.cb_USPs.isChecked()
		acoustic = self.cb_computeAcoust.isChecked()
		if self.rb_load45.isChecked() == True:
			loadDir = 45
		elif self.rb_load10.isChecked() == True:
			loadDir = 10
			
		padMesh = self.cbb_padMesh.currentText()
		
		if self.cbb_padHard.currentIndex() == 0:
			padHard = self.padHard
		else:
			padHard = self.cbb_padHard.currentText()
		
		if self.cbb_padSoft.currentIndex() == 0:
			padSoft = self.padSoft
		else:
			padSoft = self.cbb_padSoft.currentText()
			
		nuHard = self.txt_nuHard.text()
		nuSoft = self.txt_nuSoft.text()
		rhoHard = self.txt_rhoHard.text()
		rhoSoft = self.txt_rhoSoft.text()
		
		balNu = self.txt_balNu.text()
		balRho = self.txt_balRho.text()
		
		USPNu = self.txt_USPnu.text()
		USPRho = self.txt_USPrho.text()
		
		try: 
			nuH_temp = float(nuHard)
			nuS_temp = float(nuSoft)
			rhoH_temp = float(rhoHard)
			rhoS_temp = float(rhoSoft)
			
			balNu_temp = float(balNu)
			balRho_temp = float(balRho)
			
			USPNu_temp = float(USPNu)
			USPRho_temp = float(USPRho)
		except:
			QMessageBox.information(self, 'Error', 'Please enter correct densities and Poisson''s ratios.', QMessageBox.Ok,)
			return
			
		if nuH_temp < 0 or nuH_temp >= 0.5 or nuS_temp < 0 or nuS_temp >= 0.5 or balNu_temp < 0 or balNu_temp >= 0.5 or USPNu_temp < 0 or USPNu_temp >= 0.5:
			QMessageBox.information(self, 'Error', 'Poisson''s ratios must be between 0 and 0.5.', QMessageBox.Ok,)
			return
			
		if rhoH_temp < 0 or rhoS_temp < 0 or balRho_temp < 0 or USPRho_temp < 0:
			QMessageBox.information(self, 'Error', 'Please enter correct densities.', QMessageBox.Ok,)
			return
			
		balE = self.ballastE
		balTanD = self.ballastTanD
		USPE = self.USPE
		USPTanD = self.USPTanD

		freqs = self.freqBands
		
		if (type(padHard) == list and '' in padHard) or (type(padSoft) == list and '' in padSoft):
			QMessageBox.information(self, 'Error', 'Please select the pads materials.', QMessageBox.Ok,)
			return
			
		if not os.path.exists(self.paramFilesDir):
			os.makedirs(self.paramFilesDir)
		paramFileName = os.path.join(self.paramFilesDir, 'parameters_' + simuName + '.py')
		
		# Simu creation & append to listView & list of Simus
		newSimu = Simulation(self, paramFileName, workingDir, simuName, saveDir, freqs, USPs, acoustic, loadDir, padMesh, padHard, padSoft, nuHard, nuSoft, rhoHard, rhoSoft, balE, balTanD, balNu, balRho, USPE, USPTanD, USPNu, USPRho)
		self.simulations.append(newSimu)
		newListItem = QListWidgetItem(simuName)
		self.list_simu.addItem(newListItem)
		self.list_simu.setCurrentRow(self.list_simu.count()-1)
		
		newSimu.WriteParameterFile()
	
	def SimulateAll(self):
		if self.running == True:
			return
			
		if self.runDlgOpened == True:
			return
			
		n = self.list_simu.count()
		if n == 0:
			return
		
		simulationsOrdered = []
		for i in range(n):
			item = self.list_simu.item(i)
			txt = item.text()
			for simu in self.simulations:
				if simu.simuName == txt:
					simulationsOrdered.append(simu)
					break
		
		uiPath = os.path.join(self.cwd,'run.ui')
		dialog = Dialog_Run(self, uiPath, simulationsOrdered)
		dialog.show()
		dialog.exec_()
				
		try: os.rmdir(self.paramFilesDir)
		except: pass
		

	def DisplaySimu(self): #called when the index of list_simu is changed
		simu = self.SelectedSimu()
		if simu == None:
			return		
		
		simu.Display()
		self.padHard = simu.padHard
		self.padSoft = simu.padSoft
		self.ballastE = simu.ballastE
		self.ballastTanD = simu.ballastTanD
		self.USPE = simu.USPE
		self.USPTanD = simu.USPTanD
		
	def DeleteSimu(self):
		if self.running == True:
			return
			
		simu = self.SelectedSimu()
		if simu == None:
			return
			
		dir = os.path.dirname(simu.paramFileName)
		if os.path.exists(simu.paramFileName):
			os.remove(simu.paramFileName)
		if os.path.exists(dir):
			if not os.listdir(dir):
				os.rmdir(dir)
			
		self.simulations.remove(simu)
		item = self.list_simu.currentItem()
		self.list_simu.takeItem(self.list_simu.row(item))
		if len(self.simulations) == 0:
			self.DisplaySimu()
	
	def MoveSimuUp(self):
		if self.running == True:
			return
			
		i = self.list_simu.currentRow()
		if i == 0 or self.list_simu.count() == 0:
			return
			
		item = self.list_simu.item(i)
		self.list_simu.takeItem(i)
		self.list_simu.insertItem(i-1, item)
		self.list_simu.setCurrentRow(i-1)
		
	def MoveSimuDown(self):
		if self.running == True:
			return
			
		i = self.list_simu.currentRow()
		n = self.list_simu.count()
		if n == 0 or i == n-1:
			return
			
		item = self.list_simu.item(i)
		self.list_simu.takeItem(i)
		self.list_simu.insertItem(i+1, item)
		self.list_simu.setCurrentRow(i+1)
		
	def BrowseHardMatE(self):
		self.padHard = self.BrowseFilePad(self.padHard, 0, 'Browse hard material Young''s modulus')
	
	def BrowseHardMatTanD(self):
		self.padHard = self.BrowseFilePad(self.padHard, 1, 'Browse hard material Tan Delta')
	
	def BrowseSoftMatE(self):
		self.padSoft = self.BrowseFilePad(self.padSoft, 0, 'Browse soft material Young''s modulus')
	
	def BrowseSoftMatTanD(self):
		self.padSoft = self.BrowseFilePad(self.padSoft, 1, 'Browse soft material Tan Delta')
		
	def BrowseBallastE(self):
		self.ballastE = self.BrowseFile(self.ballastE, 'Browse ballast Young''s modulus')
		
	def BrowseBallastTanD(self):
		self.ballastTanD = self.BrowseFile(self.ballastTanD, 'Browse ballast Tan Delta')
		
	def BrowseUSPE(self):
		self.USPE = self.BrowseFile(self.USPE, 'Browse USP Young''s modulus')
		
	def BrowseUSPTanD(self):
		self.USPTanD = self.BrowseFile(self.USPTanD, 'Browse USP Tan Delta')
		
	def BrowseFile(self, p_prop, p_txt):
		file = QFileDialog.getOpenFileName(self, p_txt, p_prop)
		if file[0] == '':
			return p_prop  # no file selected. Leave property as it was
			
		p_prop = file[0]
		return p_prop
		
	def BrowseFilePad(self, p_pad, p_num, p_txt):
		if type(p_pad) == list and os.path.isfile(p_pad[p_num]) == True: # a file has already been selected
			path = p_pad[p_num]
		else:
			path = self.cwd + "/Materials_properties"

		file = QFileDialog.getOpenFileName(self, p_txt, path)
		if file[0] == '':
			return p_pad # no file selected. Leave self.padHard as it was

		if type(p_pad) != list:
			p_pad = ['', '']

		p_pad[p_num] = file[0] # a file was selected. affect if to self.padHard, which will be used to create a new simu later
		return p_pad
		
	def padHardChange(self):
		if self.cbb_padHard.currentIndex() == 0:
			self.btn_browseHardE.setDisabled(False)
			self.btn_browseHardTanD.setDisabled(False)
		else:
			self.btn_browseHardE.setDisabled(True)
			self.btn_browseHardTanD.setDisabled(True)
			self.UpdateNuPad(self.cbb_padHard, self.txt_nuHard)
			
	def padSoftChange(self):
		if self.cbb_padSoft.currentIndex() == 0:
			self.btn_browseSoftE.setDisabled(False)
			self.btn_browseSoftTanD.setDisabled(False)
		else:
			self.btn_browseSoftE.setDisabled(True)
			self.btn_browseSoftTanD.setDisabled(True)
			self.UpdateNuPad(self.cbb_padSoft, self.txt_nuSoft)
			
	def UpdateNuPad(self, p_comboBox, p_textBox):
		mat = p_comboBox.currentText()
		if mat == 'EVA':
			nu = 0.484
		elif mat == 'PIB':
			nu = 0.495
		elif mat == 'PUhard' or mat == 'PUsoft':
			nu = 0.3
		p_textBox.setText(str(nu))

	
	def SelectedSimu(self):
		item = self.list_simu.currentItem()
		
		if item == None:
			return None
			
		name = item.text()
	
		for simu in self.simulations:
			if simu.simuName == name:
				return simu
		return None
		
		
	def DisableUSPs(self):
		USP_on = self.cb_USPs.isChecked()
		self.txt_USPnu.setDisabled(not USP_on)
		self.txt_USPrho.setDisabled(not USP_on)
		self.btn_USPE.setDisabled(not USP_on)
		self.btn_USPTanD.setDisabled(not USP_on)
		
	def EditFreqsCPUs(self):
		uiPath = os.path.join(self.cwd,'freqsCPUedit.ui')
		dialog = Dialog_CPUs(uiPath)
		
		cb_CPUs = [dialog.cb_CPU1, dialog.cb_CPU2, dialog.cb_CPU3, dialog.cb_CPU4]
		txt_freqs = [dialog.txt_freq1, dialog.txt_freq2, dialog.txt_freq3, dialog.txt_freq4]

		for i in range(len(self.freqBands)):
			band = self.freqBands[i]
			if band == None:
				cb_CPUs[i].setChecked(False)
				txt_freqs[i].setPlainText('')
				continue
			bandStr = [str(j) for j in band]
			txt = '\n'.join(bandStr)
			txt_freqs[i].setPlainText(txt)
		
		dialog.show()
		dialog.exec_()
		
		if dialog.returnCode == 1:
			return
		
		self.freqBands = dialog.sortedFreqBands
		
	def closeEvent(self, event):
		self.closeApp()
		
	def closeApp(self):
		dir = self.paramFilesDir
		if not os.path.exists(dir):
			self.close()
			return
			
		for fileName in os.listdir(dir):
			path = os.path.join(dir, fileName)
			try: os.remove(path)
			except: pass
		try: os.rmdir(dir)
		except: pass
		
		self.close()
	

class Dialog_CPUs(QDialog):
	def __init__(self, p_uiPath):
		super(Dialog_CPUs, self).__init__()
		loadUi(p_uiPath, self)
		self.setWindowTitle('Frequency bands selection')
		self.setModal(True)
		
		self.btn_freqOK.clicked.connect(self.OK)
		self.btn_freqCancel.clicked.connect(self.Cancel)
		
		self.txt1 = None
		self.txt2 = None
		self.txt3 = None
		self.txt4 = None
		self.sortedFreqBands = None
		
		self.returnCode = 0
		
	def OK(self):
		if self.cb_CPU1.isChecked() == True:
			self.txt1 = self.txt_freq1.toPlainText()
		if self.cb_CPU2.isChecked() == True:
			self.txt2 = self.txt_freq2.toPlainText()
		if self.cb_CPU3.isChecked() == True:
			self.txt3 = self.txt_freq3.toPlainText()
		if self.cb_CPU4.isChecked() == True:
			self.txt4 = self.txt_freq4.toPlainText()
		
		if self.txt1 == None and self.txt2 == None and self.txt3 == None and self.txt4 == None:
			QMessageBox.information(self, 'Error', 'You must select at least one frequency.', QMessageBox.Ok,)
			return
			
		freqBandsStr = [self.txt1, self.txt2, self.txt3, self.txt4]
		sortedFreqs = Simulation.SortedFrequencies(freqBandsStr)
		minMax = []
		
		for freqs in sortedFreqs:
			if freqs == None:
				continue
			minMax.append(min(freqs))
			minMax.append(max(freqs))
			
		if sorted(minMax) != minMax:
			QMessageBox.information(self, 'Error', 'Frequency bands should not overlap.', QMessageBox.Ok,)
			return
		
		commonElems = False
		for i in range(len(sortedFreqs)-1):
			listI = sortedFreqs[i]
			if listI == None:
				continue
			for j in range(i+1, len(sortedFreqs)):
				listJ = sortedFreqs[j]
				if listJ == None:
					continue
				set_I = set(listI)
				set_J = set(listJ)
				if len(set_I.intersection(set_J)) > 0:
					commonElems = True
					QMessageBox.information(self, 'Error', 'Each frequency must appear once.', QMessageBox.Ok,)
					return
			
		self.sortedFreqBands = sortedFreqs
		self.close()
		
	def Cancel(self):
		self.returnCode = 1
		self.close()
		
	

class Worker(QObject):
	finished = pyqtSignal()
	progress = pyqtSignal(int)

	def __init__(self, p_simu):
		super(Worker, self).__init__()
		self.simulation = p_simu

	def run(self):
		runPath = os.path.join(self.simulation.workingDir, 'RUN.sh')
		paramFile = self.simulation.paramFileName
		os.system(runPath + ' ' + paramFile)

		self.finished.emit()
		
class Dialog_Run(QDialog):
	def __init__(self, p_interface, p_uiPath, p_simulations):
		super(Dialog_Run, self).__init__()
		loadUi(p_uiPath, self)
		self.setWindowTitle('Run simulations')	
		
		self.interface = p_interface
		self.simulations = p_simulations
		for simu in self.simulations:
			simu.runInterface = self
			simu.thread = None
			
		self.timer = QTimer()
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.TimerTicks)
		self.interface.running = False
		self.message = ''
		self.iCurrentSimu = 0
		self.interface.runDlgOpened = True
		
		self.btn_run.clicked.connect(self.button_run)
		self.btn_stop.clicked.connect(self.button_stop)
		self.btn_runClose.clicked.connect(self.button_close)
		
	def closeEvent(self, event):
		self.button_close()
		
	def button_close(self):
		if self.interface.running == True:
			reply = QMessageBox.question(self.interface, 'Info', 'Closing will stop the current execution. Are you sure ?', QMessageBox.Yes, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.button_stop()
				self.interface.runDlgOpened = False
				self.close()
		else:
			self.interface.runDlgOpened = False
			self.button_stop()
			self.close()
		
	def button_run(self):
		if self.iCurrentSimu >= len(self.simulations):
			QMessageBox.information(self.interface, 'Info', 'All simulations have been run.', QMessageBox.Ok,)
			return
		if self.interface.running == True:
			QMessageBox.information(self.interface, 'Info', 'A simulation is already running.', QMessageBox.Ok,)
			return
			
		self.interface.running=True
		self.timer.start()
		
	def button_stop(self):
		self.timer.stop()
		
		dir = os.path.dirname(self.interface.paramFilesDir)		
		if os.path.exists(dir) == True:
			for fileName in os.listdir(dir):
				path = os.path.join(dir, fileName)
				os.remove(path)
			os.rmdir(dir)
		
		if self.interface.running == False or self.CurrentSimu == None or self.CurrentSimu.thread == None:
			self.interface.running = False
			return

		os.system(self.interface.killAster)
		# t0 = time.time()
		while self.CurrentSimu.thread.isRunning() == True: # and time.time()-t0 < 20:
			now = datetime.now()
			date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
			self.txt_info.appendPlainText('[' + date_time + '] Killing simulation ' + self.CurrentSimu.simuName + '...')
			self.txt_info.repaint()
			time.sleep(10)
			self.CurrentSimu.thread.terminate()
			self.CurrentSimu.thread.quit()
			self.CurrentSimu.thread.exit()
			# os.system('salome killall')
			
		now = datetime.now()
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		self.txt_info.appendPlainText('[' + date_time + '] Simulation ' + self.CurrentSimu.simuName + ' was killed.')
		self.txt_info.repaint()

		self.interface.running = False
		self.CurrentSimu.thread = None

	def TimerTicks(self):
		simu = self.CurrentSimu
		if simu == None:
			return
		if simu.thread == None: # current simu not simulated yet
			simu.Run() # starts running
			return
		
		isRunning = True
		try:
			isRunning = simu.thread.isRunning()
		except:
			isRunning = False
		
		if isRunning == True: # current simulation is running
			# self.UpdateText()
			pass
		else: # current simulation over ; stop if over OR run next simu
			self.iCurrentSimu += 1
			if self.iCurrentSimu >= len(self.simulations): # last simulation over
				# self.iCurrentSimu = 0
				now = datetime.now()
				date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
				self.txt_info.appendPlainText('[' + date_time + '] Last simulation completed.')
				self.txt_info.repaint()
				self.button_stop()
				return
			
			os.remove(simu.paramFileName)
			simu = self.CurrentSimu # Run next simu
			simu.Run()
			self.message += '\n'
	
	# unused with thread version
	def UpdateText(self):
		simu = self.CurrentSimu
		# for i in range(50):
		try:
			text='OK'
			if text == ' ' or text == '\n':
				return
			self.message=self.message+text
			self.txt_info.setPlainText(self.message)
			self.txt_info.repaint()
		except: 
			pass
				
	@property
	def CurrentSimu(self):
		if self.iCurrentSimu >= len(self.simulations):
			return None
		return self.simulations[self.iCurrentSimu]
		
		

		
class Simulation:
	def __init__(self, p_interface, p_paramFileName, p_workingDir, p_simuName, p_saveDir, p_freqBands, p_USPs, p_acoustic, p_loadDir, p_padMesh, p_padHard, p_padSoft, p_nuHard, p_nuSoft, p_rhoHard, p_rhoSoft, p_balE, p_balTanD, p_balNu, p_balRho, p_USPE, p_USPTanD, p_USPNu, p_USPRho):
		self.interface = p_interface
		self.paramFileName = p_paramFileName
		self.workingDir = p_workingDir
		self.simuName = p_simuName
		self.saveDir = p_saveDir
		self.freqBands = p_freqBands
		self.USPs = p_USPs
		self.acoustic = p_acoustic
		self.padMesh = p_padMesh
		self.padHard = p_padHard
		self.padSoft = p_padSoft
		self.nuHard = p_nuHard
		self.nuSoft = p_nuSoft
		self.rhoHard = p_rhoHard
		self.rhoSoft = p_rhoSoft
		self.loadDir = p_loadDir
		self.ballastE = p_balE
		self.ballastTanD = p_balTanD
		self.balNu = p_balNu
		self.balRho = p_balRho
		self.USPE = p_USPE
		self.USPTanD = p_USPTanD
		self.USPNu = p_USPNu
		self.USPRho = p_USPRho
		
		if self.saveDir[-1] != os.sep:
			self.saveDir += os.sep
		
		self.thread = None
		
	def WriteParameterFile(self):
		txt = "simuName = '" + self.simuName + "'\n"
		txt += "nCPUs = " + str(self.NCPU) + "\n"
		txt += "saveToDir = '" + self.saveDir + "'\n"
		txt += "includeUSPs = " + str(self.USPs) + "\n"
		txt += "computeAcoustic = " + str(self.acoustic) + "\n"
		txt += "excitNode = 'noeuForc'\n"
		if self.loadDir == 45:
			txt += "force = (0, -173205.0, -173205.0)\n"
		elif self.loadDir == 10:
			txt += "force = (0, -100000.0, 10000.0)\n"
		txt += "acousticGrid = 'acGrid_hemisphere_7m_389n'\n"
		txt += "padMesh = '" + self.padMesh + "'\n"
		
		if type(self.padHard) == list:
			txt += "padHardE = '" + self.padHard[0] + "'\n"
			txt += "padHardTanD = '" + self.padHard[1] + "'\n"
		else:
			txt += "padHardE = '" + self.padHard + "'\n"
			txt += "padHardTanD = '" + self.padHard + "'\n"
		txt += "nuHard = " + self.nuHard + "\n"
		txt += "rhoHard = " + self.rhoHard + "e-9\n"
		
		if type(self.padSoft) == list:
			txt += "padSoftE = '" + self.padSoft[0] + "'\n"
			txt += "padSoftTanD = '" + self.padSoft[1] + "'\n"
		else:
			txt += "padSoftE = '" + self.padSoft + "'\n"
			txt += "padSoftTanD = '" + self.padSoft + "'\n"
		txt += "nuSoft = " + self.nuSoft + "\n"
		txt += "rhoSoft = " + self.rhoSoft + "e-9\n"
		
		txt += "ballastE = '" + self.ballastE + "'\n"
		txt += "ballastTanD = '" + self.ballastTanD + "'\n"
		txt += "balNu = " + self.balNu + "\n"
		txt += "balRho = " + self.balRho + "e-9\n"
		
		txt += "USPE = '" + self.USPE + "'\n"
		txt += "USPTanD = '" + self.USPTanD + "'\n"
		txt += "USPNu = " + self.USPNu + "\n"
		txt += "USPRho = " + self.USPRho + "e-9\n"
		
		dir = os.path.dirname(self.paramFileName)
		if not os.path.exists(dir):
			os.makedirs(dir)
			
		paramFile=open(self.paramFileName,'w')
		paramFile.write(txt)
		paramFile.close()
	
	def Run(self):
		self.thread = QThread()
		self.worker = Worker(self)
		self.worker.moveToThread(self.thread)
		self.thread.started.connect(self.worker.run)
		self.worker.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.worker.deleteLater)
		self.thread.finished.connect(self.thread.deleteLater)
		# self.worker.progress.connect(self.reportProgress)
	
		if os.path.exists(self.paramFileName) == False:
			self.WriteParameterFile()
		self.WriteFrequencyFiles()
		
		# runPath = os.path.join(self.workingDir, 'RUN.sh')
		# paramFile = self.paramFileName
		# self.subprocess=subprocess.Popen([runPath, paramFile], stdout=subprocess.PIPE)
		# self.pipe=self.subprocess.stdout
		
		now = datetime.now()
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		self.runInterface.txt_info.appendPlainText('[' + date_time + '] Running simulation: ' + self.simuName + ' ...')
		self.runInterface.txt_info.repaint()
		self.thread.start()
	
	
	def Run2(self):
		if os.path.exists(self.paramFileName) == False:
			self.WriteParameterFile()
			
		self.WriteFrequencyFiles()
		
		os.system('bash RUN.sh ' + self.paramFileName)
		
		os.remove(self.paramFileName)
		
	def WriteFrequencyFiles(self):
		i = 0
		iBandNone = len(self.freqBands)
		
		for band in self.freqBands:
			
			if band == None:
				freqFilePath = os.path.join(self.workingDir, 'frequencies_b' + str(iBandNone) + '.txt')
				freqFile = open(freqFilePath, 'w')
				freqFile.write('')
				freqFile.close()
				iBandNone -= 1
				continue
			
			bandStr = [str(j) for j in band]
			txt = '\n'.join(bandStr)
			
			freqFilePath = os.path.join(self.workingDir, 'frequencies_b' + str(i+1) + '.txt')
			freqFile = open(freqFilePath, 'w')
			freqFile.write(txt)
			freqFile.close()
			i += 1		
	
	def Display(self):
		self.interface.txt_simuName.setText(self.simuName)
		self.interface.txt_saveToDir.setText(self.saveDir)
		self.interface.cb_USPs.setChecked(self.USPs)
		self.interface.cb_computeAcoust.setChecked(self.acoustic)
		
		if self.loadDir == 45:
			self.interface.rb_load45.setChecked(True)
		elif self.loadDir == 10:
			self.interface.rb_load10.setChecked(True)
		
		self.interface.cbb_padMesh.setCurrentText(self.padMesh)
		
		if type(self.padHard) == list:
			self.interface.cbb_padHard.setCurrentIndex(0)
		else:
			self.interface.cbb_padHard.setCurrentText(self.padHard)
		
		if type(self.padSoft) == list:
			self.interface.cbb_padSoft.setCurrentIndex(0)
		else:
			self.interface.cbb_padSoft.setCurrentText(self.padSoft)
		
		self.interface.txt_nuHard.setText(self.nuHard)
		self.interface.txt_nuSoft.setText(self.nuSoft)
		self.interface.txt_rhoHard.setText(self.rhoHard)
		self.interface.txt_rhoSoft.setText(self.rhoSoft)
		
		self.interface.txt_balNu.setText(self.balNu)
		self.interface.txt_balRho.setText(self.balRho)
		
		self.interface.txt_USPnu.setText(self.USPNu)
		self.interface.txt_USPrho.setText(self.USPRho)
		
		self.interface.freqBands = self.freqBands
		
		
	@property
	def NCPU(self):
		i = 0
		for band in self.freqBands:
			if band != None:
				i += 1
		
		return i
		
	@staticmethod
	def SortedFrequencies(p_allFields):
	# p_allFields = ['100\n200\n300', '400\n500\n', etc]
		sortedFreqs = []
		
		for fields in p_allFields:
			if fields == None:
				sortedFreqs.append(None)
				continue
				
			fieldsArray = fields.split('\n')				
			freqsArray = []
			
			frequencyFound = False
			for txt in fieldsArray:
				try:
					freq = float(txt)
				except:
					continue
				freqsArray.append(freq)
				frequencyFound = True
				
			if frequencyFound == False:
				sortedFreqs.append(None)
				continue
			
			freqsArray = sorted(freqsArray)
			sortedFreqs.append(freqsArray)
			
		return sortedFreqs
		
		
		
		
if __name__ == '__main__':
	app = QApplication([]) #sys.argv
	widget = Harmo3sleeperGUI()
	widget.show()
	sys.exit(app.exec_())