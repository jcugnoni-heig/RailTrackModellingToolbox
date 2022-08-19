import os
import sys
import module_run as run
import shutil
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer, QObject, QThread, pyqtSignal
import clipboard
import module_run as mod
import json
from datetime import datetime
import multiprocessing


class MultiSleeperModelGUI(QMainWindow):
	def __init__(self):
		super(MultiSleeperModelGUI, self).__init__()
		appPath = os.path.dirname(os.path.realpath(__file__))
		uiFilePath=os.path.join(appPath,'GUI.ui')
		loadUi(uiFilePath,self)
		self.setWindowTitle('Multi-sleeper model')
		
		self.cb_phase1.stateChanged.connect(self.Phase1StateChanged)
		self.btn_selPhase1Folder.clicked.connect(self.SelectPhase1Folder)
		self.btn_phase1SelFreqs.clicked.connect(self.SelectPhase1Frequencies)
		self.btn_padMesh.clicked.connect(self.SelectPadMesh)
		self.btn_Emat1.clicked.connect(self.SelectEmat1)
		self.btn_Emat2.clicked.connect(self.SelectEmat2)
		self.btn_tanDmat1.clicked.connect(self.SelectTanDmat1)
		self.btn_tanDmat2.clicked.connect(self.SelectTanDmat2)
		self.btn_Ebal.clicked.connect(self.SelectEbal)
		self.btn_tanDbal.clicked.connect(self.SelectTanDbal)
		self.btn_EUSP.clicked.connect(self.SelectEUSP)
		self.btn_tanDUSP.clicked.connect(self.SelectTanDUSP)
		self.cb_USP.stateChanged.connect(self.USPStateChanged)
		self.btn_freqs.clicked.connect(self.SelectPhase2Frequencies)
		self.cb_defaultNode.stateChanged.connect(self.DefaultNodeStateChanged)
		self.rb_10pct.toggled.connect(self.LoadDirChanged)
		self.btn_selectSubstructures.clicked.connect(self.SelectSubstructures)
		self.cb_computeAcoustic.stateChanged.connect(self.ComputeAcousticStateChanged)
		self.btn_selectAcousticMesh.clicked.connect(self.SelectAcousticMesh)
		self.btn_addSimu.clicked.connect(self.AddSimuToList)
		self.btn_simuDir.clicked.connect(self.SelectSimuDir)
		self.btn_simulate.clicked.connect(self.SimulateAll)
		self.btn_savePhase1To.clicked.connect(self.SavePhase1To)
		self.actionExit.triggered.connect(self.closeApp)
		self.btn_deleteSimu.clicked.connect(self.DeleteSimu)
		self.btn_moveUp.clicked.connect(self.MoveSimuUp)
		self.btn_moveDown.clicked.connect(self.MoveSimuDown)
		self.list_simu.currentItemChanged.connect(self.DisplaySimu)
				
		self.cwd = appPath
		self.simuList = []
		self.phase1Folder = None
		self.savePhase1To = None
		self.frequenciesPh1 = [300, 308.3916084, 316.7832168, 325.1748252, 333.5664336, 341.958042, 350.3496503, 358.7412587, 367.1328671, 375.5244755, 383.9160839, 392.3076923, 400.6993007, 409.0909091, 417.4825175, 425.8741259, 434.2657343, 442.6573427, 451.048951, 459.4405594, 467.8321678, 476.2237762, 484.6153846, 493.006993, 501.3986014, 509.7902098, 518.1818182, 526.5734266, 534.965035, 543.3566434, 551.7482517, 560.1398601, 568.5314685, 576.9230769, 585.3146853, 593.7062937, 602.0979021, 610.4895105, 618.8811189, 627.2727273, 635.6643357, 644.0559441, 652.4475524, 660.8391608, 669.2307692, 677.6223776, 686.013986, 694.4055944, 702.7972028, 711.1888112, 719.5804196, 727.972028, 736.3636364, 744.7552448, 753.1468531, 761.5384615, 769.9300699, 778.3216783, 786.7132867, 795.1048951, 803.4965035, 811.8881119, 820.2797203, 828.6713287, 837.0629371, 845.4545455, 853.8461538, 862.2377622, 870.6293706, 879.020979, 887.4125874, 895.8041958, 904.1958042, 912.5874126, 920.979021, 929.3706294, 937.7622378, 946.1538462, 954.5454545, 962.9370629, 971.3286713, 979.7202797, 988.1118881, 996.5034965, 1004.895105, 1013.286713, 1021.678322, 1030.06993, 1038.461538, 1046.853147, 1055.244755, 1063.636364, 1072.027972, 1080.41958, 1088.811189, 1097.202797, 1105.594406, 1113.986014, 1122.377622, 1130.769231, 1139.160839, 1147.552448, 1155.944056, 1164.335664, 1172.727273, 1181.118881, 1189.51049, 1197.902098, 1206.293706, 1214.685315, 1223.076923, 1231.468531, 1239.86014, 1248.251748, 1256.643357, 1265.034965, 1273.426573, 1281.818182, 1290.20979, 1298.601399, 1306.993007, 1315.384615, 1323.776224, 1332.167832, 1340.559441, 1348.951049, 1357.342657, 1365.734266, 1374.125874, 1382.517483, 1390.909091, 1399.300699, 1407.692308, 1416.083916, 1424.475524, 1432.867133, 1441.258741, 1449.65035, 1458.041958, 1466.433566, 1474.825175, 1483.216783, 1491.608392, 1500]
		self.frequenciesPh2 = self.frequenciesPh1
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
		self.simuDir = None
		
	def DisplaySimu(self): #called when the index of list_simu is changed
		dictSimu = self.SelectedSimu()
		if dictSimu == None:
			return
			
		# mod.DisplaySimu(self, simu)
		
		self.txt_simuName.setText(dictSimu['name'])
		self.simuDir = dictSimu['simuDir']
		self.txt_nJobs.setText(str(dictSimu['nJobs']))
		self.txt_nCPUs.setText(str(dictSimu['nCPUs']))
		self.txt_host.setText(dictSimu['host'])
		self.txt_repTrav.setText(dictSimu['reptrav'])
		self.txt_memLimit.setText(str(dictSimu['memLimit']))
		
		self.cb_phase1.setChecked(dictSimu['runPhase1'])
		if dictSimu['runPhase1'] == True:
			self.txt_phase1Name.setText(dictSimu['phase1Name'])
			self.txt_phase1FreqMax.setText(str(dictSimu['phase1FreqMax']))
			self.txt_phase1RailModes.setText(str(dictSimu['phase1RailModes']))
			self.txt_phase1SlpModes.setText(str(dictSimu['phase1SlpModes']))
			self.txt_phase1CPUs.setText(str(dictSimu['phase1CPUs']))
			self.frequenciesPh1 = dictSimu['phase1Freqs']
			# default values must be shown if runPhase1 is turned off, instead of previous simu values
			self.phase1Folder = None
		else:
			self.phase1Folder = dictSimu['phase1Folder']
			# default values must be shown if runPhase1 is turned on, instead of previous simu values
			self.frequenciesPh1 = [300, 308.3916084, 316.7832168, 325.1748252, 333.5664336, 341.958042, 350.3496503, 358.7412587, 367.1328671, 375.5244755, 383.9160839, 392.3076923, 400.6993007, 409.0909091, 417.4825175, 425.8741259, 434.2657343, 442.6573427, 451.048951, 459.4405594, 467.8321678, 476.2237762, 484.6153846, 493.006993, 501.3986014, 509.7902098, 518.1818182, 526.5734266, 534.965035, 543.3566434, 551.7482517, 560.1398601, 568.5314685, 576.9230769, 585.3146853, 593.7062937, 602.0979021, 610.4895105, 618.8811189, 627.2727273, 635.6643357, 644.0559441, 652.4475524, 660.8391608, 669.2307692, 677.6223776, 686.013986, 694.4055944, 702.7972028, 711.1888112, 719.5804196, 727.972028, 736.3636364, 744.7552448, 753.1468531, 761.5384615, 769.9300699, 778.3216783, 786.7132867, 795.1048951, 803.4965035, 811.8881119, 820.2797203, 828.6713287, 837.0629371, 845.4545455, 853.8461538, 862.2377622, 870.6293706, 879.020979, 887.4125874, 895.8041958, 904.1958042, 912.5874126, 920.979021, 929.3706294, 937.7622378, 946.1538462, 954.5454545, 962.9370629, 971.3286713, 979.7202797, 988.1118881, 996.5034965, 1004.895105, 1013.286713, 1021.678322, 1030.06993, 1038.461538, 1046.853147, 1055.244755, 1063.636364, 1072.027972, 1080.41958, 1088.811189, 1097.202797, 1105.594406, 1113.986014, 1122.377622, 1130.769231, 1139.160839, 1147.552448, 1155.944056, 1164.335664, 1172.727273, 1181.118881, 1189.51049, 1197.902098, 1206.293706, 1214.685315, 1223.076923, 1231.468531, 1239.86014, 1248.251748, 1256.643357, 1265.034965, 1273.426573, 1281.818182, 1290.20979, 1298.601399, 1306.993007, 1315.384615, 1323.776224, 1332.167832, 1340.559441, 1348.951049, 1357.342657, 1365.734266, 1374.125874, 1382.517483, 1390.909091, 1399.300699, 1407.692308, 1416.083916, 1424.475524, 1432.867133, 1441.258741, 1449.65035, 1458.041958, 1466.433566, 1474.825175, 1483.216783, 1491.608392, 1500]
		
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
		self.cb_USP.setChecked(dictSimu['USPON'])
		if dictSimu['USPON']:
			self.txt_nuUSP.setText(str(dictSimu['nuUSP']))
			self.EUSP = dictSimu['EUSP']
			self.tanDUSP = dictSimu['tanDUSP']
		else: # idem
			self.EUSP = None
			self.tanDUSP = None

		self.txt_nModes.setText(str(dictSimu['nModes']))
		self.txt_nSlp.setText(str(dictSimu['nSlp']))
		self.rb_10pct.setChecked(dictSimu['force'] == (0, -100000.0, 10000.0))
		self.rb_45deg.setChecked(dictSimu['force'] == (0, -100000, -100000))
		self.txt_forceNode.setText(dictSimu['forceNode'])
		self.txt_slpForce.setText(str(dictSimu['slpForce']))
		self.frequenciesPh2 = dictSimu['frequencies']
		
		if dictSimu['outputType'] == 'VITE':
			self.cbb_output.setCurrentText('Velocity')
		elif dictSimu['outputType'] == 'ACCE':
			self.cbb_output.setCurrentText('Acceleration')
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
		self.label_12.setDisabled(not computePhase1)
		self.label_13.setDisabled(not computePhase1)
		self.label_26.setDisabled(not computePhase1)
		self.btn_savePhase1To.setDisabled(not computePhase1)
		self.txt_phase1Name.setDisabled(not computePhase1)
		self.txt_phase1FreqMax.setDisabled(not computePhase1)
		self.txt_phase1RailModes.setDisabled(not computePhase1)
		self.txt_phase1SlpModes.setDisabled(not computePhase1)
		self.txt_phase1CPUs.setDisabled(not computePhase1)
		self.btn_phase1SelFreqs.setDisabled(not computePhase1)
		
	def USPStateChanged(self):
		USPON = self.cb_USP.isChecked()
		self.btn_EUSP.setDisabled(not USPON)
		self.btn_tanDUSP.setDisabled(not USPON)
		self.txt_nuUSP.setDisabled(not USPON)
		self.label_18.setDisabled(not USPON)
		
	def DefaultNodeStateChanged(self):
		defNodeON = self.cb_defaultNode.isChecked()
		self.txt_forceNode.setDisabled(defNodeON)
		if defNodeON == True:
			if self.rb_10pct.isChecked() == True:
				self.txt_forceNode.setText('nForce10')
			elif self.rb_45deg.isChecked() == True:
				self.txt_forceNode.setText('nForce45')
				
	def LoadDirChanged(self):
		if self.cb_defaultNode.isChecked() == False:
			return
			
		if self.rb_10pct.isChecked() == True:
			txt = 'nForce10'
		elif self.rb_45deg.isChecked() == True:
			txt = 'nForce45'
			
		self.txt_forceNode.setText(txt)
		
	def ComputeAcousticStateChanged(self):
		self.btn_selectAcousticMesh.setDisabled(not self.cb_computeAcoustic.isChecked())
		self.rb_1D.setDisabled(not self.cb_computeAcoustic.isChecked())
		self.rb_2D.setDisabled(not self.cb_computeAcoustic.isChecked())
		
	def AddSimuToList(self):
		dictSimu = {}
		
		dictSimu['cwd'] = self.cwd
	
		# Computing parameters ===================================================================================
		#=========================================================================================================
		simuName = self.txt_simuName.text()
		
		if len(simuName) == 0 or '/' in simuName or '\\' in simuName or os.sep in simuName:
			QMessageBox.information(self, 'Error', 'Please enter a correct simulation name.', QMessageBox.Ok,)
			return
		
		dictSimu['name'] = simuName
		
		#
		if self.simuDir is None or os.path.exists(self.simuDir) == False:
			QMessageBox.information(self, 'Error', 'Saving directory was not found.', QMessageBox.Ok,)
			return
			
		dictSimu['simuDir'] = self.simuDir
		
		# 
		nJobsMax = multiprocessing.cpu_count()/2
		
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
		
		# Phase 1 parameters =====================================================================================
		#=========================================================================================================
		runPhase1 = self.cb_phase1.isChecked()
		dictSimu['runPhase1'] = runPhase1
		
		if runPhase1 == True:
		
			dictSimu['phase1WorkingDir'] = os.path.join(dictSimu['simuDir'], dictSimu['name'] + '_phase1')
			dictSimu['nJobsPh1'] = 4
		
			#
			if self.savePhase1To is None or os.path.exists(self.savePhase1To) == False:
				QMessageBox.information(self, 'Error', 'Phase 1 saving directory was not found.', QMessageBox.Ok,)
				return
				
			dictSimu['savePhase1To'] = self.savePhase1To
		
		
			#
			phase1Name = self.txt_phase1Name.text()
			if len(phase1Name) == 0:
				QMessageBox.information(self, 'Error', 'Please enter a correct name for Phase 1.', QMessageBox.Ok,)
				return
				
			dictSimu['phase1Name'] = phase1Name
			
			dir = os.path.join(dictSimu['savePhase1To'], dictSimu['phase1Name'])
			try:
				shutil.rmtree(dir)
			except:
				pass
				
			try:
				os.makedirs(dir)
			except:
				QMessageBox.information(self, 'Error', dir + 'could not be created', QMessageBox.Ok,)
				return
				
			#
			try:
				phase1FreqMax = float(self.txt_phase1FreqMax.text())
				if phase1FreqMax < 1.0:
					QMessageBox.information(self, 'Error', 'Please enter a correct max frequency for Phase 1.', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter a correct max frequency for Phase 1.', QMessageBox.Ok,)
				return
				
			dictSimu['phase1FreqMax'] = phase1FreqMax
				
			#
			try:
				phase1RailModes = int(self.txt_phase1RailModes.text())
				if phase1RailModes < 1:
					QMessageBox.information(self, 'Error', 'Please enter a correct number of modes for Phase 1.', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of modes for Phase 1.', QMessageBox.Ok,)
				return
				
			dictSimu['phase1RailModes'] = phase1RailModes
				
			#
			try:
				phase1SlpModes = int(self.txt_phase1SlpModes.text())
				if phase1SlpModes < 1:
					QMessageBox.information(self, 'Error', 'Please enter a correct number of modes for Phase 1.', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of modes for Phase 1.', QMessageBox.Ok,)
				return
				
			dictSimu['phase1SlpModes'] = phase1SlpModes
				
			#
			try:
				phase1CPUs = int(self.txt_phase1CPUs.text())
				if phase1CPUs < 1:
					QMessageBox.information(self, 'Error', 'Please enter a correct number of CPUs.', QMessageBox.Ok,)
					return
				if phase1CPUs*dictSimu['nJobsPh1'] > nJobsMax:
					QMessageBox.information(self, 'Error', 'Phase 1 will be running using 4 jobs (=frequency bands) simultaneously. The total number of CPUs used for Phase 1 (' + str(phase1CPUs*dictSimu['nJobsPh1']) + ') is larger than the number of CPUs available (' + str(nJobsMax) + '). Please use less CPUs per job.', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of CPUs.', QMessageBox.Ok,)
				return
				
			dictSimu['phase1CPUs'] = phase1CPUs
			
			#
			dictSimu['phase1Freqs'] = self.frequenciesPh1
			
			if len(dictSimu['phase1Freqs']) < dictSimu['nJobsPh1']:
				QMessageBox.information(self, 'Error', 'The number of frequencies (phase1) is smaller than the number of jobs (=' + str(dictSimu['nJobsPh1']) + ').', QMessageBox.Ok,)
				return
			
		else:
			#
			if self.phase1Folder is None or os.path.exists(self.phase1Folder) == False:
				QMessageBox.information(self, 'Error', 'Phase 1 directory was not found.', QMessageBox.Ok,)
				return
				
			dictSimu['phase1Folder'] = self.phase1Folder
				
				
		# Materials ==============================================================================================
		#=========================================================================================================
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
		USPON = self.cb_USP.isChecked()
		dictSimu['USPON'] = USPON
		
		if USPON:
			#
			try:
				nuUSP = float(self.txt_nuUSP.text())
				if nuUSP < 0 or nuUSP >= 0.5:
					QMessageBox.information(self, 'Error', 'Please enter correct Poisson''s ratios.', QMessageBox.Ok,)
					return
			except:
				QMessageBox.information(self, 'Error', 'Please enter correct Poisson''s ratios.', QMessageBox.Ok,)
				return
				
			dictSimu['nuUSP'] = nuUSP
			
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
			
		# Simulation parameters ==================================================================================
		#=========================================================================================================
		try:
			nModes = int(float(self.txt_nModes.text()))
			if nModes < 1:
				QMessageBox.information(self, 'Error', 'Please enter a correct number of modes.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'Please enter a correct number of modes.', QMessageBox.Ok,)
			return
			
		dictSimu['nModes'] = nModes
		
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
				QMessageBox.information(self, 'Error', 'The load must be applied to an existing substructure.', QMessageBox.Ok,)
				return
		except:
			QMessageBox.information(self, 'Error', 'The load must be applied to an existing substructure.', QMessageBox.Ok,)
			return
			
		dictSimu['slpForce'] = slpForce
		
		#
		dictSimu['frequencies'] = self.frequenciesPh2
		if len(dictSimu['frequencies']) < dictSimu['nJobs']:
			QMessageBox.information(self, 'Error', 'The number of frequencies (phase2) is smaller than the number of jobs (=' + str(dictSimu['nJobs']) + ').', QMessageBox.Ok,)
			return
		
		# Post-processing ========================================================================================
		#=========================================================================================================
		outputType = self.cbb_output.currentText()
		
		if outputType == 'Acceleration':
			dictSimu['outputType'] = 'ACCE'
		elif outputType == 'Velocity':
			dictSimu['outputType'] = 'VITE'
		else:
			QMessageBox.information(self, 'Error', 'Wrong output type', QMessageBox.Ok,)
			return
		
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
	
		#
		self.simuList.append(dictSimu)
		newListItem = QListWidgetItem(simuName)
		self.list_simu.addItem(newListItem)
		self.list_simu.setCurrentRow(self.list_simu.count()-1)
		
	def SelectSimuDir(self):
		if self.simuDir is None or os.path.exists(self.simuDir) == False:
			path = self.cwd
		else:
			path = self.simuDir
		
		folder = str(QFileDialog.getExistingDirectory(self, "Select directory", path))									 
		if folder == '':
			return
			
		self.simuDir = folder
		
	def SelectPhase1Folder(self):
		if self.phase1Folder is None or os.path.exists(self.phase1Folder) == False:
			path = self.cwd
		else:
			path = self.phase1Folder
		
		folder = str(QFileDialog.getExistingDirectory(self, "Select base directory", path))
		if folder == '':
			return
			
		self.phase1Folder = folder
		
	def SavePhase1To(self):
		if self.savePhase1To is None or os.path.exists(self.savePhase1To) == False:
			path = self.cwd
		else:
			path = self.savePhase1To
		
		folder = str(QFileDialog.getExistingDirectory(self, "Select directory", path))									 
		if folder == '':
			return
			
		self.savePhase1To = folder
		
	def SelectPhase1Frequencies(self):
		dlg_frequencies = Dialog_Frequencies(self.frequenciesPh1, 'Phase 1 spectrum definition (Hz)')
		dlg_frequencies.show()
		dlg_frequencies.exec_()
		self.frequenciesPh1 = dlg_frequencies.frequencies
		
	def SelectPhase2Frequencies(self):
		dlg_frequencies = Dialog_Frequencies(self.frequenciesPh2, 'Phase 2 spectrum definition (Hz)')
		dlg_frequencies.show()
		dlg_frequencies.exec_()
		self.frequenciesPh2 = dlg_frequencies.frequencies
		
	def SelectPadMesh(self):
		defPath = os.path.join(self.cwd, 'Meshes', 'pads')
		self.padMesh = self.SelectFile('Select pad mesh', self.padMesh, defPath, '*.med')

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
		defPath = os.path.join(self.cwd, 'Meshes', 'acousticMeshes')
		self.acousticMesh = self.SelectFile('Select acoustic mesh', self.acousticMesh, defPath, '*.med')
		
	def SelectFile(self, p_title, p_file, p_defaultPath, p_ext):
		if p_file == None or os.path.exists(p_file) == False:
			path = p_defaultPath
		else:
			path = p_file
		
		if os.path.exists(path) == False:
			path = self.cwd
			
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
		
			now = datetime.now()
			date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
			print('[' + date_time + '] Running simulation: ' + simu['name'] + ' ...')
			code = mod.RunSimulation(simu)
			if code != 0:
				if isinstance(code, str) or isinstance(code, unicode):
					print(simu['name'] + " did not run properly. The error message is:\n" + code)
				elif isinstance(code, int):
					print(simu['name'] + " did not run properly. Check out Code_Aster message files. Exit code: " + str(code))
				else:
					print("Unknown error; exit code: " + str(code))
					
			mod.DeletePycFiles(self.cwd)
				
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
		mod.DeletePycFiles(self.cwd)
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


# workingDir = os.path.dirname(os.path.realpath(__file__))
# saveDir45 = '/home/cae/scratch/RNA/RailPad/PhaseIII/harmoAcoustic_allPads/load45'
# saveDir10 = '/home/cae/scratch/RNA/RailPad/PhaseIII/harmoAcoustic_allPads/load10'

# name = 'EVA10'
# paramFile = os.path.join(workingDir, name + '.py')

# exec("from " + name + " import *")
# baseDir = os.path.join(workingDir, 'Bases', 'Base_' + padDesign)

# if not os.path.exists(baseDir) or len(os.listdir(baseDir)) == 0:
	# simFolder1 = os.path.join(workingDir, name + '_modes')
	# run.RunPhase1(workingDir, simFolder1, paramFile)

# simFolder2 = os.path.join(saveDir10, name)
# run.RunPhase2(workingDir, simFolder2, paramFile)



# name = 'EVA45'
# paramFile = os.path.join(workingDir, name + '.py')

# exec("from " + name + " import *")
# baseDir = os.path.join(workingDir, 'Bases', 'Base_' + padDesign)

# simFolder2 = os.path.join(saveDir45, name)
# run.RunPhase2(workingDir, simFolder2, paramFile)






# # shutil.copytree('/home/cae/Documents/Railpad2/MultiSleeperModel/8_automation/Bases/Base_singleMat', '/home/cae/Documents/Railpad2/MultiSleeperModel/8_automation/Bases/Base_singleMat_RefReal')



