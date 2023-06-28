#from ast import Try
#from symbol import try_stmt
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
from PyQt5.uic import loadUi
import os
import sys
import shutil
import json

class ImpulseModelGUI(QMainWindow):
	def __init__(self):
		# Initialize + load UI
		super(ImpulseModelGUI, self).__init__()
		# Set the different path
		self.GUI_dir = os.path.dirname(os.path.realpath(__file__))
		self.modelDir = os.path.dirname(self.GUI_dir)
		self.workingDir = os.path.join(self.modelDir,'working_directory')

		self.messagespath=os.path.join(self.workingDir, 'messages')

		self.meshesPath = os.path.join(self.modelDir,'meshes')
		self.materialsPath = os.path.join(self.modelDir,'meshes')

		self.padmaterialspath=os.path.join(self.modelDir,'materials', 'pad')
		self.sleepermaterialspath=os.path.join(self.modelDir,'materials', 'sleeper')
		self.railmaterialspath=os.path.join(self.modelDir,'materials', 'rail')
		self.ballastmaterialspath=os.path.join(self.modelDir,'materials', 'ballast')
		self.USPmaterialspath=os.path.join(self.modelDir,'materials', 'USP')

		self.padmeshespath=os.path.join(self.modelDir,'meshes', 'pad')
		self.sleepermeshespath=os.path.join(self.modelDir,'meshes', 'sleeper')
		self.railmeshespath=os.path.join(self.modelDir,'meshes', 'rail')
		self.ballastmeshespath=os.path.join(self.modelDir,'meshes', 'ballast')
		self.USPmeshespath=os.path.join(self.modelDir,'meshes', 'USP')
		
		loadUi(os.path.join(self.GUI_dir, 'impulse_model_gui.ui'), self)
		self.setWindowTitle('Impulse Model')

         # Signals & slots
		self.newPadMeshButton.clicked.connect(self.NewPadMesh)
		self.newSleeperMeshButton.clicked.connect(self.NewSleeperMesh)
		self.newRailMeshButton.clicked.connect(self.NewRailMesh)
		self.newBallastMeshButton.clicked.connect(self.NewBallastMesh)
		self.newUSPMeshButton.clicked.connect(self.NewUSPMesh)
		self.newPadMaterialButton.clicked.connect(self.NewPadMaterial)
		self.newSleeperMaterialButton.clicked.connect(self.NewSleeperMaterial)
		self.newRailMaterialButton.clicked.connect(self.NewRailMaterial)
		self.newBallastMaterialButton.clicked.connect(self.NewBallastMaterial)
		self.newUSPMaterialButton.clicked.connect(self.NewUSPMaterial)
		self.runButton.clicked.connect(self.Run)
		self.btn_clear.clicked.connect(self.ClearFolders)
		self.btn_updateCB.clicked.connect(self.UpdateComboBoxes)

		self.UpdateComboBoxes()
		self.ClearFolders()

	def UpdateComboBoxes(self):
		comboBoxes = [self.railMeshes, self.railMaterial, self.padMeshes, self.padMaterial1, self.padMaterial2, \
					  self.sleeperMeshes, self.sleeperMaterial, self.ballastMeshes, self.ballastMaterial, self.USPMeshes, self.USPMaterial]
		
		paths = [self.railmeshespath, self.railmaterialspath, self.padmeshespath, self.padmaterialspath, self.padmaterialspath, \
				 self.sleepermeshespath, self.sleepermaterialspath, self.ballastmeshespath, self.ballastmaterialspath, self.USPmeshespath, self.USPmaterialspath]
		
		for i in range(len(comboBoxes)):
			cb = comboBoxes[i]
			path = paths[i]
			
			cb.clear()
			myList = os.listdir(path)
			cb.addItems(myList)

		
	def NewPadMesh(self):
		"""Launch the new pad mesh dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_mesh_dialog.ui')
		dlg = NewMeshDialog(uiPath, self, 'pad')
		dlg.show()
		self.newMeshFile = dlg.exec_()
		if(self.newPadMeshFile == 1):
			self.padMeshes.clear()
			mesh_list = os.listdir(self.padmeshespath)
			# adding list of items to combo box
			self.padMeshes.addItems(mesh_list)
		
	def NewSleeperMesh(self):
		"""Launch the new sleeper mesh dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_mesh_dialog.ui')
		dlg = NewMeshDialog(uiPath, self, 'sleeper')
		dlg.show()
		self.newSleeperMeshFile = dlg.exec_()
		if(self.newSleeperMeshFile == 1):
			self.sleeperMeshes.clear()
			mesh_list = os.listdir(self.sleepermeshespath)
			# adding list of items to combo box
			self.sleeperMeshes.addItems(mesh_list)
		
	def NewRailMesh(self):
		"""Launch the new rail mesh dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_mesh_dialog.ui')
		dlg = NewMeshDialog(uiPath, self, 'rail')
		dlg.show()
		self.newRailMeshFile = dlg.exec_()
		if(self.newRailMeshFile == 1):
			self.railMeshes.clear()
			mesh_list = os.listdir(self.railmeshespath)
			# adding list of items to combo box
			self.railMeshes.addItems(mesh_list)
		
	def NewBallastMesh(self):
		"""Launch the new ballast mesh dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_mesh_dialog.ui')
		dlg = NewMeshDialog(uiPath, self, 'ballast')
		dlg.show()
		self.newBallastMeshFile = dlg.exec_()
		if(self.newBallastMeshFile == 1):
			self.ballastMeshes.clear()
			mesh_list = os.listdir(self.ballastmeshespath)
			# adding list of items to combo box
			self.ballastMeshes.addItems(mesh_list)

	def NewUSPMesh(self):
		"""Launch the new USP mesh dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_mesh_dialog.ui')
		dlg = NewMeshDialog(uiPath, self, 'USP')
		dlg.show()
		self.newUSPMeshFile = dlg.exec_()
		if(self.newUSPMeshFile == 1):
			self.padMeshes.clear()
			mesh_list = os.listdir(self.USPmeshespath)
			# adding list of items to combo box
			self.padMeshes.addItems(mesh_list)

	def NewPadMaterial(self):
		"""Launch the new pad material dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_ViscMat_dialog.ui')
		dlg = NewViscMatDialog(uiPath, self, 'pad')
		dlg.show()
		self.newPadMaterialFile = dlg.exec_()
		if(self.newPadMaterialFile == 1):
			self.padMaterial1.clear()
			self.padMaterial2.clear()
			materials_list = os.listdir(self.padmaterialspath)
			# adding list of items to combo box
			self.padMaterial1.addItems(materials_list)
			self.padMaterial2.addItems(materials_list)
			# self.DisplayMX1(self.currentMaterial1)
			# self.DisplayMX2(self.currentMaterial2)

	def NewSleeperMaterial(self):
		"""Launch the new sleeper material dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_ElasMat_dialog.ui')
		dlg = NewElasMatDialog(uiPath, self, 'sleeper')
		dlg.show()
		self.newSleeperMaterialFile = dlg.exec_()
		if(self.newSleeperMaterialFile == 1):
			self.sleeperMaterial.clear()
			materials_list = os.listdir(self.sleepermaterialspath)
			# adding list of items to combo box
			self.sleeperMaterial.addItems(materials_list)

	def NewRailMaterial(self):
		"""Launch the new rail material dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_ElasMat_dialog.ui')
		dlg = NewElasMatDialog(uiPath, self, 'rail')
		dlg.show()
		self.newRailMaterialFile = dlg.exec_()
		if(self.newRailMaterialFile == 1):
			self.railMaterial.clear()
			materials_list = os.listdir(self.railmaterialspath)
			# adding list of items to combo box
			self.railMaterial.addItems(materials_list)

	def NewBallastMaterial(self):
		"""Launch the new ballast material dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_ElasMat_dialog.ui')
		dlg = NewElasMatDialog(uiPath, self, 'ballast')
		dlg.show()
		self.newBallastMaterialFile = dlg.exec_()
		if(self.newBallastMaterialFile == 1):
			self.ballastMaterial.clear()
			materials_list = os.listdir(self.ballastmaterialspath)
			# adding list of items to combo box
			self.ballastMaterial.addItems(materials_list)

	def NewUSPMaterial(self):
		"""Launch the new USP material dialog."""
		uiPath = os.path.join(self.GUI_dir,'new_ElasMat_dialog.ui')
		dlg = NewElasMatDialog(uiPath, self, 'USP')
		dlg.show()
		self.newUSPMaterialFile = dlg.exec_()
		if(self.newUSPMaterialFile == 1):
			self.USPMaterial.clear()
			materials_list = os.listdir(self.USPmaterialspath)
			# adding list of items to combo box
			self.USPMaterial.addItems(materials_list)


	def MoveFilesMX(self, material=1):
		
		if (material == 1):
			mx = self.padMaterial1.currentText()
			mx_type = 'mx1'
		if (material == 2):
			mx = self.padMaterial2.currentText()
			mx_type = 'mx2'
		# Moving the material1 properties files in WD
		# E1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.workingDir
		fileOldName = 'E.csv'
		fileNewName = 'E_' + mx_type + '.csv'
		Utils.CopyFile(src, dst, fileOldName, fileNewName)
		# G1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.workingDir
		fileOldName = 'G.csv'
		fileNewName = 'G_' + mx_type + '.csv'
		Utils.CopyFile(src, dst, fileOldName, fileNewName)
		# K1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.workingDir
		fileOldName = 'K.csv'
		fileNewName = 'K_' + mx_type + '.csv'
		Utils.CopyFile(src, dst, fileOldName, fileNewName)
		# tau1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.workingDir
		fileOldName = 'tau.csv'
		fileNewName = 'tau_' + mx_type + '.csv'
		Utils.CopyFile(src, dst, fileOldName, fileNewName)
		# Poisson's Ratio1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.workingDir
		fileOldName = 'poisson.csv'
		fileNewName = 'poisson_' + mx_type + '.csv'
		Utils.CopyFile(src, dst, fileOldName, fileNewName)
		# Density1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.workingDir
		fileOldName = 'density.csv'
		fileNewName = 'density_' + mx_type + '.csv'
		Utils.CopyFile(src, dst, fileOldName, fileNewName)
		
	def IsMeshOK(self):
		"""Launch the popup message."""
		uiPath = os.path.join(self.GUI_dir,'mesh_ok.ui')
		dlg = MeshOKDialog(uiPath)
		dlg.show()
		self.isOK = dlg.exec_()



	def Run(self):
		self.ClearFolders()

		parameters = {}
     
		resultsDirectoryPath = os.path.join(self.pathWorkingDirectory.text(), self.nameSimu.text())

		parameters['ResultsDir'] = resultsDirectoryPath

		USP_on = self.cb_USP.isChecked()
		parameters['USP_on'] = USP_on
         
        # Create user folders for results
		if os.path.exists(resultsDirectoryPath) == True:
			try:
				shutil.rmtree(resultsDirectoryPath)
			except:
				pass
		
		try:
			os.makedirs(resultsDirectoryPath)
			os.mkdir(os.path.join(resultsDirectoryPath,'med_files'))
			os.mkdir(os.path.join(resultsDirectoryPath,'results_files'))
			os.mkdir(os.path.join(resultsDirectoryPath,'message_files'))
			os.mkdir(os.path.join(resultsDirectoryPath,'mesh_assembly'))
		except:
			print("Problem creating the results folders.")
			return
			
		# Create a file for the study parameters
		with open(os.path.join(resultsDirectoryPath,'study_parameters.txt'),'a+') as fp:
			fp.write('Here are the parameters selected for the sutdy: ' + resultsDirectoryPath + '\n\n')

		# Moving the meshes file in WD
		srcPad = os.path.join(self.padmeshespath, self.padMeshes.currentText())
		srcSleeper = os.path.join(self.sleepermeshespath, self.sleeperMeshes.currentText())
		srcRail = os.path.join(self.railmeshespath, self.railMeshes.currentText())
		srcBallast = os.path.join(self.ballastmeshespath, self.ballastMeshes.currentText())
		srcUSP = os.path.join(self.USPmeshespath, self.USPMeshes.currentText())
		dst = self.workingDir
		filePadOldName = os.listdir(srcPad)[0]
		fileSleeperOldName = os.listdir(srcSleeper)[0]
		fileRailOldName = os.listdir(srcRail)[0]
		fileBallastOldName = os.listdir(srcBallast)[0]
		fileUSPOldName = os.listdir(srcUSP)[0]
		filePadNewName = 'pad.med'
		fileSleeperNewName = 'sleeper.med'
		fileRailNewName = 'rail.med'
		fileBallastNewName = 'ballast.med'
		fileUSPNewName = 'USP.med'
		try:
			Utils.CopyFile(srcPad, dst, filePadOldName, filePadNewName)
			Utils.CopyFile(srcSleeper, dst, fileSleeperOldName, fileSleeperNewName)
			Utils.CopyFile(srcRail, dst, fileRailOldName, fileRailNewName)
			Utils.CopyFile(srcBallast, dst, fileBallastOldName, fileBallastNewName)
			if USP_on:
				Utils.CopyFile(srcUSP, dst, fileUSPOldName, fileUSPNewName)
		except:
			print("A problem occured while copying the mesh files from the mesh folder to the working directory.")
			return

		
		# Clamps properties		
		parameters['clampStiffX'] = float(self.stiffnessX.text())*1000
		parameters['clampStiffY'] = float(self.stiffnessY.text())*1000
		parameters['clampStiffZ'] = float(self.stiffnessZ.text())*1000
		parameters['clampDampX'] = float(self.dampingX.text())
		parameters['clampDampY'] = float(self.dampingY.text())
		parameters['clampDampZ'] = float(self.dampingZ.text())


		# Sleeper spacing
		parameters['slpSpacing'] = float(self.slpDist.text())

		# Add info in the file of parameters
		with open(os.path.join(resultsDirectoryPath,'study_parameters.txt'),'a') as fp:
			fp.write('The selected meshes are:\n')
			fp.write('Pads: ' + '\n' + self.padMeshes.currentText() + '\n')
			fp.write('Sleepers: ' + '\n' + self.sleeperMeshes.currentText() + '\n')
			fp.write('Rails: ' + '\n' + self.railMeshes.currentText() + '\n')
			fp.write('Ballast: ' + '\n' + self.ballastMeshes.currentText() + '\n\n')
			if USP_on:
				fp.write('USP: ' + '\n' + self.USPMeshes.currentText() + '\n\n')
			fp.write('Distance between sleepers: ' + self.slpDist.text() + '\n\n')

			fp.write('Pads properties:\n')
			fp.write('The material 1 is: ' + self.padMaterial1.currentText() + '\n')
			fp.write('The material 2 is: ' + self.padMaterial2.currentText() + '\n\n')
			fp.write('Sleepers properties:\n')
			fp.write('The sleeper\'s material is: ' + self.sleeperMaterial.currentText() + '\n\n')
			fp.write('Rails properties:\n')
			fp.write('The rail\'s material is: ' + self.railMaterial.currentText() + '\n\n')
			fp.write('Ballasts properties:\n')
			fp.write('The ballast\'s material is: ' + self.ballastMaterial.currentText() + '\n\n')
			if USP_on:
				fp.write('USPs properties:\n')
				fp.write('The USP\'s material is: ' + self.USPMaterial.currentText() + '\n\n')
			fp.write('Clamps properties:\n')
			fp.write('Stiffness:\n')
			fp.write('X : ' + self.stiffnessX.text() + '[MPa]\n')
			fp.write('Y : ' + self.stiffnessY.text() + '[MPa]\n')
			fp.write('Z : ' + self.stiffnessZ.text() + '[MPa]\n')
			fp.write('Damping:\n')
			fp.write('X : ' + self.dampingX.text() + '[-]\n')
			fp.write('Y : ' + self.dampingY.text() + '[-]\n')
			fp.write('Z : ' + self.dampingZ.text() + '[-]\n\n')

		# Write JSON file containing some parameters
		try:
			txt = json.dumps(parameters, indent = 4, sort_keys=True)
			jsonPath = os.path.join(self.workingDir, 'parameters.json')
			with open(jsonPath, 'w') as f:
				f.write(txt)
			f.close()
		except:
			print(jsonPath + ' could not be created.')
			return

		# Move export files to working directory
		# An export file that is run adds the path to all files at the bottom of the file. To avoid that, we need to copy export files "templates" and run the copy
		srcFolder = os.path.join(self.workingDir, 'template_files')
		dstFolder = self.workingDir
		try:
			Utils.CopyFile(srcFolder, dstFolder, 'generateMesh.export')
			Utils.CopyFile(srcFolder, dstFolder, 'impulse.export')
		except:
			print("Problem copying the export files to the working directory.")
			return
		
		if USP_on:
			os.system('sed -i -E "s!__USPmesh__!F mmed USP.med D  10!" ' + os.path.join(self.workingDir, 'generateMesh.export'))
			os.system('sed -i -E "s!__USP_E__!F libr USP_E.csv D  44!" ' + os.path.join(self.workingDir, 'impulse.export'))
			os.system('sed -i -E "s!__USP_Nu__!F libr USP_Nu.csv D  45!" ' + os.path.join(self.workingDir, 'impulse.export'))
			os.system('sed -i -E "s!__USP_Rho__!F libr USP_Rho.csv D  46!" ' + os.path.join(self.workingDir, 'impulse.export'))
			os.system('sed -i -E "s!__USP_AmHyst__!F libr USP_AmHyst.csv D  47!" ' + os.path.join(self.workingDir, 'impulse.export'))
		else:
			os.system('sed -i -E "s!__USPmesh__!!" ' + os.path.join(self.workingDir, 'generateMesh.export'))
			os.system('sed -i -E "s!__USP_E__!!" ' + os.path.join(self.workingDir, 'impulse.export'))
			os.system('sed -i -E "s!__USP_Nu__!!" ' + os.path.join(self.workingDir, 'impulse.export'))
			os.system('sed -i -E "s!__USP_Rho__!!" ' + os.path.join(self.workingDir, 'impulse.export'))
			os.system('sed -i -E "s!__USP_AmHyst__!!" ' + os.path.join(self.workingDir, 'impulse.export'))

		######################################################################################################################
		# Run the command file to assemble the mesh
		######################################################################################################################
		
		# This is not working. This export file is 'not found'. idk why
		# runScript = os.path.join(self.workingDir, 'runGenerateMesh.sh')
		# os.system('bash ' + runScript)

		os.system('cd ' + self.workingDir + '\n ./runGenerateMesh.sh')

		# Copy + Run the script in salome to add the edges
		edgesScript = 'add_clamps.py'
		try:
			Utils.CopyFile(srcFolder, dstFolder, edgesScript)
		except:
			print("Problem copying " + edgesScript + " to the working directory.")
			return
		
		os.system('sed -i -E "s!__workingDir__!' + "'" + self.workingDir + "'" + '!" ' + os.path.join(self.workingDir, edgesScript))
		os.system('/opt/SalomeMeca/appli_V2019_univ/salome -t ' + os.path.join(self.workingDir, edgesScript))

		# Open the mesh in salome
		openMeshScript = 'open_mesh.py'
		try:
			Utils.CopyFile(srcFolder, dstFolder, openMeshScript)
		except:
			print("Problem copying " + openMeshScript + " to the working directory.")
			return
		
		os.system('sed -i -E "s!__workingDir__!' + "'" + self.workingDir + "'" + '!" ' + os.path.join(self.workingDir, openMeshScript))
		os.system(os.path.join(self.workingDir, 'runSalome2019.sh') + ' ' + os.path.join(self.workingDir, openMeshScript))

		self.IsMeshOK()

		if(self.isOK == 0):
			return

		# Moving the materials files in WD
		# pads
		try:
			self.MoveFilesMX(1)
			self.MoveFilesMX(2)
		except:
			print("Problem copying the pads material files to the working directory.")
			return

		# sleeper
		try:
			listOfFiles = ['sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv']
			src = os.path.join(self.sleepermaterialspath, self.sleeperMaterial.currentText())
			dst = self.workingDir
			for fileName in listOfFiles:
				Utils.CopyFile(src, dst, fileName)
		except:
			print("Problem copying the sleepers material files to the working directory.")
			return

		# rail
		try:
			listOfFiles = ['rail_E.csv','rail_Nu.csv','rail_Rho.csv','rail_AmHyst.csv']
			src = os.path.join(self.railmaterialspath, self.railMaterial.currentText())
			dst = self.workingDir
			for fileName in listOfFiles:
				Utils.CopyFile(src, dst, fileName)
		except:
			print("Problem copying the rails material files to the working directory.")
			return

		# ballast
		try:
			listOfFiles = ['ballast_E.csv','ballast_Nu.csv','ballast_Rho.csv','ballast_AmHyst.csv']
			src = os.path.join(self.ballastmaterialspath, self.ballastMaterial.currentText())
			dst = self.workingDir
			for fileName in listOfFiles:
				Utils.CopyFile(src, dst, fileName)
		except:
			print("Problem copying the ballast material files to the working directory.")
			return
		
		# USP
		if USP_on:
			try:
				listOfFiles = ['USP_E.csv','USP_Nu.csv','USP_Rho.csv','USP_AmHyst.csv']
				src = os.path.join(self.USPmaterialspath, self.USPMaterial.currentText())
				dst = self.workingDir
				for fileName in listOfFiles:
					Utils.CopyFile(src, dst, fileName)
			except:
				print("Problem copying the USP material files to the working directory.")
				return


		# Run main simulation
		# os.system('cd working_directory \n bash runImpulse.sh')
		os.system('cd ' + self.workingDir + '\n ./runImpulse.sh')


		Utils.CopyFile(self.messagespath, os.path.join(resultsDirectoryPath,'message_files'), 'impulse.mess')
		Utils.CopyFile(self.messagespath, os.path.join(resultsDirectoryPath,'message_files'), 'generateMesh.mess')
		Utils.CopyFile(self.workingDir, os.path.join(resultsDirectoryPath,'med_files'), 'resultImpulse.res.med')
		Utils.CopyFile(self.workingDir, os.path.join(resultsDirectoryPath,'mesh_assembly'), 'unitCellWithClamps.med')
		Utils.CopyFile(self.workingDir, os.path.join(resultsDirectoryPath,'results_files'), 'Resultats_ballast_impulse_INVAR.txt')
		Utils.CopyFile(self.workingDir, os.path.join(resultsDirectoryPath,'results_files'), 'Resultats_ballast_impulse_SGIM.txt')
		Utils.CopyFile(self.workingDir, os.path.join(resultsDirectoryPath,'results_files'), 'Resultats_impulse.txt')


	def ClearFolders(self):
		# Remove unnecessary files from working directory
		for fileOrDir in os.listdir(self.workingDir):
			path = os.path.join(self.workingDir, fileOrDir)

			if os.path.isdir(path):
				if fileOrDir not in ['include', 'src', 'template_files']:
					shutil.rmtree(path)
			elif os.path.isfile(path):
				if os.path.splitext(fileOrDir)[1][1:] not in ['sh', 'comm', 'mfront', 'so']:
					os.remove(path)

		# Correct potential problems with DOS / Unix files
		scriptPath = os.path.join(os.path.dirname(self.modelDir), 'correctBashFiles.sh')
		os.system('bash ' + scriptPath)






class MeshOKDialog(QDialog):
	"""POPup For mesh checking."""
	def __init__(self, uiPath):
		super(MeshOKDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('Mesh verification')
		self.goButton.clicked.connect(self.Go)
		self.stopButton.clicked.connect(self.Stop)

	def Go(self):
		self.accept()

	def Stop(self):
		self.close()



class NewMeshDialog(QDialog):
	"""New Mesh dialog."""
	def __init__(self, uiPath, interface, partName):
		super(NewMeshDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New mesh selection')
		self.browseNewMeshButton.clicked.connect(self.MeshDownload)
		self.addMeshButton.clicked.connect(self.AddNewMesh)
		self.cancelButton.clicked.connect(self.Cancel)
		self.partName = partName
		self.interface = interface
  
	def MeshDownload(self):
		self.newMesh = QFileDialog.getOpenFileName(self, "Open " + self.partName + " Med File", self.interface.modelDir)

	def AddNewMesh(self):
		if self.newMeshName.text() == '':
			QMessageBox.information(self, 'Error', 'Please enter a mesh name.', QMessageBox.Ok,)
			return
		
		newMeshDirectoryPath = os.path.join(self.interface.meshesPath, self.partName, self.newMeshName.text())
		Utils.CopyFile(os.path.dirname(self.newMesh), newMeshDirectoryPath, os.path.basename(self.newMesh), self.partName + '.med')
		self.accept()

	def Cancel(self):
		self.close()




class NewViscMatDialog(QDialog):
	"""New Pad Material dialog."""
	def __init__(self, uiPath, interface, partName):
		super(NewViscMatDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New ' + partName + ' viscoelastic material selection')
		self.newModulusButton.clicked.connect(self.EDownload)
		self.newKButton.clicked.connect(self.KDownload)
		self.newGButton.clicked.connect(self.GDownload)
		self.newTauButton.clicked.connect(self.tauDownload)
		self.addMaterialButton.clicked.connect(self.AddNewMaterial)
		self.cancelButton.clicked.connect(self.Cancel)

		self.interface = interface
		self.partName = partName

		self.newModulus = None
		self.newK = None
		self.newG = None
		self.newtau = None

	def EDownload(self):
		self.newModulus = QFileDialog.getOpenFileName(self, "Open csv File", self.interface.modelDir)

	def KDownload(self):
		self.newK = QFileDialog.getOpenFileName(self, "Open csv File",self.interface.modelDir)
		
	def GDownload(self):
		self.newG = QFileDialog.getOpenFileName(self, "Open csv File",self.interface.modelDir)
		
	def tauDownload(self):
		self.newtau = QFileDialog.getOpenFileName(self, "Open csv File",self.interface.modelDir)

	def AddNewMaterial(self):

		if self.newModulus is None or self.newK is None or self.newG is None or self.newtau is None:
			QMessageBox.information(self, 'Error', 'Please select all materials properties.', QMessageBox.Ok,)
			return
		
		newMaterialDirectoryPath = os.path.join(self.interface.materialsPath, self.partName, self.newMaterialName.text())

		Utils.CopyFile(os.path.dirname(self.newModulus), newMaterialDirectoryPath, os.path.basename(self.newModulus), 'E.csv')
		Utils.CopyFile(os.path.dirname(self.newK), newMaterialDirectoryPath, os.path.basename(self.newK), 'K.csv')
		Utils.CopyFile(os.path.dirname(self.newG), newMaterialDirectoryPath, os.path.basename(self.newG), 'G.csv')
		Utils.CopyFile(os.path.dirname(self.newtau), newMaterialDirectoryPath, os.path.basename(self.newtau), 'tau.csv')

  
		# Add poisson ratio
		with open(os.path.join(newMaterialDirectoryPath,'poisson.csv'),'w') as fp:
			fp.write(self.newMaterialPoisson.text())

		# Add density
		with open(os.path.join(newMaterialDirectoryPath,'density.csv'),'w') as fp:
			fp.write(self.newMaterialDensity.text())

		self.accept()

	def Cancel(self):
		self.close()


class NewElasMatDialog(QDialog):
	"""New Elastic Material dialog."""
	def __init__(self, uiPath, interface, partName):
		super(NewElasMatDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New ' + partName + ' elastic material selection')
		self.addMaterialButton.clicked.connect(self.AddNewMaterial)
		self.cancelButton.clicked.connect(self.Cancel)

		self.partName = partName
		self.interface = interface

	def AddNewMaterial(self):

		if self.newMaterialName.text(self.newMaterialName.text()) == '':
			QMessageBox.information(self, 'Error', 'Please select a material name.', QMessageBox.Ok,)
			return

		newMaterialDirectoryPath = os.path.join(self.interface.materialsPath, self.partName, self.newMaterialName.text())
		
		if os.path.exists(newMaterialDirectoryPath) == False:
			try:
				os.makedirs(newMaterialDirectoryPath)
			except:
				QMessageBox.information(self, 'Error', 'Impossible to create directory ' +  newMaterialDirectoryPath, QMessageBox.Ok,)
				return
			
		if self.newMaterialName.text(self.newMaterialModulus.text()) == '':
			QMessageBox.information(self, 'Error', 'Please enter all materials properties.', QMessageBox.Ok,)
			return

		if self.newMaterialName.text(self.newMaterialDamp.text()) == '':
			QMessageBox.information(self, 'Error', 'Please enter all materials properties.', QMessageBox.Ok,)
			return
		
		if self.newMaterialName.text(self.newMaterialPoisson.text()) == '':
			QMessageBox.information(self, 'Error', 'Please enter all materials properties.', QMessageBox.Ok,)
			return

		if self.newMaterialName.text(self.newMaterialDensity.text()) == '':
			QMessageBox.information(self, 'Error', 'Please enter all materials properties.', QMessageBox.Ok,)
			return	
  
		# Add Young Modulus
		with open(os.path.join(newMaterialDirectoryPath, self.partName + '_E.csv'),'w') as fp:
			fp.write(self.newMaterialModulus.text())
  
		# Add Hysteretic damping
		with open(os.path.join(newMaterialDirectoryPath, self.partName + '_AmHyst.csv'),'w') as fp:
			fp.write(self.newMaterialDamp.text())
  
		# Add poisson ratio
		with open(os.path.join(newMaterialDirectoryPath, self.partName + '_Nu.csv'),'w') as fp:
			fp.write(self.newMaterialPoisson.text())

		# Add density
		with open(os.path.join(newMaterialDirectoryPath, self.partName + '_Rho.csv'),'w') as fp:
			fp.write(self.newMaterialDensity.text())

		self.accept()

	def Cancel(self):
		self.close()


class Utils:

	@staticmethod
	def CopyFile(src_folder, dst_folder, fileOldName, fileNewName = None):

		if fileNewName is None:
			fileNewName = fileOldName

		sourceFile = os.path.join(src_folder, fileOldName)
		destinationFile = os.path.join(dst_folder, fileNewName)

		if os.path.exists(dst_folder) == False:
			try:
				os.makedirs(dst_folder)
			except:
				print('Impossible to create directory ' + dst_folder)
				return

		try:
			shutil.copyfile(sourceFile, destinationFile)
		except:
			print('Problem copying ' + sourceFile + ' to ' + fileNewName)




if __name__ == '__main__':
	app = QApplication([]) #sys.argv
	widget = ImpulseModelGUI()
	widget.show()
	sys.exit(app.exec_())
