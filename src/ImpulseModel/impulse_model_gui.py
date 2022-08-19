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
		self.materialspath=os.path.join(filepath,'materials')
		self.meshespath=os.path.join(filepath,'meshes')
		uiFilePath=os.path.join(filepath,'impulse_model_gui.ui')
		loadUi(uiFilePath, self)
		self.setWindowTitle('Impulse Model')
		
		
		# Attributes
         # mesh list
		materials_list = os.listdir(self.materialspath)
		# adding list of items to combo box
		self.padMaterial1.addItems(materials_list)
		self.padMaterial2.addItems(materials_list)
  
		mesh_list = os.listdir(self.meshespath)
         # adding list of items to combo box
		self.padMeshes.addItems(mesh_list)


         #get selected material 1 & 2
		self.currentMaterial1 = str(self.padMaterial1.currentText())
 		self.currentMaterial2 = str(self.padMaterial2.currentText())
		# Set the value of the density and poisson ratio
		# and Update value when material is changed
		self.DisplayMX1(self.currentMaterial1)
		self.DisplayMX2(self.currentMaterial2)
		self.padMaterial1.currentTextChanged.connect(self.DisplayMX1)
		self.padMaterial2.currentTextChanged.connect(self.DisplayMX2)
		
  
         # Signals & slots
		self.newMeshButton.clicked.connect(self.NewMesh)
		self.newMaterialButton.clicked.connect(self.NewMaterial)
		self.runButton.clicked.connect(self.Run)
		
  
		# Create a slot for launching the employee dialog
	def NewMesh(self):
		"""Launch the new mesh dialog."""
		uiPath = os.path.join(os.getcwd(),'new_mesh_dialog.ui')
		dlg = NewMeshDialog(uiPath)
		dlg.show()
		self.newMeshFile = dlg.exec_()
		if(self.newMeshFile == 1):
			self.padMeshes.clear()
			mesh_list = os.listdir(self.meshespath)
			# adding list of items to combo box
			self.padMeshes.addItems(mesh_list)

	def NewMaterial(self):
		"""Launch the new material dialog."""
		uiPath = os.path.join(os.getcwd(),'new_material_dialog.ui')
		dlg = NewMaterialDialog(uiPath)
		dlg.show()
		self.newMaterialFile = dlg.exec_()
		if(self.newMaterialFile == 1):
			self.padMaterial1.clear()
			self.padMaterial2.clear()
			materials_list = os.listdir(self.materialspath)
			# adding list of items to combo box
			self.padMaterial1.addItems(materials_list)
			self.padMaterial2.addItems(materials_list)
			self.DisplayMX1(self.currentMaterial1)
			self.DisplayMX2(self.currentMaterial2)

	def DisplayMX1(self, value):

		if(type(value) == type("EVA") or type(value) == type(u'EVA')):
 	       	 #get selected material 1
			#currentMaterial1 = str(self.padMaterial1.currentText())
			#get poisson ratio and density for the selected material
			with open(os.path.join(self.materialspath, value + '/poisson.csv')) as fp:
				Lines = fp.readlines()
				self.poissonRatioMX1 = Lines[0]
			with open(os.path.join(self.materialspath, value + '/density.csv')) as fp:
				Lines = fp.readlines()
				self.densityMX1 = Lines[0]
   
			# Set the value of the density and poisson ratio
			self.poissonRatio1.setText(self.poissonRatioMX1)
			self.density1.setText(self.densityMX1)
		
	def DisplayMX2(self, value):

		if(type(value) == type("EVA") or type(value) == type(u'EVA')):
  	       #get selected material 1 & 2
			#currentMaterial2 = str(self.padMaterial2.currentText())
			#get poisson ratio and density for the selected material
			with open(os.path.join(self.materialspath, value + '/poisson.csv')) as fp:
				Lines = fp.readlines()
				self.poissonRatioMX2 = Lines[0]
			with open(os.path.join(self.materialspath, value + '/density.csv')) as fp:
				Lines = fp.readlines()
				self.densityMX2 = Lines[0]
   
			# Set the value of the density and poisson ratio
			self.poissonRatio2.setText(self.poissonRatioMX2)
			self.density2.setText(self.densityMX2)



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
		src = os.path.join(self.materialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'E.csv'
		fileNewName = 'E_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# G1
		src = os.path.join(self.materialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'G.csv'
		fileNewName = 'G_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# K1
		src = os.path.join(self.materialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'K.csv'
		fileNewName = 'K_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# tau1
		src = os.path.join(self.materialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'tau.csv'
		fileNewName = 'tau_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# Poisson's Ratio1
		src = os.path.join(self.materialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'poisson.csv'
		fileNewName = 'poisson_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# Density1
		src = os.path.join(self.materialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'density.csv'
		fileNewName = 'density_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)



	def Run(self):
     
		self.resultsDirectoryName = self.nameSimu.text()
		self.resultsDirectoryPath = os.path.join(self.pathWorkingDirectory.text(), self.resultsDirectoryName)
         
         # Create user folders for results
		os.mkdir(self.resultsDirectoryPath)
		os.mkdir(os.path.join(self.resultsDirectoryPath,'med_files'))
		os.mkdir(os.path.join(self.resultsDirectoryPath,'results_files'))
		os.mkdir(os.path.join(self.resultsDirectoryPath,'message_files'))
		# Create a file for the study parameters
		with open(os.path.join(self.resultsDirectoryPath,'study_parameters.txt'),'a+') as fp:
			fp.write('Here are the parameters selected for the sutdy: ' + self.resultsDirectoryName + '\n\n')

		# Moving the mesh file in WD
		src = os.path.join(self.meshespath, self.padMeshes.currentText())
		dst = self.working_directorypath
		fileOldName = os.listdir(src)[0]
		fileNewName = 'importedPad.mesh.med'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# Add info in the file of parameters
		with open(os.path.join(self.resultsDirectoryPath,'study_parameters.txt'),'a') as fp:
			fp.write('The selected mesh is: ' + self.padMeshes.currentText() + '\n\n')

		# Moving the materials files in WD
		self.MoveFilesMX(1)
		# Add info in the file of parameters
		with open(os.path.join(self.resultsDirectoryPath,'study_parameters.txt'),'a') as fp:
			fp.write('The selected material 1 is: ' + self.padMaterial1.currentText() + '\n')
			fp.write('The poisson\'s ratio of material 1 is: ' + self.poissonRatio1.text())
			fp.write('The density of material 1 in [t/mm3] is: ' + self.density1.text() + '\n')
		self.MoveFilesMX(2)
		# Add info in the file of parameters
		with open(os.path.join(self.resultsDirectoryPath,'study_parameters.txt'),'a') as fp:
			fp.write('The selected material 2 is: ' + self.padMaterial2.currentText() + '\n')
			fp.write('The poisson\'s ratio of material 2 is: ' + self.poissonRatio2.text())
			fp.write('The density of material 2 in [t/mm3] is: ' + self.density2.text() + '\n')

		# Run the script in salome for 0D element from importPad to padWithRF
		os.system('cd working_directory \n ./gen3SleepersMesh.sh')

		# Run phase I
		os.system('cd working_directory \n ./runImpulsePhase1.sh')

		# Run phase II
		os.system('cd working_directory \n ./runImpulsePhase2.sh')


		# Copy messages in User folder
		listOfFile = ['messageImpulsePhase1.mess','messageImpulsePhase2.mess']
		src = self.messagespath
		dst = os.path.join(self.resultsDirectoryPath,'message_files')
		for fileName in listOfFile:
			self.MoveOnly(src, dst, fileName)
		# Copy med results in User folder
		listOfFile = ['resultImpulse.res.med']
		src = self.working_directorypath
		dst = os.path.join(self.resultsDirectoryPath,'med_files')
		for fileName in listOfFile:
			self.MoveOnly(src, dst, fileName)
		# Copy impulse results in User folder
		listOfFile = ['Resultats_ballast_impulse_INVAR.txt', 'Resultats_ballast_impulse_SGIM.txt', 'Resultats_impulse.txt']
		src = self.working_directorypath
		dst = os.path.join(self.resultsDirectoryPath,'results_files')
		for fileName in listOfFile:
			self.MoveOnly(src, dst, fileName)
		## Concat in one file
		#self.ConcatStiffness()


		# Delete files of the sutdy (mx, freq, mesh, message, res.med...etc)
		listOfFileToDelete = ['resultImpulse.res.med', 
                        'Resultats_ballast_impulse_INVAR.txt', 'Resultats_ballast_impulse_SGIM.txt', 'Resultats_impulse.txt',
                        'E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
                        'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
                        'importedPad.mesh.med', 'gen3Sleeper.mesh.med']
		for fileToDelete in listOfFileToDelete:
			os.remove(os.path.join(self.working_directorypath, fileToDelete))
		listOfFileToDelete2 = ['messageImpulsePhase1.mess','messageImpulsePhase2.mess']
		for fileToDelete in listOfFileToDelete2:
			os.remove(os.path.join(self.messagespath, fileToDelete))





         
class NewMeshDialog(QDialog):
	"""New Mesh dialog."""
	def __init__(self, uiPath):
		super(NewMeshDialog, self).__init__()
		loadUi(uiPath, self)
		self.setWindowTitle('New mesh selection')
		self.browseNewMeshButton.clicked.connect(self.MeshDownload)
		self.addMeshButton.clicked.connect(self.AddNewMesh)
		self.cancelButton.clicked.connect(self.Cancel)
  
	def MeshDownload(self):
		self.newMesh = QFileDialog.getOpenFileName(self, "Open Med File",os.getcwd())

	def AddNewMesh(self):
		
		self.newMeshDirectoryName = self.newMeshName.text()
		self.newMeshDirectoryPath = os.path.join(os.getcwd(),'meshes')
         
         # Create user folders for new mesh
		os.mkdir(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName))
		mesh_path_separated = self.newMesh[0].split(os.sep)
		src = self.newMesh[0]
		dst = os.path.join(os.path.join(self.newMeshDirectoryPath,self.newMeshDirectoryName),mesh_path_separated[-1])
		shutil.copyfile(src, dst)
		self.accept()

	def Cancel(self):
		self.close()




class NewMaterialDialog(QDialog):
	"""New Material dialog."""
	def __init__(self, uiPath):
		super(NewMaterialDialog, self).__init__()
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
		self.newMaterialDirectoryPath = os.path.join(os.getcwd(),'materials')
         
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




if __name__ == '__main__':
	app = QApplication([]) #sys.argv
	widget = ImpulseModelGUI()
	widget.show()
	sys.exit(app.exec_())
