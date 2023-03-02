from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
from PyQt5.uic import loadUi
import os
import sys
import shutil

class PadStiffnessModelGUI(QMainWindow):
	def __init__(self):
		# Initialize + load UI
		super(PadStiffnessModelGUI, self).__init__()
		# Set the different path
		filepath=os.getcwd()
		self.working_directorypath=os.path.join(filepath,'working_directory')
		self.messagespath=os.path.join(filepath,'working_directory/messages')
		self.frequenciespath=os.path.join(filepath,'frequencies')
		self.materialspath=os.path.join(filepath,'materials')
		self.meshespath=os.path.join(filepath,'meshes')
		uiFilePath=os.path.join(filepath,'pad_stiffness_model_gui.ui')
		loadUi(uiFilePath, self)
		self.setWindowTitle('Pad Stiffness Model')
		
		
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

	def ConcatStiffness(self):
		
		# Moving the file in WD
		stiffness_dictionary = {"vertical" : [], "around x" : [], "around z" : [], "horizontal" : []}
		for i in range(4):
			with open(os.path.join(self.resultsDirectoryPath,'stiffness_files/Stiffness_b' + str(i+1) + '.txt')) as fp:
				Lines = fp.readlines()
				case = 0
				for line in Lines:
					if(line[0] == 'F'):
						case += 1
						if(i > 0):
							continue
					if(case == 1):
						stiffness_dictionary["vertical"].append(line)
					if(case == 2):
						stiffness_dictionary["around x"].append(line)
					if(case == 3):
						stiffness_dictionary["around z"].append(line)
					if(case == 4):
						stiffness_dictionary["horizontal"].append(line)
		with open(os.path.join(self.resultsDirectoryPath,'stiffness_files/Stiffness.txt'),'a+') as fp:
			for direction in ["vertical","around x","around z","horizontal"]:
				for line in stiffness_dictionary[direction]:
					fp.write(line)





	def MoveFilesMX(self, material=1):
		
		if (material == 1):
			mx = self.padMaterial1.currentText()
   			mx_type = 'hard'
		if (material == 2):
			mx = self.padMaterial2.currentText()
   			mx_type = 'soft'
		# Moving the material1 properties files in WD
		# E1
		src = os.path.join(self.materialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'E.csv'
		fileNewName = 'E_' + mx_type + '.csv'
		self.MoveAndRename(src, dst, fileOldName, fileNewName)
		# TanD1
		src = os.path.join(self.materialspath, mx)
		dst = self.working_directorypath
		fileOldName = 'tanD.csv'
		fileNewName = 'tanD_' + mx_type + '.csv'
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
		if os.path.exists(self.resultsDirectoryPath):
			shutil.rmtree(self.resultsDirectoryPath)

		os.makedirs(self.resultsDirectoryPath)
		os.makedirs(os.path.join(self.resultsDirectoryPath,'med_files'))
		os.makedirs(os.path.join(self.resultsDirectoryPath,'stiffness_files'))
		os.makedirs(os.path.join(self.resultsDirectoryPath,'message_files'))
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

		# Moving the frequencies files in WD
		src = self.frequenciespath
		dst = self.working_directorypath
		fileNames = os.listdir(src)
		for fileName in fileNames:
			self.MoveOnly(src, dst, fileName)

		# Run the script in salome for 0D element from importPad to padWithRF
		os.system('/opt/SalomeMeca/appli_V2019_univ/salome -t ' + self.working_directorypath + '/add_RF_node_to_pad.py')

		# Run phase I
		os.system('cd working_directory \n bash ./runPadStiffnessPhase1.sh')

		# Run phase II
		os.system('cd working_directory \n bash ./runPadStiffnessPhase2.sh')


		# Copy messages in User folder
		listOfFile = ['messagePadStiffnessPhase1.mess', 'messagePadStiffnessPhase2_b1.mess', 'messagePadStiffnessPhase2_b2.mess', 'messagePadStiffnessPhase2_b3.mess', 'messagePadStiffnessPhase2_b4.mess']
		src = self.messagespath
		dst = os.path.join(self.resultsDirectoryPath,'message_files')
		for fileName in listOfFile:
			self.MoveOnly(src, dst, fileName)
		# Copy med results in User folder
		listOfFile = ['resultPadStiffnessPhase2_b1.res.med', 'resultPadStiffnessPhase2_b2.res.med', 'resultPadStiffnessPhase2_b3.res.med', 'resultPadStiffnessPhase2_b4.res.med']
		src = self.working_directorypath
		dst = os.path.join(self.resultsDirectoryPath,'med_files')
		for fileName in listOfFile:
			self.MoveOnly(src, dst, fileName)
		# Copy stiffness results in User folder
		listOfFile = ['Stiffness_b1.txt', 'Stiffness_b2.txt', 'Stiffness_b3.txt', 'Stiffness_b4.txt']
		src = self.working_directorypath
		dst = os.path.join(self.resultsDirectoryPath,'stiffness_files')
		for fileName in listOfFile:
			self.MoveOnly(src, dst, fileName)
		# Concat in one file
		self.ConcatStiffness()
        # Copy static stiffness result in User folder
		listOfFile = ['Static_Stiffness_b1.txt']
		src = self.working_directorypath
		dst = os.path.join(self.resultsDirectoryPath,'stiffness_files')
		for fileName in listOfFile:
			self.MoveAndRename(src, dst, fileName, 'Static_Stiffness.txt')


		# Delete files of the sutdy (mx, freq, mesh, message, res.med...etc)
		listOfFileToDelete = ['resultPadStiffnessPhase2_b1.res.med', 'resultPadStiffnessPhase2_b2.res.med', 'resultPadStiffnessPhase2_b3.res.med', 'resultPadStiffnessPhase2_b4.res.med',
                        'Stiffness_b1.txt', 'Stiffness_b2.txt', 'Stiffness_b3.txt', 'Stiffness_b4.txt',
                        'Static_Stiffness_b1.txt', 'Static_Stiffness_b2.txt', 'Static_Stiffness_b3.txt', 'Static_Stiffness_b4.txt',
                        'E_hard.csv', 'tanD_hard.csv', 'poisson_hard.csv', 'density_hard.csv',
                        'E_soft.csv', 'tanD_soft.csv', 'poisson_soft.csv', 'density_soft.csv',
                        'importedPad.mesh.med', 'padWithRF.mesh.med',
                        'frequencies_b1.txt', 'frequencies_b2.txt', 'frequencies_b3.txt', 'frequencies_b4.txt']
		for fileToDelete in listOfFileToDelete:
			os.remove(os.path.join(self.working_directorypath, fileToDelete))
		listOfFileToDelete2 = ['messagePadStiffnessPhase1.mess', 'messagePadStiffnessPhase2_b1.mess', 'messagePadStiffnessPhase2_b2.mess', 'messagePadStiffnessPhase2_b3.mess', 'messagePadStiffnessPhase2_b4.mess']
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
		self.newTanDButton.clicked.connect(self.TanDDownload)
		self.addMaterialButton.clicked.connect(self.AddNewMaterial)
		self.cancelButton.clicked.connect(self.Cancel)
  
	def EDownload(self):
		self.newModulus = QFileDialog.getOpenFileName(self, "Open csv File",os.getcwd())

	def TanDDownload(self):
		self.newTanD = QFileDialog.getOpenFileName(self, "Open csv File",os.getcwd())

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

		# Copy tanD data
		tanD_path_separated = self.newTanD[0].split(os.sep)
		src = self.newTanD[0]
		dst = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName),tanD_path_separated[-1])
		shutil.copyfile(src, dst)
		# Change name modulus data
		destinationFileOldName = dst
		destinationFileNewName = os.path.join(os.path.join(self.newMaterialDirectoryPath,self.newMaterialDirectoryName), 'tanD.csv')
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
	widget = PadStiffnessModelGUI()
	widget.show()
	sys.exit(app.exec_())
