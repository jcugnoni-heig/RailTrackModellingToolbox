import os
import sys
import shutil
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import pyperclip as clipboard
#import clipboard
import module_run as mod
import json
import multiprocessing


class MultiSleeperModelGUI(QMainWindow):
	def __init__(self):
		super(MultiSleeperModelGUI, self).__init__()
		appPath = os.path.dirname(os.path.realpath(__file__))
		uiFilePath=os.path.join(appPath,'GUI.ui')
		loadUi(uiFilePath,self)
		self.setWindowTitle('Multi-sleeper model')
		
		self.cb_phase1.stateChanged.connect(self.Phase1StateChanged)
		self.btn_selPhase1Folder.clicked.connect(self.SelectModesFolder)
		self.btn_railMesh.clicked.connect(self.SelectRailMesh)
		self.btn_padMesh.clicked.connect(self.SelectPadMesh)
		self.btn_Emat1.clicked.connect(self.SelectEmat1)
		self.btn_Emat2.clicked.connect(self.SelectEmat2)
		self.btn_tanDmat1.clicked.connect(self.SelectTanDmat1)
		self.btn_tanDmat2.clicked.connect(self.SelectTanDmat2)
		self.btn_sleeperMesh.clicked.connect(self.SelectSleeperMesh)
		self.btn_Ebal.clicked.connect(self.SelectEbal)
		self.btn_tanDbal.clicked.connect(self.SelectTanDbal)
		self.btn_EUSP.clicked.connect(self.SelectEUSP)
		self.btn_tanDUSP.clicked.connect(self.SelectTanDUSP)
		self.btn_USPMesh.clicked.connect(self.SelectUSPMesh)
		self.cb_USP.stateChanged.connect(self.USPStateChanged)
		self.btn_freqs.clicked.connect(self.SelectFrequencies)
		self.cb_defaultNode.stateChanged.connect(self.DefaultNodeStateChanged)
		self.rb_10pct.toggled.connect(self.LoadDirChanged)
		self.btn_selectSubstructures.clicked.connect(self.SelectSubstructures)
		self.cb_computeAcoustic.stateChanged.connect(self.ComputeAcousticStateChanged)
		self.btn_selectAcousticMesh.clicked.connect(self.SelectAcousticMesh)
		self.btn_addSimu.clicked.connect(self.AddSimuToList)
		self.btn_simuDir.clicked.connect(self.SelectSimuDir)
		self.btn_simulate.clicked.connect(self.SimulateAll)
		self.btn_savePhase1To.clicked.connect(self.SelectModesParentFolder)
		self.actionExit.triggered.connect(self.closeApp)
		self.btn_deleteSimu.clicked.connect(self.DeleteSimu)
		self.btn_moveUp.clicked.connect(self.MoveSimuUp)
		self.btn_moveDown.clicked.connect(self.MoveSimuDown)
		self.list_simu.currentItemChanged.connect(self.DisplaySimu)
				
		self.appPath = appPath # src/MultiSleeperModel/DevFiles/
		temp = os.path.dirname(appPath)
		self.cwd = os.path.dirname(temp) # src/MultiSleeperModel/
		self.simuList = []
		self.modesParentFolder = None
		self.modesFolder = None
		self.frequencies = [100.0, 106.9930068, 115.3846152, 123.7762236, 132.167832, 140.5594404, 148.9510488, 157.3426572, 165.7342656, 174.125874, 182.5174824, 190.9090908, 199.3006992, 207.6923076, 216.083916, 224.4755244, 232.8671328, 241.2587412, 249.6503496, 258.041958, 266.4335664, 274.8251748, 283.2167832, 291.6083916, 300, 308.3916084, 316.7832168, 325.1748252, 333.5664336, 341.958042, 350.3496503, 358.7412587, 367.1328671, 375.5244755, 383.9160839, 392.3076923, 400.6993007, 409.0909091, 417.4825175, 425.8741259, 434.2657343, 442.6573427, 451.048951, 459.4405594, 467.8321678, 476.2237762, 484.6153846, 493.006993, 501.3986014, 509.7902098, 518.1818182, 526.5734266, 534.965035, 543.3566434, 551.7482517, 560.1398601, 568.5314685, 576.9230769, 585.3146853, 593.7062937, 602.0979021, 610.4895105, 618.8811189, 627.2727273, 635.6643357, 644.0559441, 652.4475524, 660.8391608, 669.2307692, 677.6223776, 686.013986, 694.4055944, 702.7972028, 711.1888112, 719.5804196, 727.972028, 736.3636364, 744.7552448, 753.1468531, 761.5384615, 769.9300699, 778.3216783, 786.7132867, 795.1048951, 803.4965035, 811.8881119, 820.2797203, 828.6713287, 837.0629371, 845.4545455, 853.8461538, 862.2377622, 870.6293706, 879.020979, 887.4125874, 895.8041958, 904.1958042, 912.5874126, 920.979021, 929.3706294, 937.7622378, 946.1538462, 954.5454545, 962.9370629, 971.3286713, 979.7202797, 988.1118881, 996.5034965, 1004.895105, 1013.286713, 1021.678322, 1030.06993, 1038.461538, 1046.853147, 1055.244755, 1063.636364, 1072.027972, 1080.41958, 1088.811189, 1097.202797, 1105.594406, 1113.986014, 1122.377622, 1130.769231, 1139.160839, 1147.552448, 1155.944056, 1164.335664, 1172.727273, 1181.118881, 1189.51049, 1197.902098, 1206.293706, 1214.685315, 1223.076923, 1231.468531, 1239.86014, 1248.251748, 1256.643357, 1265.034965, 1273.426573, 1281.818182, 1290.20979, 1298.601399, 1306.993007, 1315.384615, 1323.776224, 1332.167832, 1340.559441, 1348.951049, 1357.342657, 1365.734266, 1374.125874, 1382.517483, 1390.909091, 1399.300699, 1407.692308, 1416.083916, 1424.475524, 1432.867133, 1441.258741, 1449.65035, 1458.041958, 1466.433566, 1474.825175, 1483.216783, 1491.608392, 1500]
		self.railMesh = None
		self.sleeperMesh = None
		self.USPMesh = None
		self.padMesh = None
		self.Emat1 = None
		self.Emat2 = None
		self.tanDmat1 = None
		self.tanDmat2 = None
		self.Ebal = None
		self.tanDbal = None
		self.EUSP = None
		self.tanDUSP = None
		self.selectedSubst = None
		self.acousticMesh = None
		self.simuParentFolder = None
		
	def DisplaySimu(self): #called when the index of list_simu is changed
		dictSimu = self.SelectedSimu()
		if dictSimu == None:
			return
			
		# mod.DisplaySimu(self, simu)
		
		self.txt_simuName.setText(dictSimu['name'])
		self.simuParentFolder = dictSimu['simuParentFolder']
		self.cb_debugPh2.setChecked(dictSimu['debugPh2'])
		self.cb_writeMED.setChecked(dictSimu['writeMED'])
		self.txt_nJobs.setText(str(dictSimu['nJobs']))
		self.txt_nCPUs.setText(str(dictSimu['nCPUs']))
		self.txt_host.setText(dictSimu['host'])
		self.txt_repTrav.setText(dictSimu['reptrav'])
		self.txt_memLimit.setText(str(dictSimu['memLimit']))
		
		self.cb_phase1.setChecked(dictSimu['computeModes'])

		if dictSimu['computeModes'] == True:

			modesName = os.path.basename(dictSimu['modesFolder'])
			self.txt_phase1Name.setText(modesName)
			modesParentFolder = os.path.dirname(dictSimu['modesFolder'])
			self.modesParentFolder = modesParentFolder

			self.txt_phase1FreqMax.setText(str(dictSimu['modesMaxFreq']))
			self.txt_phase1freq.setText(str(dictSimu['phase1Freq']))
			self.cb_debugPh1.setChecked(dictSimu['debugPh1'])
			self.txt_phase1CPUs.setText(str(dictSimu['phase1CPUs']))
			# default values must be shown if computeModes is turned off, instead of previous simu values
			
		else:
			self.modesFolder = dictSimu['modesFolder']
		
		self.railMesh = dictSimu['railMesh']
		self.txt_ERail.setText(str(dictSimu['ERail']))
		self.txt_nuRail.setText(str(dictSimu['nuRail']))
		self.txt_tanDRail.setText(str(dictSimu['tanDRail']))
		self.txt_rhoRail.setText(str(dictSimu['rhoRail']))

		self.sleeperMesh = dictSimu['sleeperMesh']
		self.txt_E1Sleeper.setText(str(dictSimu['E1Sleeper']))
		self.txt_E2Sleeper.setText(str(dictSimu['E2Sleeper']))
		self.txt_E3Sleeper.setText(str(dictSimu['E3Sleeper']))
		self.txt_nuSleeper.setText(str(dictSimu['nuSleeper']))
		self.txt_tanDSleeper.setText(str(dictSimu['tanDSleeper']))
		self.txt_rhoSleeper.setText(str(dictSimu['rhoSleeper']))

		self.padMesh = dictSimu['padMesh']
		self.Emat1 = dictSimu['Emat1']
		self.Emat2 = dictSimu['Emat2']
		self.tanDmat1 = dictSimu['tanDmat1']
		self.tanDmat2 = dictSimu['tanDmat2']
		self.Ebal = dictSimu['Ebal']
		self.tanDbal = dictSimu['tanDbal']
		self.txt_nuMat1.setText(str(dictSimu['nuMat1']))
		self.txt_nuMat2.setText(str(dictSimu['nuMat2']))
		self.txt_nuBal.setText(str(dictSimu['nuBal']))
		self.txt_hBal.setText(str(dictSimu['hBal']))
		self.txt_balAreaCoef.setText(str(dictSimu['balAreaCoef']))
		self.cb_USP.setChecked(dictSimu['USP_on'])
		if dictSimu['USP_on']:
			self.txt_nuUSP.setText(str(dictSimu['nuUSP']))
			self.txt_thkUSP.setText(str(dictSimu['thkUSP']))
			self.USPMesh = dictSimu['USPMesh']
			self.EUSP = dictSimu['EUSP']
			self.tanDUSP = dictSimu['tanDUSP']
		else: # idem
			self.EUSP = None
			self.tanDUSP = None

		self.txt_stiffX.setText(str(dictSimu['clampStiffX']))
		self.txt_stiffY.setText(str(dictSimu['clampStiffY']))
		self.txt_stiffZ.setText(str(dictSimu['clampStiffZ']))
		self.txt_dampX.setText(str(dictSimu['clampDampX']))
		self.txt_dampY.setText(str(dictSimu['clampDampY']))
		self.txt_dampZ.setText(str(dictSimu['clampDampZ']))

		self.txt_nModesRai.setText(str(dictSimu['nModesRai']))
		self.txt_nModesSlp.setText(str(dictSimu['nModesSlp']))
		self.txt_slpSpacing.setText(str(dictSimu['slpSpacing']))
		self.txt_nSlp.setText(str(dictSimu['nSlp']))
		self.rb_10pct.setChecked(dictSimu['force'] == (0, -100000.0, 10000.0))
		self.rb_45deg.setChecked(dictSimu['force'] == (0, -100000, -100000))
		self.txt_forceNode.setText(dictSimu['forceNode'])
		self.txt_slpForce.setText(str(dictSimu['slpForce']))
		self.frequencies = dictSimu['frequencies']
		
		if dictSimu['outputType'] == 'VITE':
			self.cbb_output.setCurrentText('Velocity')
		elif dictSimu['outputType'] == 'ACCE':
			self.cbb_output.setCurrentText('Acceleration')
		elif dictSimu['outputType'] == 'DEPL':
			self.cbb_output.setCurrentText('Displacement')

		self.selectedSubst = dictSimu['selectedSubstFRF']
		self.cb_computeAcoustic.setChecked(dictSimu['computeAcoustic'])
		self.rb_1D.setChecked(dictSimu['acMeshDim'] == '1D')
		self.rb_2D.setChecked(dictSimu['acMeshDim'] == '2D')
		if dictSimu['computeAcoustic'] == True:
			self.acousticMesh = dictSimu['acousticMesh']
		else:
			self.acousticMesh = None
		
		
	def Phase1StateChanged(self):
		computePhase1 = self.cb_phase1.isChecked()
		self.btn_selPhase1Folder.setDisabled(computePhase1)
		self.label_19.setDisabled(not computePhase1)
		self.label_10.setDisabled(not computePhase1)
		self.label_11.setDisabled(not computePhase1)
		self.label_13.setDisabled(not computePhase1)
		self.label_26.setDisabled(not computePhase1)
		self.btn_savePhase1To.setDisabled(not computePhase1)
		self.txt_phase1Name.setDisabled(not computePhase1)
		self.txt_phase1FreqMax.setDisabled(not computePhase1)
		self.txt_phase1freq.setDisabled(not computePhase1)
		self.txt_phase1CPUs.setDisabled(not computePhase1)
		self.cb_debugPh1.setDisabled(not computePhase1)
		
	def USPStateChanged(self):
		USP_on = self.cb_USP.isChecked()
		self.btn_EUSP.setDisabled(not USP_on)
		self.btn_tanDUSP.setDisabled(not USP_on)
		self.txt_nuUSP.setDisabled(not USP_on)
		self.label_18.setDisabled(not USP_on)
		self.btn_USPMesh.setDisabled(not USP_on)
		self.label_35.setDisabled(not USP_on)
		self.txt_thkUSP.setDisabled(not USP_on)
		
	def DefaultNodeStateChanged(self):
		defNodeON = self.cb_defaultNode.isChecked()
		self.txt_forceNode.setDisabled(defNodeON)
		if defNodeON == True:
			if self.rb_10pct.isChecked() == True:
				self.txt_forceNode.setText('nodeF')
			elif self.rb_45deg.isChecked() == True:
				self.txt_forceNode.setText('nodeF')
				
	def LoadDirChanged(self):
		if self.cb_defaultNode.isChecked() == False:
			return
			
		if self.rb_10pct.isChecked() == True:
			txt = 'nodeF'
		elif self.rb_45deg.isChecked() == True:
			txt = 'nodeF'
			
		self.txt_forceNode.setText(txt)
		
	def ComputeAcousticStateChanged(self):
		self.btn_selectAcousticMesh.setDisabled(not self.cb_computeAcoustic.isChecked())
		self.rb_1D.setDisabled(not self.cb_computeAcoustic.isChecked())
		self.rb_2D.setDisabled(not self.cb_computeAcoustic.isChecked())
		
	def AddSimuToList(self):
		dictSimu = {}
		
		dictSimu['cwd'] = self.cwd
		dictSimu['appPath'] = self.appPath
	
		# Execution parameters ===================================================================================
		#=========================================================================================================
		simuName = self.txt_simuName.text()
		
		if len(simuName) == 0 or '/' in simuName or '\\' in simuName or os.sep in simuName:
			QMessageBox.information(self, 'Error', 'Please enter a correct simulation name.', QMessageBox.Ok,)
			return
		
		dictSimu['name'] = simuName
		
		#
		if self.simuParentFolder is None or os.path.exists(self.simuParentFolder) == False:
			QMessageBox.information(self, 'Error', 'Saving directory was not found.', QMessageBox.Ok,)
			return
			
		dictSimu['simuParentFolder'] = self.simuParentFolder
		
		#
		debugPh2 = self.cb_debugPh2.isChecked()
		dictSimu['debugPh2'] = debugPh2

		#
		writeMED = self.cb_writeMED.isChecked()
		dictSimu['writeMED'] = writeMED

		# 
		nJobsMax = multiprocessing.cpu_count()
		
		try:
			nJobs = int(self.txt_nJobs.text())
			if nJobs < 1 or nJobs > 24:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of jobs (1-24).', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct number of jobs.', QMessageBox.Ok,)
			return
			
		dictSimu['nJobs'] = nJobs
		
		#
		try:
			nCPUs = int(self.txt_nCPUs.text())
			if nCPUs < 1:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of CPUs (1-' + str(nJobsMax) + ').', QMessageBox.Ok,)
				return
			if nCPUs*nJobs > nJobsMax:
				QMessageBox.information(self, 'Error', 'The total number of CPUs used (' + str(nCPUs*nJobs) + ') is larger than the number of CPUs available (' + str(nJobsMax) + ')', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct number of CPUs.', QMessageBox.Ok,)
			return
			
		dictSimu['nCPUs'] = nCPUs
			
		#
		host = self.txt_host.text()
		dictSimu['host'] = host
		
		#
		reptrav = self.txt_repTrav.text()
		reptrav = reptrav.replace('/', os.sep)
		reptrav = reptrav.replace('\\', os.sep)
		if os.path.exists(reptrav) == False:
			QMessageBox.information(self, 'Error', 'Please enter a correct working directory (reptrav).', QMessageBox.Ok,)
			return
			
		dictSimu['reptrav'] = reptrav
		
		#
		try:
			memLimit = float(self.txt_memLimit.text())
			if memLimit < 0:
				QMessageBox.information(self, 'Error', 'Please enter a correct memory limit.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct memory limit.', QMessageBox.Ok,)
			return
			
		dictSimu['memLimit'] = memLimit
		
		# Phase 1 (modes) parameters =====================================================================================
		#=========================================================================================================
		computeModes = self.cb_phase1.isChecked()
		dictSimu['computeModes'] = computeModes
		
		if computeModes == True:
		
			dictSimu['phase1WorkingDir'] = os.path.join(dictSimu['simuParentFolder'], dictSimu['name'] + '_modes')
			
			#
			if self.modesParentFolder is None or os.path.exists(self.modesParentFolder) == False:
				QMessageBox.information(self, 'Error', 'Modes saving directory was not found.', QMessageBox.Ok,)
				return
		
			modesName = self.txt_phase1Name.text()
			if len(modesName) == 0:
				QMessageBox.information(self, 'Error', 'Please enter a correct name for the modes simulation.', QMessageBox.Ok,)
				return
			
			if modesName == dictSimu['name'] + '_modes':
				QMessageBox.information(self, 'Error', dictSimu['name'] + '_modes (Phase 1: modes) cannot be used, please choose a different name.', QMessageBox.Ok,)
				return
			
			modesFolder = os.path.join(self.modesParentFolder, modesName)
			try:
				shutil.rmtree(modesFolder)
			except:
				pass
				
			try:
				os.makedirs(modesFolder)
			except:
				QMessageBox.information(self, 'Error', modesFolder + ' could not be created', QMessageBox.Ok,)
				return
			
			dictSimu['modesFolder'] = modesFolder
			

			#
			debugPh1 = self.cb_debugPh1.isChecked()
			dictSimu['debugPh1'] = debugPh1

			
			#
			try:
				modesMaxFreq = float(self.txt_phase1FreqMax.text())
				if modesMaxFreq < 1.0:
					QMessageBox.information(self, 'Error', 'Please enter a correct max frequency for modes computing.', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter a correct max frequency for modes computing.', QMessageBox.Ok,)
				return
				
			dictSimu['modesMaxFreq'] = modesMaxFreq

			#
			try:
				phase1Freq = float(self.txt_phase1freq.text())
				if phase1Freq < 0:
					QMessageBox.information(self, 'Error', 'Please enter a correct frequency for frequency-dependent materials.', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter a correct frequency for frequency-dependent materials.', QMessageBox.Ok,)
				return
				
			dictSimu['phase1Freq'] = phase1Freq
				
			#
			try:
				phase1CPUs = int(self.txt_phase1CPUs.text())
				if phase1CPUs < 1:
					QMessageBox.information(self, 'Error', 'Please enter a correct number of CPUs.', QMessageBox.Ok,)
					return
				if phase1CPUs > nJobsMax:
					QMessageBox.information(self, 'Error', 'The total number of CPUs used for modes computing is larger than the number of CPUs available (' + str(nJobsMax) + ').', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of CPUs.', QMessageBox.Ok,)
				return
				
			dictSimu['phase1CPUs'] = phase1CPUs

		else:
			#
			if self.modesFolder is None or os.path.exists(self.modesFolder) == False:
				QMessageBox.information(self, 'Error', 'Modes directory was not found.', QMessageBox.Ok,)
				return
			
			dictSimu['modesFolder'] = self.modesFolder

			dictSimu['phase1WorkingDir'] = None
			dictSimu['debugPh1'] = None
			dictSimu['modesMaxFreq'] = None				
			dictSimu['phase1CPUs'] = None
			dictSimu['phase1Freq'] = None
				
				
		# Materials ==============================================================================================
		#=========================================================================================================
		try:
			ERail = float(self.txt_ERail.text())
			nuRail = float(self.txt_nuRail.text())
			tanDRail = float(self.txt_tanDRail.text())
			rhoRail = float(self.txt_rhoRail.text())
			if ERail <= 0 or nuRail >= 0.5 or nuRail < 0 or tanDRail < 0 or rhoRail < 0:
				QMessageBox.information(self, 'Error', 'Please enter correct rails materials properties.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter correct rails materials properties.', QMessageBox.Ok,)
			return
			
		dictSimu['ERail'] = ERail
		dictSimu['nuRail'] = nuRail
		dictSimu['tanDRail'] = tanDRail
		dictSimu['rhoRail'] = rhoRail

		#
		if self.railMesh is None or os.path.exists(self.railMesh) == False:
			QMessageBox.information(self, 'Error', 'Rail mesh not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['railMesh'] = self.railMesh

		#
		if self.sleeperMesh is None or os.path.exists(self.sleeperMesh) == False:
			QMessageBox.information(self, 'Error', 'Sleeper mesh not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['sleeperMesh'] = self.sleeperMesh

		#
		if self.padMesh is None or os.path.exists(self.padMesh) == False:
			QMessageBox.information(self, 'Error', 'Pad mesh not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['padMesh'] = self.padMesh
		
		#
		if self.Emat1 is None or os.path.exists(self.Emat1) == False:
			QMessageBox.information(self, 'Error', 'Pad material 1 Young''s modulus not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['Emat1'] = self.Emat1
		
		#
		if self.Emat2 is None or os.path.exists(self.Emat2) == False:
			QMessageBox.information(self, 'Error', 'Pad material 2 Young''s modulus not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['Emat2'] = self.Emat2
		
		#
		if self.tanDmat1 is None or os.path.exists(self.tanDmat1) == False:
			QMessageBox.information(self, 'Error', 'Pad material 1 damping not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['tanDmat1'] = self.tanDmat1
		
		#
		if self.tanDmat2 is None or os.path.exists(self.tanDmat2) == False:
			QMessageBox.information(self, 'Error', 'Pad material 2 damping not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['tanDmat2'] = self.tanDmat2
		
		#
		try:
			E1Sleeper = float(self.txt_E1Sleeper.text())
			E2Sleeper = float(self.txt_E2Sleeper.text())
			E3Sleeper = float(self.txt_E3Sleeper.text())
			nuSleeper = float(self.txt_nuSleeper.text())
			tanDSleeper = float(self.txt_tanDSleeper.text())
			rhoSleeper = float(self.txt_rhoSleeper.text())
			if E1Sleeper <= 0 or E2Sleeper <= 0 or E3Sleeper <= 0 or nuSleeper >= 0.5 or nuSleeper < 0 or tanDSleeper < 0 or rhoSleeper < 0:
				QMessageBox.information(self, 'Error', 'Please enter correct sleepers materials properties.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter correct sleepers materials properties.', QMessageBox.Ok,)
			return
			
		dictSimu['E1Sleeper'] = E1Sleeper
		dictSimu['E2Sleeper'] = E2Sleeper
		dictSimu['E3Sleeper'] = E3Sleeper
		dictSimu['nuSleeper'] = nuSleeper
		dictSimu['tanDSleeper'] = tanDSleeper
		dictSimu['rhoSleeper'] = rhoSleeper

		#
		try:
			stiffX = float(self.txt_stiffX.text())
			stiffY = float(self.txt_stiffY.text())
			stiffZ = float(self.txt_stiffZ.text())
			dampX = float(self.txt_dampX.text())
			dampY = float(self.txt_dampY.text())
			dampZ = float(self.txt_dampZ.text())
			if stiffX < 0 or stiffY < 0 or stiffZ < 0 or dampX < 0 or dampY < 0 or dampZ < 0:
				QMessageBox.information(self, 'Error', 'Please enter correct clamps properties.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter correct clamps properties.', QMessageBox.Ok,)
			return
			
		dictSimu['clampStiffX'] = stiffX
		dictSimu['clampStiffY'] = stiffY
		dictSimu['clampStiffZ'] = stiffZ
		dictSimu['clampDampX'] = dampX
		dictSimu['clampDampY'] = dampY
		dictSimu['clampDampZ'] = dampZ


		#
		if self.Ebal is None or os.path.exists(self.Ebal) == False:
			QMessageBox.information(self, 'Error', 'Ballast Young''s modulus not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['Ebal'] = self.Ebal
		
		#
		if self.tanDbal is None or os.path.exists(self.tanDbal) == False:
			QMessageBox.information(self, 'Error', 'Ballast damping not defined.', QMessageBox.Ok,)
			return
			
		dictSimu['tanDbal'] = self.tanDbal
		
		#
		try:
			nuMat1 = float(self.txt_nuMat1.text())
			nuMat2 = float(self.txt_nuMat2.text())
			nuBal = float(self.txt_nuBal.text())
			if nuMat1 < 0 or nuMat1 >= 0.5 or nuMat2 < 0 or nuMat2 >= 0.5 or nuBal < 0 or nuBal >= 0.5:
				QMessageBox.information(self, 'Error', 'Please enter correct Poisson''s ratios.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter correct Poisson''s ratios.', QMessageBox.Ok,)
			return
			
		dictSimu['nuMat1'] = nuMat1
		dictSimu['nuMat2'] = nuMat2
		dictSimu['nuBal'] = nuBal
		
		#
		try:
			hBal = float(self.txt_hBal.text())
			if hBal < 0:
				QMessageBox.information(self, 'Error', 'Please enter a correct ballast height.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct ballast height.', QMessageBox.Ok,)
			return
			
		dictSimu['hBal'] = hBal
			
		#
		try:
			balAreaCoef = float(self.txt_balAreaCoef.text())
			if balAreaCoef < 0:
				QMessageBox.information(self, 'Error', 'Please enter a correct ballast area coefficient.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct ballast area coefficient.', QMessageBox.Ok,)
			return
			
		dictSimu['balAreaCoef'] = balAreaCoef
			
		#
		USP_on = self.cb_USP.isChecked()
		dictSimu['USP_on'] = USP_on
		
		if USP_on:
			#
			if self.USPMesh is None or os.path.exists(self.USPMesh) == False:
				QMessageBox.information(self, 'Error', 'USP mesh not defined.', QMessageBox.Ok,)
				return
				
			dictSimu['USPMesh'] = self.USPMesh

			#
			try:
				nuUSP = float(self.txt_nuUSP.text())
				thkUSP = float(self.txt_thkUSP.text())
				if nuUSP < 0 or nuUSP >= 0.5 or thkUSP < 0:
					QMessageBox.information(self, 'Error', 'Please enter correct USPs properties.', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter correct USPs properties.', QMessageBox.Ok,)
				return
				
			dictSimu['nuUSP'] = nuUSP
			dictSimu['thkUSP'] = thkUSP
			
			#
			if self.EUSP is None or os.path.exists(self.EUSP) == False:
				QMessageBox.information(self, 'Error', 'USP Young''s modulus not defined.', QMessageBox.Ok,)
				return
				
			dictSimu['EUSP'] = self.EUSP
			
			#
			if self.tanDUSP is None or os.path.exists(self.tanDUSP) == False:
				QMessageBox.information(self, 'Error', 'USP damping not defined.', QMessageBox.Ok,)
				return
				
			dictSimu['tanDUSP'] = self.tanDUSP



		else:
			dictSimu['USPMesh'] = None
			dictSimu['nuUSP'] = None
			dictSimu['thkUSP'] = None
			dictSimu['EUSP'] = None
			dictSimu['tanDUSP'] = None


			
		# Simulation parameters ==================================================================================
		#=========================================================================================================
		try:
			nModesRai = int(float(self.txt_nModesRai.text()))
			if nModesRai < 1:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of interface modes.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct number of interface modes.', QMessageBox.Ok,)
			return
			
		dictSimu['nModesRai'] = nModesRai

		#
		try:
			nModesSlp = int(float(self.txt_nModesSlp.text()))
			if nModesSlp < 1:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of interface modes.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct number of interface modes.', QMessageBox.Ok,)
			return
			
		dictSimu['nModesSlp'] = nModesSlp

		#
		try:
			cumulMassEffeUn = float(self.txt_cumulMassEffeUn.text())
			if cumulMassEffeUn < 0 or cumulMassEffeUn > 1:
				QMessageBox.information(self, 'Error', 'Please enter a correct total effective unit mass.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct total effective unit mass.', QMessageBox.Ok,)
			return
			
		dictSimu['cumulMassEffeUn'] = cumulMassEffeUn
		
		#
		try:
			nSlp = int(self.txt_nSlp.text())
			if nSlp < 1:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of sleepers.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct number of sleepers.', QMessageBox.Ok,)
			return
			
		dictSimu['nSlp'] = nSlp

		#
		try:
			slpSpacing = float(self.txt_slpSpacing.text())
			if slpSpacing < 0:
				QMessageBox.information(self, 'Error', 'Please enter a correct sleeper spacing.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct sleeper spacing.', QMessageBox.Ok,)
			return
			
		dictSimu['slpSpacing'] = slpSpacing
		
		#
		if self.rb_10pct.isChecked() == True:
			force = (0, -100000.0, 10000.0)
		elif self.rb_45deg.isChecked() == True:
			force = (0, -100000, -100000)
			
		dictSimu['force'] = force
		
		#
		forceNode = self.txt_forceNode.text()
		if len(forceNode) < 1:
			QMessageBox.information(self, 'Error', 'Please enter a correct node group for load application.', QMessageBox.Ok,)
			return
			
		dictSimu['forceNode'] = forceNode
		
		#
		try:
			slpForce = int(self.txt_slpForce.text())
			if slpForce < 1 or slpForce > dictSimu['nSlp']:
				QMessageBox.information(self, 'Error', 'The load must be applied to an existing substructure (sleeper).', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'The load must be applied to an existing substructure (sleeper).', QMessageBox.Ok,)
			return
			
		dictSimu['slpForce'] = slpForce
		
		#
		dictSimu['frequencies'] = self.frequencies
		if len(dictSimu['frequencies']) < dictSimu['nJobs']:
			QMessageBox.information(self, 'Error', 'The number of frequenciesis smaller than the number of jobs (=' + str(dictSimu['nJobs']) + ').', QMessageBox.Ok,)
			return
		
		# Post-processing ========================================================================================
		#=========================================================================================================
		outputType = self.cbb_output.currentText()
		
		if outputType == 'Acceleration':
			dictSimu['outputType'] = 'ACCE'
		elif outputType == 'Velocity':
			dictSimu['outputType'] = 'VITE'
		elif outputType == 'Displacement':
			dictSimu['outputType'] = 'DEPL'
		
		#
		if self.selectedSubst == None or len(self.selectedSubst) == 0:
			QMessageBox.information(self, 'Error', 'Please select at least one substructure to extract FRFs from.', QMessageBox.Ok,)
			return
			
		tmp = []
		for subst in self.selectedSubst:
			if subst <= dictSimu['nSlp']:
				tmp.append(subst)
		
		self.selectedSubst = tmp
		dictSimu['selectedSubstFRF'] = self.selectedSubst

		#
		try:
			nSlpAcoustic = int(self.txt_nSlpAcoustic.text())
			if nSlpAcoustic < -1:
				QMessageBox.information(self, 'Error', 'Wrong number of sleepers for MED / acoustic calculation.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Wrong number of sleepers for MED / acoustic calculation.', QMessageBox.Ok,)
			return
		
		dictSimu['nSlpAcoustic'] = nSlpAcoustic
		
		#
		computeAcoustic = self.cb_computeAcoustic.isChecked()
		dictSimu['computeAcoustic'] = computeAcoustic
		
		#
		if self.rb_1D.isChecked() == True:
			acMeshDim = '1D'
		elif self.rb_2D.isChecked() == True:
			acMeshDim = '2D'
			
		dictSimu['acMeshDim'] = acMeshDim
		
		#
		if computeAcoustic == True:
			if (self.acousticMesh is None or os.path.exists(self.acousticMesh) == False):
				QMessageBox.information(self, 'Error', 'Acoustic mesh not defined.', QMessageBox.Ok,)
				return
			
			dictSimu['acousticMesh'] = self.acousticMesh
		else:
			dictSimu['acousticMesh'] = None
	
		#
		try:
			txt = json.dumps(dictSimu, indent = 4, sort_keys=True)
			jsonPath = os.path.join(self.cwd, dictSimu['name'] + '.json')
			with open(jsonPath, 'w') as f:
				f.write(txt)
			f.close()
		except:
			return jsonPath + ' could not be created.'



		self.simuList.append(dictSimu)
		newListItem = QListWidgetItem(simuName)
		self.list_simu.addItem(newListItem)
		self.list_simu.setCurrentRow(self.list_simu.count()-1)
		
	def SelectSimuDir(self):
		if self.simuParentFolder is None or os.path.exists(self.simuParentFolder) == False:
			path = self.cwd
		else:
			path = self.simuParentFolder
		
		folder = str(QFileDialog.getExistingDirectory(self, "Select directory", path))									 
		if folder == '':
			return
			
		self.simuParentFolder = folder
		
	def SelectModesFolder(self):
		# Used if already computed modes are reused
		if self.modesFolder is None or os.path.exists(self.modesFolder) == False:
			path = self.cwd
		else:
			path = self.modesFolder
		
		folder = str(QFileDialog.getExistingDirectory(self, "Select modes folder", path))
		if folder == '':
			return
			
		self.modesFolder = folder
		
	def SelectModesParentFolder(self):
		# Used if modes are recomputed
		if self.modesParentFolder is None or os.path.exists(self.modesParentFolder) == False:
			path = self.cwd
		else:
			path = self.modesParentFolder
		
		folder = str(QFileDialog.getExistingDirectory(self, "Select directory where the modes folder will be saved", path))									 
		if folder == '':
			return
			
		self.modesParentFolder = folder
		
		
	def SelectFrequencies(self):
		dlg_frequencies = Dialog_Frequencies(self.frequencies, 'Spectrum definition (Hz)')
		dlg_frequencies.show()
		dlg_frequencies.exec_()
		self.frequencies = dlg_frequencies.frequencies
		
	def SelectRailMesh(self):
		defPath = os.path.join(self.cwd, 'Meshes', 'Rails')
		self.railMesh = self.SelectFile('Select rail mesh', self.railMesh, defPath, '*.med')

	def SelectSleeperMesh(self):
		defPath = os.path.join(self.cwd, 'Meshes', 'Sleepers')
		self.sleeperMesh = self.SelectFile('Select sleeper mesh', self.sleeperMesh, defPath, '*.med')

	def SelectUSPMesh(self):
		defPath = os.path.join(self.cwd, 'Meshes', 'USPs')
		self.USPMesh = self.SelectFile('Select USP mesh', self.USPMesh, defPath, '*.med')

	def SelectPadMesh(self):
		defPath = os.path.join(self.cwd, 'Meshes', 'RailPads')
		self.padMesh = self.SelectFile('Select rail pad mesh', self.padMesh, defPath, '*.med')

	def SelectEmat1(self):
		defPath = os.path.join(self.cwd, 'MaterialsProperties')
		self.Emat1 = self.SelectFile('Select material 1 Young''s modulus', self.Emat1, defPath, '*.csv *.txt')
		
	def SelectEmat2(self):
		defPath = os.path.join(self.cwd, 'MaterialsProperties')
		self.Emat2 = self.SelectFile('Select material 2 Young''s modulus', self.Emat2, defPath, '*.csv *.txt')
		
	def SelectTanDmat1(self):
		defPath = os.path.join(self.cwd, 'MaterialsProperties')
		self.tanDmat1 = self.SelectFile('Select material 1 damping', self.tanDmat1, defPath, '*.csv *.txt')
		
	def SelectTanDmat2(self):
		defPath = os.path.join(self.cwd, 'MaterialsProperties')
		self.tanDmat2 = self.SelectFile('Select material 2 damping', self.tanDmat2, defPath, '*.csv *.txt')
		
	def SelectEbal(self):
		defPath = os.path.join(self.cwd, 'MaterialsProperties')
		self.Ebal = self.SelectFile('Select ballast Young''s modulus', self.Ebal, defPath, '*.csv *.txt')
		
	def SelectTanDbal(self):
		defPath = os.path.join(self.cwd, 'MaterialsProperties')
		self.tanDbal = self.SelectFile('Select ballast damping', self.tanDbal, defPath, '*.csv *.txt')
		
	def SelectEUSP(self):
		defPath = os.path.join(self.cwd, 'MaterialsProperties')
		self.EUSP = self.SelectFile('Select USP Young''s modulus', self.EUSP, defPath, '*.csv *.txt')
		
	def SelectTanDUSP(self):
		defPath = os.path.join(self.cwd, 'MaterialsProperties')
		self.tanDUSP = self.SelectFile('Select USP damping', self.tanDUSP, defPath, '*.csv *.txt')
		
	def SelectAcousticMesh(self):
		defPath = os.path.join(self.cwd, 'Meshes', 'AcousticMeshes')
		self.acousticMesh = self.SelectFile('Select acoustic mesh', self.acousticMesh, defPath, '*.med')
		
	def SelectFile(self, p_title, p_file, p_defaultPath, p_ext):
		if p_file == None or os.path.exists(p_file) == False:
			path = p_defaultPath
		else:
			path = p_file
		
		if os.path.exists(path) == False:
			path = self.cwd

		if os.path.exists(path) == False:
			path = self.appPath
			
		file = QFileDialog.getOpenFileName(self, p_title, path, p_ext)
		
		if file[0] == '':
			return path
		
		return file[0]
		
	def SelectSubstructures(self):
		try:
			nSlp = int(self.txt_nSlp.text())
			if nSlp < 1:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of sleepers.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct number of sleepers.', QMessageBox.Ok,)
			return

		dlg_subst = Dialog_Substructures(nSlp, self.selectedSubst)
		dlg_subst.show()
		dlg_subst.exec_()
		
		self.selectedSubst = dlg_subst.substructures
		
	def SimulateAll(self):
	
		n = self.list_simu.count()
		if n == 0:
			return
		
		simulationsOrdered = []
		for i in range(n):
			item = self.list_simu.item(i)
			txt = item.text()
			for simu in self.simuList:
				if simu['name'] == txt:
					simulationsOrdered.append(simu)
					break
	
	
	
		for simu in simulationsOrdered:
			code = mod.RunSimulation(simu)
			if code != 0:
				if isinstance(code, str) or isinstance(code, unicode):
					print(simu['name'] + " did not run properly. The error message is:\n" + code)
				elif isinstance(code, int):
					print(simu['name'] + " did not run properly. Check out Code_Aster message files. Exit code: " + str(code))
				else:
					print("Unknown error; exit code: " + str(code))
					
			mod.DeletePycFiles(self.appPath)
				
	def DeleteSimu(self):
		# if self.running == True:
			# return
			
		simu = self.SelectedSimu()
		if simu == None:
			return
			
		self.simuList.remove(simu)
			
		item = self.list_simu.currentItem()
		self.list_simu.takeItem(self.list_simu.row(item))
		if len(self.simuList) == 0:
			self.DisplaySimu()
		
	
	def MoveSimuUp(self):
		# if self.running == True:
			# return
			
		i = self.list_simu.currentRow()
		if i == 0 or self.list_simu.count() == 0:
			return
			
		item = self.list_simu.item(i)
		self.list_simu.takeItem(i)
		self.list_simu.insertItem(i-1, item)
		self.list_simu.setCurrentRow(i-1)
		
	def MoveSimuDown(self):
		# if self.running == True:
			# return
			
		i = self.list_simu.currentRow()
		n = self.list_simu.count()
		if n == 0 or i == n-1:
			return
			
		item = self.list_simu.item(i)
		self.list_simu.takeItem(i)
		self.list_simu.insertItem(i+1, item)
		self.list_simu.setCurrentRow(i+1)

	def SelectedSimu(self):
		item = self.list_simu.currentItem()
		
		if item == None:
			return None
			
		name = item.text()
		
		for i in range(len(self.simuList)):
			simu = self.simuList[i]
			if simu['name'] == name:
				return simu
				
		return None
			
	def closeEvent(self, event):
		self.closeApp()
		
	def closeApp(self):
		mod.DeletePycFiles(self.appPath)
		self.close()


class Dialog_Frequencies(QDialog):
	def __init__(self, p_currentFreqs, p_title):
		super(QDialog, self).__init__()
		self.setWindowTitle(p_title)
		self.resize(340, 500)
		self.setModal(True)
		
		mainlayout = QVBoxLayout()
		self.table = Table(p_currentFreqs)
		self.btn_OK = QPushButton('OK')
		self.btn_Cancel = QPushButton('Cancel')
		self.btn_Add = QPushButton('+')
		mainlayout.addWidget(self.table)
		mainlayout.addWidget(self.btn_OK)
		mainlayout.addWidget(self.btn_Cancel)
		mainlayout.addWidget(self.btn_Add)
		self.setLayout(mainlayout)
		
		self.btn_Cancel.clicked.connect(self.close)
		self.btn_OK.clicked.connect(self.OK)
		self.btn_Add.clicked.connect(self.Add)
		
		self.frequencies = p_currentFreqs
		
	def OK(self):
		freqs = []
		for i in range(self.table.rowCount()):
			item = self.table.item(i, 0)
			try:
				freq = float(item.text())
				freqs.append(freq)
			except:
				continue
		
		if freqs:
			freqs = list(dict.fromkeys(freqs))
			self.frequencies = sorted(freqs)
			self.close()
		else:
			QMessageBox.information(self, 'Error', 'No frequency selected.', QMessageBox.Ok,)
			return
			
	def Add(self):
		r = self.table.currentRow()
		self.table.insertRow(r+1)
		item = QTableWidgetItem('')
		item.setToolTip(self.table.tooltip)
		self.table.setItem(r+1,0, item)
		# self.table.setRowCount(self.table.rowCount() + 1)
		
		# for i in range(r+1, self.table.rowCount() - 1):
			# item = self.table.item(i, 0)
			# self.table.setItem(i+1,0, item)
		
		# item = QTableWidgetItem('')
		# item.setToolTip(self.table.tooltip)
		# self.table.setItem(r+1,0, item)
			
class Dialog_Substructures(QDialog):
	def __init__(self, p_nSlp, p_currentSubsOutput):
		super(QDialog, self).__init__()
		self.setWindowTitle('Substructures selection')
		self.resize(340, 500)
		self.setModal(True)
		self.substructures = p_currentSubsOutput
		
		mainlayout = QVBoxLayout()
		scroll = QScrollArea()				# Scroll Area which contains the widgets, set as the centralWidget
		widget = QWidget()					# Widget that contains the collection of Vertical Box
		vbox = QVBoxLayout()	
		lbl = QLabel('Select substructures to extract FRF from')
		mainlayout.addWidget(lbl)
		
		
		self.checkBoxes = []
		for i in range(1, p_nSlp + 1):
			cb = QCheckBox('Substructure ' + str(i))
			if p_currentSubsOutput is not None and i in p_currentSubsOutput:
				cb.setChecked(True)
			
			self.checkBoxes.append(cb)
			vbox.addWidget(cb)
			
		widget.setLayout(vbox)
		scroll.setWidget(widget)
		mainlayout.addWidget(scroll)
		
		#Scroll Area Properties
		scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		# scroll.setWidgetResizable(True)
		
		# Add buttons
		self.btn_OK = QPushButton('OK')
		self.btn_Cancel = QPushButton('Cancel')
		mainlayout.addWidget(self.btn_OK)
		mainlayout.addWidget(self.btn_Cancel)
		self.setLayout(mainlayout)
		
		# Signals and slots
		self.btn_Cancel.clicked.connect(self.close)
		self.btn_OK.clicked.connect(self.OK)
	
	def OK(self):
		newSubst = []
		i = 1
		for cb in self.checkBoxes:
			if cb.isChecked() == True:
				newSubst.append(i)
			i += 1
				
		self.substructures = newSubst
		self.close()

class Table(QTableWidget):
	def __init__(self, p_freqs):
		super(QTableWidget, self).__init__()
		self.setRowCount(len(p_freqs))
		self.setColumnCount(1)
		self.setSortingEnabled(False)
		self.tooltip = 'Enter at least one frequency per job (=frequency band). Multiple cells can be copied/pasted from/to Excel or another table.'
				
		for i in range(len(p_freqs)):
			item = QTableWidgetItem(str(p_freqs[i]))
			item.setToolTip(self.tooltip)
			self.setItem(i,0, item)
		
	def keyPressEvent(self, event):
		super(QTableWidget, self).keyPressEvent(event)
		
		if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
			txt = ''		
			for index in self.selectedIndexes():
				if index.data() is None:
					txt += '\n'
				else:
					txt += index.data() + '\n'
							
			clipboard.copy(txt)
			
		elif event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier):
			r = self.currentRow()
			txt = clipboard.paste()				
			txt = txt.split('\n')
			if txt[-1] == '' and len(txt) > 1:
				txt = txt[0:-1]
			
			if len(txt) + r > self.rowCount():
				self.setRowCount(len(txt) + r)
			
			for i in range(len(txt)):
				item = QTableWidgetItem(txt[i])
				item.setToolTip(self.tooltip)
				self.setItem(i+r,0, item)
				
		elif event.key() == Qt.Key_Delete:
			for item in self.selectedItems():
				item.setText('')



if __name__ == '__main__':
	app = QApplication([])
	widget = MultiSleeperModelGUI()
	widget.show()
	sys.exit(app.exec_())