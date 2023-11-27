#!/usr/bin/python
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QLabel, QPushButton
from PyQt5.uic import loadUi
import os
import sys
import shutil

class LauncherGUI(QMainWindow):
	def __init__(self):
		# Initialize + load UI
		super(LauncherGUI, self).__init__()
		# Set the different path
		self.filepath=os.path.dirname(os.path.abspath(__file__))
		uiFilePath=os.path.join(self.filepath,'RailTrackToolboxLauncher.ui')
		loadUi(uiFilePath, self)
		self.srcpath=os.path.abspath(os.path.join(self.filepath, os.pardir))
		self.termcmd="xterm -hold -e"
		self.salome_path="__path__salome"
  
         # Signals & slots
		self.PadStiffnessBtn.clicked.connect(self.RunPadStiffness)
		self.ThreeSleeperBtn.clicked.connect(self.RunThreeSleeper)
		self.ImpulseModelBtn.clicked.connect(self.RunImpulseModel)
		self.MultiSleeperBtn.clicked.connect(self.RunMultiSleeperModel)
		self.SemiAnalyticalTrackBtn.clicked.connect(self.RunSemiAnalyticalTrack)
		self.SalomeBtn.clicked.connect(self.RunSalome)


	def RunPadStiffness(self):
		"""Launch the PadStiffness model"""
		exe=os.path.join(self.srcpath,'PadStiffnessModel/PadStiffnessGUI.sh')
		cmd=self.termcmd + " " + exe + " &"		
		os.system(cmd)

	def RunThreeSleeper(self):
		"""Launch the ThreeSleeper model"""
		exe=os.path.join(self.srcpath,'ThreeSleeperModel/ThreeSleeperModel/ThreeSleeperModelGUI.sh')
		cmd=self.termcmd + " " + exe + " &"		
		os.system(cmd)

	def RunImpulseModel(self):
		"""Launch the Impulse model"""
		exe=os.path.join(self.srcpath,'ImpulseModel/ImpulseModelGUI.sh')
		cmd=self.termcmd + " " + exe + " &"		
		os.system(cmd)

	def RunMultiSleeperModel(self):
		"""Launch the MultiSleeper model"""
		exe=os.path.join(self.srcpath,'MultiSleeperModel/MultiSleeperModel.sh')
		cmd=self.termcmd + " " + exe + " &"		
		os.system(cmd)

	def RunSemiAnalyticalTrack(self):
		"""Launch the SemiAnalyticalTrack model"""
		exe=os.path.join(self.srcpath,'SemiAnalyticalTrackModel/SemiAnalyticalTrackGUI.sh')
		cmd=self.termcmd + " " + exe + " &"		
		os.system(cmd)

	def RunSalome(self):
		"""Launch the Salome FE Pre - Post"""
		exe=self.salome_path
		cmd=self.termcmd + " " + exe + " &"		
		os.system(cmd)


if __name__ == '__main__':
	app = QApplication([]) #sys.argv
	widget = LauncherGUI()
	widget.show()
	sys.exit(app.exec_())
