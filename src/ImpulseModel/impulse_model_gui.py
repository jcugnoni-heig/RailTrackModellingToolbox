#from ast import Try
#from symbol import try_stmt
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
from PyQt5.uic import loadUi
import os
import sys
import shutil

class ImpulseModelGUI(QMainWindow):
	def __init__(self):
		# Initialize + load UI
		super(ImpulseModelGUI, self).__init__()
		# Set the different path
		filepath=os.getcwd()
		self.working_directorypath=os.path.join(filepath,'working_directory')
		self.messagespath=os.path.join(filepath,'working_directory/messages')
		self.padmaterialspath=os.path.join(filepath,'materials/Pad')
		self.sleepermaterialspath=os.path.join(filepath,'materials/Sleeper')
		self.railmaterialspath=os.path.join(filepath,'materials/Rail')
		self.ballastmaterialspath=os.path.join(filepath,'materials/Ballast')
		self.padmeshespath=os.path.join(filepath,'meshes/Pads')
		self.sleepermeshespath=os.path.join(filepath,'meshes/Sleepers')
		self.railmeshespath=os.path.join(filepath,'meshes/Rails')
		self.ballastmeshespath=os.path.join(filepath,'meshes/Ballasts')
		uiFilePath=os.path.join(filepath,'impulse_model_gui.ui')
		loadUi(uiFilePath, self)
		self.setWindowTitle('Impulse Model')
		
		
		# Attributes

        # pad mesh list
		pad_mesh_list = os.listdir(self.padmeshespath)
        # adding list of items to combo box
		self.padMeshes.addItems(pad_mesh_list)
        # pad material list
		pad_materials_list = os.listdir(self.padmaterialspath)
		# adding list of items to combo box
		self.padMaterial1.addItems(pad_materials_list)
		self.padMaterial2.addItems(pad_materials_list)

        # sleeper mesh list
		sleeper_mesh_list = os.listdir(self.sleepermeshespath)
        # adding list of items to combo box
		self.sleeperMeshes.addItems(sleeper_mesh_list)
        # sleeper material list
		sleeper_materials_list = os.listdir(self.sleepermaterialspath)
		# adding list of items to combo box
		self.sleeperMaterial.addItems(sleeper_materials_list)

        # rail mesh list
		rail_mesh_list = os.listdir(self.railmeshespath)
        # adding list of items to combo box
		self.railMeshes.addItems(rail_mesh_list)
        # rail material list
		rail_materials_list = os.listdir(self.railmaterialspath)
		# adding list of items to combo box
		self.railMaterial.addItems(rail_materials_list)

        # ballast mesh list
		ballast_mesh_list = os.listdir(self.ballastmeshespath)
        # adding list of items to combo box
		self.ballastMeshes.addItems(ballast_mesh_list)
        # ballast material list
		ballast_materials_list = os.listdir(self.ballastmaterialspath)
		# adding list of items to combo box
		self.ballastMaterial.addItems(ballast_materials_list)
  
         # Signals & slots
		self.newPadMeshButton.clicked.connect(self.NewPadMesh)
		self.newSleeperMeshButton.clicked.connect(self.NewSleeperMesh)
		self.newRailMeshButton.clicked.connect(self.NewRailMesh)
		self.newBallastMeshButton.clicked.connect(self.NewBallastMesh)
		self.newPadMaterialButton.clicked.connect(self.NewPadMaterial)
		self.newSleeperMaterialButton.clicked.connect(self.NewSleeperMaterial)
		self.newRailMaterialButton.clicked.connect(self.NewRailMaterial)
		self.newBallastMaterialButton.clicked.connect(self.NewBallastMaterial)
		self.runButton.clicked.connect(self.Run)
		
	def NewPadMesh(self):
		"""Launch the new pad mesh dialog."""
		uiPath = os.path.join(os.getcwd(),'new_pad_mesh_dialog.ui')
		dlg = NewPadMeshDialog(uiPath)
		dlg.show()
		self.newMeshFile = dlg.exec_()
		if(self.newPadMeshFile == 1):
			self.padMeshes.clear()
			mesh_list = os.listdir(self.padmeshespath)
			# adding list of items to combo box
			self.padMeshes.addItems(mesh_list)
		
	def NewSleeperMesh(self):
		"""Launch the new sleeper mesh dialog."""
		uiPath = os.path.join(os.getcwd(),'new_sleeper_mesh_dialog.ui')
		dlg = NewSleeperMeshDialog(uiPath)
		dlg.show()
		self.newSleeperMeshFile = dlg.exec_()
		if(self.newSleeperMeshFile == 1):
			self.sleeperMeshes.clear()
			mesh_list = os.listdir(self.sleepermeshespath)
			# adding list of items to combo box
			self.sleeperMeshes.addItems(mesh_list)
		
	def NewRailMesh(self):
		"""Launch the new rail mesh dialog."""
		uiPath = os.path.join(os.getcwd(),'new_rail_mesh_dialog.ui')
		dlg = NewRailMeshDialog(uiPath)
		dlg.show()
		self.newRailMeshFile = dlg.exec_()
		if(self.newRailMeshFile == 1):
			self.railMeshes.clear()
			mesh_list = os.listdir(self.railmeshespath)
			# adding list of items to combo box
			self.railMeshes.addItems(mesh_list)
		
	def NewBallastMesh(self):
		"""Launch the new ballast mesh dialog."""
		uiPath = os.path.join(os.getcwd(),'new_ballast_mesh_dialog.ui')
		dlg = NewBallastMeshDialog(uiPath)
		dlg.show()
		self.newBallastMeshFile = dlg.exec_()
		if(self.newBallastMeshFile == 1):
			self.padMeshes.clear()
			mesh_list = os.listdir(self.padmeshespath)
			# adding list of items to combo box
			self.padMeshes.addItems(mesh_list)

	def NewPadMaterial(self):
		"""Launch the new pad material dialog."""
		uiPath = os.path.join(os.getcwd(),'new_pad_material_dialog.ui')
		dlg = NewPadMaterialDialog(uiPath)
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
		uiPath = os.path.join(os.getcwd(),'new_sleeper_material_dialog.ui')
		dlg = NewSleeperMaterialDialog(uiPath)
		dlg.show()
		self.newSleeperMaterialFile = dlg.exec_()
		if(self.newSleeperMaterialFile == 1):
			self.sleeperMaterial.clear()
			materials_list = os.listdir(self.sleepermaterialspath)
			# adding list of items to combo box
			self.sleeperMaterial.addItems(materials_list)

	def NewRailMaterial(self):
		"""Launch the new rail material dialog."""
		uiPath = os.path.join(os.getcwd(),'new_rail_material_dialog.ui')
		dlg = NewRailMaterialDialog(uiPath)
		dlg.show()
		self.newRailMaterialFile = dlg.exec_()
		if(self.newRailMaterialFile == 1):
			self.railMaterial.clear()
			materials_list = os.listdir(self.railmaterialspath)
			# adding list of items to combo box
			self.railMaterial.addItems(materials_list)

	def NewBallastMaterial(self):
		"""Launch the new ballast material dialog."""
		uiPath = os.path.join(os.getcwd(),'new_ballast_material_dialog.ui')
		dlg = NewBallastMaterialDialog(uiPath)
		dlg.show()
		self.newBallastMaterialFile = dlg.exec_()
		if(self.newBallastMaterialFile == 1):
			self.ballastMaterial.clear()
			materials_list = os.listdir(self.ballastmaterialspath)
			# adding list of items to combo box
			self.ballastMaterial.addItems(materials_list)

	def MoveAndRename(self, src_folder, dst_folder, fileOldName, fileNewName):
		
		# Moving the file in WD
		sourceFile = os.path.join(src_folder, fileOldName)
		destinationFile = os.path.join(dst_folder, fileOldName)
		# Moving the file
		shutil.copyfile(sourceFile, destinationFile)
		# Renaming the file in WD
		destinationFileOldName = os.path.join(dst_folder, fileOldName)
		destinationFileNewName = os.path.join(dst_folder, fileNewName)
		os.rename(destinationFileOldName, destinationFileNewName)

	def MoveOnly(self, src_folder, dst_folder, fileName):
		
		# Moving the file in WD
		sourceFile = os.path.join(src_folder, fileName)
		destinationFile = os.path.join(dst_folder, fileName)
		# Moving the file
		shutil.copyfile(sourceFile, destinationFile)



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
		dst = self.working_directorypath
		fileOldName = 'E.csv'
		fileNewName = 'E_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# G1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'G.csv'
		fileNewName = 'G_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# K1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'K.csv'
		fileNewName = 'K_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# tau1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'tau.csv'
		fileNewName = 'tau_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# Poisson's Ratio1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'poisson.csv'
		fileNewName = 'poisson_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# Density1
		src = os.path.join(self.padmaterialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'density.csv'
		fileNewName = 'density_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		
	def IsMeshOK(self):
		"""Launch the popup message."""
		uiPath = os.path.join(os.getcwd(),'mesh_ok.ui')
		dlg = MeshOKDialog(uiPath)
		dlg.show()
		self.isOK = dlg.exec_()



	def Run(self):
     
		self.resultsDirectoryName = self.nameSimu.text()
		self.resultsDirectoryPath = os.path.join(self.pathWorkingDirectory.text(), self.resultsDirectoryName)
         
         # Create user folders for results
		try:
			os.mkdir(self.resultsDirectoryPath)
			os.mkdir(os.path.join(self.resultsDirectoryPath,'med_files'))
			os.mkdir(os.path.join(self.resultsDirectoryPath,'results_files'))
			os.mkdir(os.path.join(self.resultsDirectoryPath,'message_files'))
			os.mkdir(os.path.join(self.resultsDirectoryPath,'mesh_assembly'))
		except:
			print("Problem creating the results folders. Maybe the folder already exist ?")
			return
		# Create a file for the study parameters
		with open(os.path.join(self.resultsDirectoryPath,'study_parameters.txt'),'a+') as fp:
			fp.write('Here are the parameters selected for the sutdy: ' + self.resultsDirectoryName + '\n\n')

		# Moving the meshes file in WD
		srcPad = os.path.join(self.padmeshespath, self.padMeshes.currentText())
		srcSleeper = os.path.join(self.sleepermeshespath, self.sleeperMeshes.currentText())
		srcRail = os.path.join(self.railmeshespath, self.railMeshes.currentText())
		srcBallast = os.path.join(self.ballastmeshespath, self.ballastMeshes.currentText())
		dst = self.working_directorypath
		filePadOldName = os.listdir(srcPad)[0]
		fileSleeperOldName = os.listdir(srcSleeper)[0]
		fileRailOldName = os.listdir(srcRail)[0]
		fileBallastOldName = os.listdir(srcBallast)[0]
		filePadNewName = 'pad.med'
		fileSleeperNewName = 'sleeper.med'
		fileRailNewName = 'rail.med'
		fileBallastNewName = 'ballast.med'
		try:
			self.MoveAndRename(srcPad, dst, filePadOldName, filePadNewName)
			self.MoveAndRename(srcSleeper, dst, fileSleeperOldName, fileSleeperNewName)
			self.MoveAndRename(srcRail, dst, fileRailOldName, fileRailNewName)
			self.MoveAndRename(srcBallast, dst, fileBallastOldName, fileBallastNewName)
		except:
			print("A problem occure while copying the mesh files from the mesh folder to the working directory.")
			return

		
		# If no properties are given for the clamps stiffness and damping they are put to 0.
		if(self.stiffnessX.text() == ""):
			self.stiffnessX.setText("0")

		if(self.stiffnessY.text() == ""):
			self.stiffnessY.setText("0")

		if(self.stiffnessZ.text() == ""):
			self.stiffnessZ.setText("0")

		if(self.dampingX.text() == ""):
			self.dampingX.setText("0")

		if(self.dampingY.text() == ""):
			self.dampingY.setText("0")

		if(self.dampingZ.text() == ""):
			self.dampingZ.setText("0")
		# Create a file for the clamps properties
		with open(os.path.join(self.working_directorypath,'clamps_properties.txt'),'a+') as fp:
			fp.write('Stiffness:\n')
			fp.write(self.stiffnessX.text() + '\n')
			fp.write(self.stiffnessY.text() + '\n')
			fp.write(self.stiffnessZ.text() + '\n')
			fp.write('Damping:\n')
			fp.write(self.dampingX.text() + '\n')
			fp.write(self.dampingY.text() + '\n')
			fp.write(self.dampingZ.text() + '\n')

		# Create a file for the distance between sleepers 
		with open(os.path.join(self.working_directorypath,'sleeperDistance.csv'),'a+') as fp:
			fp.write(self.slpDist.text())

		# Add info in the file of parameters
		with open(os.path.join(self.resultsDirectoryPath,'study_parameters.txt'),'a') as fp:
			fp.write('The selected meshes are:\n')
			fp.write('Pads: ' + '\n' + self.padMeshes.currentText() + '\n')
			fp.write('Sleepers: ' + '\n' + self.sleeperMeshes.currentText() + '\n')
			fp.write('Rails: ' + '\n' + self.railMeshes.currentText() + '\n')
			fp.write('Ballast: ' + '\n' + self.ballastMeshes.currentText() + '\n\n')
			fp.write('Distance between sleepers: ' + self.slpDist.text() + '\n\n')

		# Add info in the file of parameters
		with open(os.path.join(self.resultsDirectoryPath,'study_parameters.txt'),'a') as fp:
			fp.write('Pads properties:\n')
			fp.write('The material 1 is: ' + self.padMaterial1.currentText() + '\n')
			fp.write('The material 2 is: ' + self.padMaterial2.currentText() + '\n\n')
			fp.write('Sleepers properties:\n')
			fp.write('The sleeper\'s material is: ' + self.sleeperMaterial.currentText() + '\n\n')
			fp.write('Rails properties:\n')
			fp.write('The rail\'s material is: ' + self.railMaterial.currentText() + '\n\n')
			fp.write('Ballasts properties:\n')
			fp.write('The ballast\'s material is: ' + self.ballastMaterial.currentText() + '\n\n')
			fp.write('Clamps properties:\n')
			fp.write('Stiffness:\n')
			fp.write('X : ' + self.stiffnessX.text() + '[MPa]\n')
			fp.write('Y : ' + self.stiffnessY.text() + '[MPa]\n')
			fp.write('Z : ' + self.stiffnessZ.text() + '[MPa]\n')
			fp.write('Damping:\n')
			fp.write('X : ' + self.dampingX.text() + '[-]\n')
			fp.write('Y : ' + self.dampingY.text() + '[-]\n')
			fp.write('Z : ' + self.dampingZ.text() + '[-]\n\n')

		# Run the cmmande file to assemble the mesh
		os.system('cd working_directory \n ./gen3SleepersMesh.sh')

		# Run the script in salome to add the edges
		os.system('/opt/SalomeMeca/appli_V2019_univ/salome -t ' + self.working_directorypath + '/script_to_add_edges.py')

		# Open the mesh in salome
		os.system('/opt/SalomeMeca/runSalome2019.sh ' + self.working_directorypath + '/open_mesh.py')

		self.IsMeshOK()
		if(self.isOK == 1):

			# Moving the materials files in WD
			# pads
			try:
				self.MoveFilesMX(1)
				self.MoveFilesMX(2)
			except:
				print("Problem copying the pads material files to the working directory.")
				# Delete files of the sutdy
				listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
										'clamps_properties.txt',
										'unitCell.med', 'unitCellWithClamps.med']
				for fileToDelete in listOfFileToDelete:
					os.remove(os.path.join(self.working_directorypath, fileToDelete))
				# removing directory
				shutil.rmtree(self.resultsDirectoryPath)
				return

			# sleeper
			try:
				listOfFiles = ['sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv']
				src = os.path.join(self.sleepermaterialspath, self.sleeperMaterial.currentText())
				dst = self.working_directorypath
				for fileName in listOfFiles:
					self.MoveOnly(src, dst, fileName)
			except:
				print("Problem copying the sleepers material files to the working directory.")
				# Delete files of the sutdy
				listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
										'E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
										'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
										'clamps_properties.txt', 'sleeperDistance.csv',
										'unitCell.med', 'unitCellWithClamps.med']
				for fileToDelete in listOfFileToDelete:
					os.remove(os.path.join(self.working_directorypath, fileToDelete))
				# removing directory
				shutil.rmtree(self.resultsDirectoryPath)
				return

			# rail
			try:
				listOfFiles = ['rail_E.csv','rail_Nu.csv','rail_Rho.csv','rail_AmHyst.csv']
				src = os.path.join(self.railmaterialspath, self.railMaterial.currentText())
				dst = self.working_directorypath
				for fileName in listOfFiles:
					self.MoveOnly(src, dst, fileName)
			except:
				print("Problem copying the rails material files to the working directory.")
				# Delete files of the sutdy
				listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
										'E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
										'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
										'sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv',
										'clamps_properties.txt', 'sleeperDistance.csv',
										'unitCell.med', 'unitCellWithClamps.med']
				for fileToDelete in listOfFileToDelete:
					os.remove(os.path.join(self.working_directorypath, fileToDelete))
				# removing directory
				shutil.rmtree(self.resultsDirectoryPath)
				return

			# ballast
			try:
				listOfFiles = ['ballast_E.csv','ballast_Nu.csv','ballast_Rho.csv','ballast_AmHyst.csv']
				src = os.path.join(self.ballastmaterialspath, self.ballastMaterial.currentText())
				dst = self.working_directorypath
				for fileName in listOfFiles:
					self.MoveOnly(src, dst, fileName)
			except:
				print("Problem copying the ballast material files to the working directory.")
				# Delete files of the sutdy
				listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
										'E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
										'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
										'sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv',
										'rail_E.csv','rail_Nu.csv','rail_Rho.csv','rail_AmHyst.csv',
										'clamps_properties.txt', 'sleeperDistance.csv',
										'unitCell.med', 'unitCellWithClamps.med']
				for fileToDelete in listOfFileToDelete:
					os.remove(os.path.join(self.working_directorypath, fileToDelete))
				# removing directory
				shutil.rmtree(self.resultsDirectoryPath)
				return

			
			# Run phase I
			os.system('cd working_directory \n ./runImpulsePhase1.sh')

			# Run phase II
			os.system('cd working_directory \n ./runImpulsePhase2.sh')

			
			message_copied = True
			med_result_copied = True
			mesh_assembly_copied = True
			txt_results_copied = True

			# Copy messages in User folder
			try:
				listOfFile = ['messageImpulsePhase1.mess','messageImpulsePhase2.mess']
				src = self.messagespath
				dst = os.path.join(self.resultsDirectoryPath,'message_files')
				for fileName in listOfFile:
					self.MoveOnly(src, dst, fileName)
			except:
				print("Problem while copying the message files from the working directory to the result folder.")
				message_copied = False
			

			# Copy med results in User folder
			try:
				listOfFile = ['resultImpulse.res.med']
				src = self.working_directorypath
				dst = os.path.join(self.resultsDirectoryPath,'med_files')
				for fileName in listOfFile:
					self.MoveOnly(src, dst, fileName)
			except:
				print("Problem while copying the .med results file from the working directory to the result folder.")
				med_result_copied = False
			

			# Copy mesh assembly in User folder
			try:
				listOfFile = ['unitCellWithClamps.med']
				src = self.working_directorypath
				dst = os.path.join(self.resultsDirectoryPath,'mesh_assembly')
				for fileName in listOfFile:
					self.MoveOnly(src, dst, fileName)
			except:
				print("Problem while copying the mesh assembly file from the working directory to the result folder.")
				mesh_assembly_copied = False
			

			# Copy impulse results in User folder
			try:
				listOfFile = ['Resultats_ballast_impulse_INVAR.txt', 'Resultats_ballast_impulse_SGIM.txt', 'Resultats_impulse.txt']
				src = self.working_directorypath
				dst = os.path.join(self.resultsDirectoryPath,'results_files')
				for fileName in listOfFile:
					self.MoveOnly(src, dst, fileName)
			except:
				print("Problem while copying the extracted text results files from the working directory to the result folder.")
				txt_results_copied = False



			# Delete files of the sutdy (mx, mesh, message, res.med...etc)
			listOfFileToDelete = ['E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
							'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
							'sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv',
							'rail_E.csv','rail_Nu.csv','rail_Rho.csv','rail_AmHyst.csv',
							'ballast_E.csv','ballast_Nu.csv','ballast_Rho.csv','ballast_AmHyst.csv',
							'pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
							'clamps_properties.txt', 'sleeperDistance.csv',
							'unitCell.med']

			if(med_result_copied):
				listOfFileToDelete = listOfFileToDelete + ['resultImpulse.res.med']

			if(mesh_assembly_copied):
				listOfFileToDelete = listOfFileToDelete + ['unitCellWithClamps.med']

			if(txt_results_copied):
				listOfFileToDelete = listOfFileToDelete + ['Resultats_ballast_impulse_INVAR.txt', 'Resultats_ballast_impulse_SGIM.txt', 'Resultats_impulse.txt']

			for fileToDelete in listOfFileToDelete:
				os.remove(os.path.join(self.working_directorypath, fileToDelete))

			if(message_copied):
				listOfFileToDelete2 = ['messageImpulsePhase1.mess','messageImpulsePhase2.mess']
				for fileToDelete in listOfFileToDelete2:
					os.remove(os.path.join(self.messagespath, fileToDelete))

		if(self.isOK == 0):

			# Delete files of the sutdy (mx, mesh, message, res.med...etc)
			listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
							'clamps_properties.txt', 'sleeperDistance.csv',
							'unitCell.med', 'unitCellWithClamps.med']
			for fileToDelete in listOfFileToDelete:
				os.remove(os.path.join(self.working_directorypath, fileToDelete))
			
			# removing directory
			shutil.rmtree(self.resultsDirectoryPath)






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



class NewPadMeshDialog(QDialog):
	"""New Pad Mesh dialog."""
	def __init__(self, uiPath):
		super(NewPadMeshDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New mesh selection')
		self.browseNewMeshButton.clicked.connect(self.MeshDownload)
		self.addMeshButton.clicked.connect(self.AddNewMesh)
		self.cancelButton.clicked.connect(self.Cancel)
  
	def MeshDownload(self):
		self.newMesh = QFileDialog.getOpenFileName(self, "Open Med File",os.getcwd())

	def AddNewMesh(self):
		
		self.newMeshDirectoryName = self.newMeshName.text()
		self.newMeshDirectoryPath = os.path.join(os.getcwd(),'meshes/Pads')
         
         # Create user folders for new mesh
		os.mkdir(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName))
		mesh_path_separated = self.newMesh[0].split(os.sep)
		src = self.newMesh[0]
		dst = os.path.join(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName),mesh_path_separated[-1])
		shutil.copyfile(src, dst)
		self.accept()

	def Cancel(self):
		self.close()



class NewSleeperMeshDialog(QDialog):
	"""New Sleeper Mesh dialog."""
	def __init__(self, uiPath):
		super(NewSleeperMeshDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New mesh selection')
		self.browseNewMeshButton.clicked.connect(self.MeshDownload)
		self.addMeshButton.clicked.connect(self.AddNewMesh)
		self.cancelButton.clicked.connect(self.Cancel)
  
	def MeshDownload(self):
		self.newMesh = QFileDialog.getOpenFileName(self, "Open Med File",os.getcwd())

	def AddNewMesh(self):
		
		self.newMeshDirectoryName = self.newMeshName.text()
		self.newMeshDirectoryPath = os.path.join(os.getcwd(),'meshes/Sleepers')
         
         # Create user folders for new mesh
		os.mkdir(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName))
		mesh_path_separated = self.newMesh[0].split(os.sep)
		src = self.newMesh[0]
		dst = os.path.join(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName),mesh_path_separated[-1])
		shutil.copyfile(src, dst)
		self.accept()

	def Cancel(self):
		self.close()



class NewRailMeshDialog(QDialog):
	"""New Rail Mesh dialog."""
	def __init__(self, uiPath):
		super(NewRailMeshDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New mesh selection')
		self.browseNewMeshButton.clicked.connect(self.MeshDownload)
		self.addMeshButton.clicked.connect(self.AddNewMesh)
		self.cancelButton.clicked.connect(self.Cancel)
  
	def MeshDownload(self):
		self.newMesh = QFileDialog.getOpenFileName(self, "Open Med File",os.getcwd())

	def AddNewMesh(self):
		
		self.newMeshDirectoryName = self.newMeshName.text()
		self.newMeshDirectoryPath = os.path.join(os.getcwd(),'meshes/Rails')
         
         # Create user folders for new mesh
		os.mkdir(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName))
		mesh_path_separated = self.newMesh[0].split(os.sep)
		src = self.newMesh[0]
		dst = os.path.join(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName),mesh_path_separated[-1])
		shutil.copyfile(src, dst)
		self.accept()

	def Cancel(self):
		self.close()



class NewBallastMeshDialog(QDialog):
	"""New BallastMesh dialog."""
	def __init__(self, uiPath):
		super(NewBallastMeshDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New mesh selection')
		self.browseNewMeshButton.clicked.connect(self.MeshDownload)
		self.addMeshButton.clicked.connect(self.AddNewMesh)
		self.cancelButton.clicked.connect(self.Cancel)
  
	def MeshDownload(self):
		self.newMesh = QFileDialog.getOpenFileName(self, "Open Med File",os.getcwd())

	def AddNewMesh(self):
		
		self.newMeshDirectoryName = self.newMeshName.text()
		self.newMeshDirectoryPath = os.path.join(os.getcwd(),'meshes/Ballast')
         
         # Create user folders for new mesh
		os.mkdir(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName))
		mesh_path_separated = self.newMesh[0].split(os.sep)
		src = self.newMesh[0]
		dst = os.path.join(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName),mesh_path_separated[-1])
		shutil.copyfile(src, dst)
		self.accept()

	def Cancel(self):
		self.close()




class NewPadMaterialDialog(QDialog):
	"""New Pad Material dialog."""
	def __init__(self, uiPath):
		super(NewPadMaterialDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New material selection')
		self.newModulusButton.clicked.connect(self.EDownload)
		self.newKButton.clicked.connect(self.KDownload)
		self.newGButton.clicked.connect(self.GDownload)
		self.newTauButton.clicked.connect(self.tauDownload)
		self.addMaterialButton.clicked.connect(self.AddNewMaterial)
		self.cancelButton.clicked.connect(self.Cancel)
  
	def EDownload(self):
		self.newModulus = QFileDialog.getOpenFileName(self, "Open csv File",os.getcwd())

	def KDownload(self):
		self.newK = QFileDialog.getOpenFileName(self, "Open csv File",os.getcwd())
		
	def GDownload(self):
		self.newG = QFileDialog.getOpenFileName(self, "Open csv File",os.getcwd())
		
	def tauDownload(self):
		self.newtau = QFileDialog.getOpenFileName(self, "Open csv File",os.getcwd())

	def AddNewMaterial(self):
		
		self.newMaterialDirectoryName = self.newMaterialName.text()
		self.newMaterialDirectoryPath = os.path.join(os.getcwd(),'materials/Pad')
         
         # Create user folders for new material
		os.mkdir(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName))
  
         # Copy Modulus data
		modulus_path_separated = self.newModulus[0].split(os.sep)
		src = self.newModulus[0]
		dst = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),modulus_path_separated[-1])
		shutil.copyfile(src, dst)
		# Change name modulus data
		destinationFileOldName = dst
		destinationFileNewName = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName), 'E.csv')
		os.rename(destinationFileOldName, destinationFileNewName)

		# Copy K data
		K_path_separated = self.newK[0].split(os.sep)
		src = self.newK[0]
		dst = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),K_path_separated[-1])
		shutil.copyfile(src, dst)
		# Change name modulus data
		destinationFileOldName = dst
		destinationFileNewName = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName), 'K.csv')
		os.rename(destinationFileOldName, destinationFileNewName)
		
		# Copy G data
		G_path_separated = self.newG[0].split(os.sep)
		src = self.newG[0]
		dst = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),G_path_separated[-1])
		shutil.copyfile(src, dst)
		# Change name modulus data
		destinationFileOldName = dst
		destinationFileNewName = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName), 'G.csv')
		os.rename(destinationFileOldName, destinationFileNewName)
		
		# Copy tau data
		tau_path_separated = self.newtau[0].split(os.sep)
		src = self.newtau[0]
		dst = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),tau_path_separated[-1])
		shutil.copyfile(src, dst)
		# Change name modulus data
		destinationFileOldName = dst
		destinationFileNewName = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName), 'tau.csv')
		os.rename(destinationFileOldName, destinationFileNewName)
  
		# Add poisson ratio
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'poisson.csv'),'w') as fp:
			fp.write(self.newMaterialPoisson.text())

		# Add density
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'density.csv'),'w') as fp:
			fp.write(self.newMaterialDensity.text())

		self.accept()

	def Cancel(self):
		self.close()


class NewSleeperMaterialDialog(QDialog):
	"""New Sleeper Material dialog."""
	def __init__(self, uiPath):
		super(NewSleeperMaterialDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New material selection')
		self.addMaterialButton.clicked.connect(self.AddNewMaterial)
		self.cancelButton.clicked.connect(self.Cancel)

	def AddNewMaterial(self):
		
		self.newMaterialDirectoryName = self.newMaterialName.text()
		self.newMaterialDirectoryPath = os.path.join(os.getcwd(),'materials/Sleeper')
         
         # Create user folders for new material
		os.mkdir(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName))
  
		# Add Young Modulus
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'sleeper_E.csv'),'w') as fp:
			fp.write(self.newMaterialModulus.text())
  
		# Add Hysteretic damping
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'sleeper_AmHyst.csv'),'w') as fp:
			fp.write(self.newMaterialDamp.text())
  
		# Add poisson ratio
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'sleeper_Nu.csv'),'w') as fp:
			fp.write(self.newMaterialPoisson.text())

		# Add density
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'sleeper_Rho.csv'),'w') as fp:
			fp.write(self.newMaterialDensity.text())

		self.accept()

	def Cancel(self):
		self.close()


class NewRailMaterialDialog(QDialog):
	"""New Rail Material dialog."""
	def __init__(self, uiPath):
		super(NewRailMaterialDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New material selection')
		self.addMaterialButton.clicked.connect(self.AddNewMaterial)
		self.cancelButton.clicked.connect(self.Cancel)

	def AddNewMaterial(self):
		
		self.newMaterialDirectoryName = self.newMaterialName.text()
		self.newMaterialDirectoryPath = os.path.join(os.getcwd(),'materials/Rail')
         
         # Create user folders for new material
		os.mkdir(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName))
  
		# Add Young Modulus
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'rail_E.csv'),'w') as fp:
			fp.write(self.newMaterialModulus.text())
  
		# Add Hysteretic damping
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'rail_AmHyst.csv'),'w') as fp:
			fp.write(self.newMaterialDamp.text())
  
		# Add poisson ratio
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'rail_Nu.csv'),'w') as fp:
			fp.write(self.newMaterialPoisson.text())

		# Add density
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'rail_Rho.csv'),'w') as fp:
			fp.write(self.newMaterialDensity.text())

		self.accept()

	def Cancel(self):
		self.close()


class NewBallastMaterialDialog(QDialog):
	"""New Ballast Material dialog."""
	def __init__(self, uiPath):
		super(NewBallastMaterialDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New material selection')
		self.addMaterialButton.clicked.connect(self.AddNewMaterial)
		self.cancelButton.clicked.connect(self.Cancel)

	def AddNewMaterial(self):
		
		self.newMaterialDirectoryName = self.newMaterialName.text()
		self.newMaterialDirectoryPath = os.path.join(os.getcwd(),'materials/Ballast')
         
         # Create user folders for new material
		os.mkdir(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName))
  
		# Add Young Modulus
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'ballast_E.csv'),'w') as fp:
			fp.write(self.newMaterialModulus.text())
  
		# Add Hysteretic damping
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'ballast_AmHyst.csv'),'w') as fp:
			fp.write(self.newMaterialDamp.text())
  
		# Add poisson ratio
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'ballast_Nu.csv'),'w') as fp:
			fp.write(self.newMaterialPoisson.text())

		# Add density
		with open(os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),'ballast_Rho.csv'),'w') as fp:
			fp.write(self.newMaterialDensity.text())

		self.accept()

	def Cancel(self):
		self.close()




if __name__ == '__main__':
	app = QApplication([]) #sys.argv
	widget = ImpulseModelGUI()
	widget.show()
	sys.exit(app.exec_())
