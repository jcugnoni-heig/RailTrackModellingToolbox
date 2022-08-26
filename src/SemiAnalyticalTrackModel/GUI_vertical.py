# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_vertical_2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from scipy import interpolate
import csv
import numpy as np
import os
import FunctionsVertical as funvert
import FunctionsSleeper
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QGridLayout, QWidget,\
                            QTextEdit, QPushButton, QLabel, QFileDialog, QVBoxLayout
                            
                            
##############################################################################           
# Classes for frequencies
##############################################################################                           
                            
class Frequencies(QWidget):
    
    def __init__(self):
        super(Frequencies, self).__init__()
        self.start = QTextEdit(self)
        self.end = QTextEdit(self)
        self.step = QTextEdit(self)
        self.saveButton = QPushButton("Save")
        self.initUI()
        
    def initUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Start"), 0, 0)
        layout.addWidget(self.start, 1, 0)
        layout.addWidget(QLabel("End"), 0, 1)
        layout.addWidget(self.end, 1, 1)
        layout.addWidget(QLabel("Step"), 0, 2)
        layout.addWidget(self.step, 1, 2)
        layout.addWidget(self.saveButton, 0, 3)
        self.saveButton.clicked.connect(self.save)
        self.setLayout(layout)
        self.setWindowTitle("Define Frequencies")
        self.show()
        
    def save(self):
        print("save frequencies")
        with open("Frequencies.txt", "w") as file:
            file.write("Frequencies [Hz]\n")
            file.write("Start = ")
            startValue = self.start.toPlainText()
            file.write(startValue)
            file.write("\nEnd = ")
            endValue = self.end.toPlainText()
            file.write(endValue)
            file.write("\nStep = ")
            stepValue = self.step.toPlainText()
            file.write(stepValue)
            file.close()
        Param.frequencies = np.arange(int(self.start.toPlainText()),\
                                      int(self.end.toPlainText()),\
                                      int(self.step.toPlainText()))
        print(Param.frequencies)
        self.close()
            

##############################################################################           
# Classes for rail pads 
##############################################################################

class RailPad(QMessageBox):
    
    def __init__(self):
        super(RailPad, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rail Pads Complex Stiffness')
        self.setText('Options: \nDefault \nCustom constant value\nFrequency dependent serie')
        #self.setInformativeText('Options: \nDefault \nCustom \nSerie')
        self.addButton('Default', QMessageBox.YesRole)
        self.addButton('Custom', QMessageBox.YesRole)
        self.addButton('Series', QMessageBox.YesRole)
        self.setDetailedText('Complex Stiffness: \nKp = K(1+i*n) \n\nDefault: \nK = 2000e6 [N/m] \nn = 0.2')                   
        self.buttonClicked.connect(self.popupButton)
        self.show()
    
    def popupButton(self, i):
        print(i.text())
        if i.text() == "Default":
            self.window = DefaultRailPad()
        if i.text() == "Custom":
            self.window = CustomRailPad()
        if i.text() == "Series":
            self.window = SerieRailPad()


class DefaultRailPad(QMessageBox):
    
    def __init__(self):
        super(DefaultRailPad, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('')
        self.setText('Reset rail pad stiffness to default?')
        self.addButton('Yes', QMessageBox.YesRole)
        self.addButton('No', QMessageBox.NoRole)
        self.setDetailedText('Complex Stiffness: \nKp = K(1+i*n) \n\nDefault: \nK = 2000e6 [N/m] \nn = 0.2') 
        self.buttonClicked.connect(self.popupButton)
        self.show()
    
    def popupButton(self, i):
        print(i.text())
        if i.text() == "Yes":
            Param.railPadStiffness = 2000e6*(1+1j*0.2)
            self.close()
        if i.text() == "No":
            self.close()
        

class CustomRailPad(QWidget):
    
    def __init__(self):
        super(CustomRailPad, self).__init__()
        self.stiffness = QTextEdit(self)
        self.damping = QTextEdit(self)
        self.saveButton = QPushButton("Save")
        self.initUI()
        
    def initUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Stiffness [N/m]"), 0, 0)
        layout.addWidget(self.stiffness, 1, 0)
        layout.addWidget(QLabel("Damping [-]"), 0, 1)
        layout.addWidget(self.damping, 1, 1)
        layout.addWidget(self.saveButton, 1, 2)
        self.saveButton.clicked.connect(self.save)
        self.setLayout(layout)
        self.setWindowTitle("Custom constant values")
        self.show()
        
    def save(self):
        print("save custom rail pad")
        Param.railPadStiffness = float(self.stiffness.toPlainText())*(1+1j*float(self.damping.toPlainText()))
        self.close()
            
        
class SerieRailPad(QWidget):
    
    def __init__(self):
        super(SerieRailPad, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.openFileNameDialogCSV()
        
    def openFileNameDialog(self):
        options =  QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _= QFileDialog.getOpenFileName(parent=self,\
                                                 caption="Rail Pads Stiffness Series",\
                                                 directory=os.getcwd(),\
                                                 filter='File (*.txt)', options=options)
        if fileName:
            print("save rail pad series")
            stiffnessReal = np.zeros(len(Param.frequencies))
            stiffnessImag = np.zeros(len(Param.frequencies))
            with open(fileName, "r") as file:
                for l, line in enumerate(file):
                    string = line.split()
                    i = 0
                    if l == 0:
                        pass
                    if l>0 and l<len(Param.frequencies):
                        stiffnessReal[i] = string[1]
                        stiffnessImag[i] = string[2]
                        i+=1
                    if l>=len(Param.frequencies):
                        break
                file.close()
            Param.railPadStiffness = stiffnessReal+1j*stiffnessImag

    def openFileNameDialogCSV(self):
        options =  QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _= QFileDialog.getOpenFileName(parent=self,\
                                                 caption="Rail Pads Stiffness Series",\
                                                 directory=os.getcwd(),\
                                                 filter='File (*.csv)', options=options)                

        """ get all the data """
        with open(fileName, newline='') as file:
            """ check for delimiter"""
            reader = csv.reader(file, delimiter=";" )
            data = list(reader)
            if len(data[0])>=3:
                pass
            else:
                with open(fileName, newline='') as file1:
                    """ check for delimiter"""
                    reader1 = csv.reader(file1, delimiter="," )
                    data = list(reader1)
                
            """ import numeric data"""
            rows=len(data)
            frequency   = np.zeros(rows-1)
            stiffnessVertReal = np.zeros(rows-1)
            stiffnessVertImag = np.zeros(rows-1)
            
            for l, line in enumerate(data):
                if l == 0:
                    continue
                frequency[l-1]   = float(line[0])
                stiffnessVertReal[l-1] = float(line[1])
                stiffnessVertImag[l-1] = float(line[2])
            file.close
                
        """ interpolate """
        # Vertical #
        Param.frequencies = frequency
        stiffnessVertReal_interpolate = interpolate.interp1d(frequency, stiffnessVertReal, fill_value='extrapolate')
        stiffnessVertReal_intp = stiffnessVertReal_interpolate(Param.frequencies)
        
        stiffnessVertImag_interpolate = interpolate.interp1d(frequency, stiffnessVertImag, fill_value='extrapolate')
        stiffnessVertImag_intp = stiffnessVertImag_interpolate(Param.frequencies)
        
        
        Param.railPadStiffness = stiffnessVertReal_intp+1j*stiffnessVertImag_intp
        
        # plt.figure(10)
        # plt.plot(frequency, stiffnessVertReal)
        # plt.plot(Param.frequencies, stiffnessVertReal_intp)
        # plt.title('Interpolation of Railpad real part')
        
        # plt.figure(11)
        # plt.plot(frequency, stiffnessVertImag)
        # plt.plot(Param.frequencies, stiffnessVertImag_intp)
        # plt.title('Interpolation of Railpad imag part')
            
            
##############################################################################           
# Classes for ballast
##############################################################################


class Ballast(QMessageBox):
    
    def __init__(self):
        super(Ballast, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ballast Complex Stiffness')
        self.setText('Options: \nDefault \nCustom constant value\nFrequency dependent serie')
        #self.setInformativeText('Options: \nDefault \nCustom \nSerie')
        self.addButton('Default', QMessageBox.YesRole)
        self.addButton('Custom', QMessageBox.YesRole)
        self.addButton('Serie', QMessageBox.YesRole)
        self.setDetailedText('Complex Stiffness: \nKb = K(1+i*n) \n\nDefault: \nK = 50e6 [Pa/m] \nn = 2.0')
        self.buttonClicked.connect(self.popupButton)
        self.show()
    
    def popupButton(self, i):
        print(i.text())
        if i.text() == "Default":
            self.window = DefaultBallast()
        if i.text() == "Custom":
            self.window = CustomBallast()
        if i.text() == "Serie":
            self.window = SerieBallast()

            
class DefaultBallast(QMessageBox):
    
    def __init__(self):
        super(DefaultBallast, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('')
        self.setText('Reset ballast stiffness to default?')
        self.addButton('Yes', QMessageBox.YesRole)
        self.addButton('No', QMessageBox.NoRole)
        self.setDetailedText('Complex Stiffness: \nKb = K(1+i*n) \n\nDefault: \nK = 50e6 [Pa/m] \nn = 2.0') 
        self.buttonClicked.connect(self.popupButton)
        self.show()
    
    def popupButton(self, i):
        print(i.text())
        if i.text() == "Yes":
            Param.ballastStiffness = 50e6*(1+1j*2.0)
            self.close()
        if i.text() == "No":
            self.close()
            
            
class CustomBallast(QWidget):
    
    def __init__(self):
        super(CustomBallast, self).__init__()
        self.stiffness = QTextEdit(self)
        self.damping = QTextEdit(self)
        self.saveButton = QPushButton("Save")
        self.initUI()
        
    def initUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Stiffness [Pa/m]"), 0, 0)
        layout.addWidget(self.stiffness, 1, 0)
        layout.addWidget(QLabel("Damping [-]"), 0, 1)
        layout.addWidget(self.damping, 1, 1)
        layout.addWidget(self.saveButton, 1, 2)
        self.saveButton.clicked.connect(self.save)
        self.setLayout(layout)
        self.setWindowTitle("Custom constant values")
        self.show()
        
    def save(self):
        print("save custom ballast")
        Param.ballastStiffness = float(self.stiffness.toPlainText())*(1+1j*float(self.damping.toPlainText()))
        self.close()
        
                
class SerieBallast(QWidget):
    
    def __init__(self):
        super(SerieBallast, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.openFileNameDialog()
        
    def openFileNameDialog(self):
        options =  QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _= QFileDialog.getOpenFileName(parent=self,\
                                                 caption="Ballast Stiffness Series",\
                                                 directory=os.getcwd(),\
                                                 filter='File (*.txt)', options=options)
        if fileName:
            print("save ballast serie")
            stiffness = np.zeros(len(Param.frequencies))
            damping = np.zeros(len(Param.frequencies))
            with open(fileName, "r") as file:
                for l, line in enumerate(file):
                    string = line.split()
                    stiffness[l] = string[0]
                    damping[l] = string[1]
            Param.ballastStiffness = stiffness*(1+1j*damping)
            
            
##############################################################################           
# Classes for sleeper
##############################################################################


class Sleeper(QMessageBox):
    
    def __init__(self):
        super(Sleeper, self).__init__()
        self.initUI()

    def initUI(self): 
        self.setWindowTitle('Sleeper Transfer Function')
        self.setText('Sleepers transfer functions at the interface between rail and sleepers\
                     \nFrequency dependent serie')
        self.addButton('Default', QMessageBox.YesRole)
        self.addButton('Generate', QMessageBox.YesRole)
        self.addButton('Import', QMessageBox.YesRole)
        self.setDetailedText("Default: B91 sleeper type supported on default ballast \nGenerate: B91 sleeper type supported on user defined ballast \nImport: User defined sleeper transfer function (Should include ballast/ground support)")
        self.buttonClicked.connect(self.popupButton)
        self.show()
    
    def popupButton(self, i):
        print(i.text())
        if i.text() == "Default":
            self.window = DefaultSleeper()
        if i.text() == "Generate":
            self.window = GenerateSleeper()
        if i.text() == "Import":
            self.window = ImportSleeper()
       
            
class DefaultSleeper(QMessageBox):
    
    def __init__(self):
        super(DefaultSleeper, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('')
        self.setText('Reset sleeper tranfer function to default?')
        self.addButton('Yes', QMessageBox.YesRole)
        self.addButton('No', QMessageBox.NoRole)
        self.setDetailedText('B91 sleeper with pre-defined default ballast \n\nBallast stiffness: Kb = K*(1+i*n) \nK = 50e6 [Pa/m] \nn = 2.0 [-]') 
        self.buttonClicked.connect(self.popupButton)
        self.show()
    
    def popupButton(self, i):
        print(i.text())
        if i.text() == "Yes":
            Param.sleeperTF = 0*Param.frequencies
            """ get all the data """
            with open('B91_mobility.csv', newline='') as f:
                """ check for delimiter"""
                reader = csv.reader(f, delimiter=";" )
                data = list(reader)
                if len(data[0])==3:
                    pass
                else:
                    with open('B91_mobility.csv', newline='') as f1:
                        """ check for delimiter"""
                        reader1 = csv.reader(f1, delimiter="," )
                        data = list(reader1)
                    
                """ import numeric data"""
                rows=len(data)
                frequency   = np.zeros(rows-1)
                sleeperReal = np.zeros(rows-1)
                sleeperImag = np.zeros(rows-1)
                
                for l, line in enumerate(data):
                    if l == 0:
                        continue
                    frequency[l-1]   = float(line[0])
                    sleeperReal[l-1] = float(line[1])
                    sleeperImag[l-1] = float(line[2])
                    
                """ interpolate """
                sleeperReal_interpolate = interpolate.interp1d(frequency, sleeperReal, fill_value='extrapolate')
                sleeperReal_intp = sleeperReal_interpolate(Param.frequencies)
                
                sleeperImag_interpolate = interpolate.interp1d(frequency, sleeperImag, fill_value='extrapolate')
                sleeperImag_intp = sleeperImag_interpolate(Param.frequencies)
                
                Param.sleeperTF = sleeperReal_intp + 1j*sleeperImag_intp
            
                self.close()
        if i.text() == "No":
            self.close()      
        
            
class GenerateSleeper(QMessageBox):
    
    def __init__(self):
        super(GenerateSleeper, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('')
        self.setText('Generate sleeper tranfer function?')
        self.addButton('Yes', QMessageBox.YesRole)
        self.addButton('No', QMessageBox.NoRole)
        self.setDetailedText('B91 sleeper with user defined ballast \n\nBallast stiffness: Kb = K*(1+i*n) \nK = user defined if clicked Ballast \nn = user defined if clicked Ballast') 
        self.buttonClicked.connect(self.popupButton)
        self.show()
    
    def popupButton(self, i):
        print(i.text())
        if i.text() == "Yes":
            Param.sleeperTF = FunctionsSleeper.GenerateTF(Param.frequencies,\
                                                          Param.ballastStiffness) 
        if i.text() == "No":
            self.close()
                
                
class ImportSleeper(QWidget):
    
    def __init__(self):
        super(ImportSleeper, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.openFileNameDialogCSV()
        
    def openFileNameDialog(self):
        options =  QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _= QFileDialog.getOpenFileName(parent=self,\
                                                 caption="Sleeper Transfer Functions Series",\
                                                 directory=os.getcwd(),\
                                                 filter='File (*.txt)', options=options)
        if fileName:
            print("import sleeper serie")
            sleeperReal = np.zeros(len(Param.frequencies))
            sleeperImag = np.zeros(len(Param.frequencies))
            with open(fileName, "r") as file:
                for l, line in enumerate(file):
                    string = line.split()
                    sleeperReal[l] = string[0]
                    sleeperImag[l] = string[1]
            file.close()
            Param.sleeperTF = sleeperReal + 1j*sleeperImag
            self.close()
            
            
    def openFileNameDialogCSV(self):
        options =  QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _= QFileDialog.getOpenFileName(parent=self,\
                                                 caption="Sleeper Transfer Functions Series",\
                                                 directory=os.getcwd(),\
                                                 filter='File (*.csv)', options=options)

        """ get all the data """
        with open(fileName, newline='') as f:
            """ check for delimiter"""
            reader = csv.reader(f, delimiter=";" )
            data = list(reader)
            if len(data[0])==3:
                pass
            else:
                with open(fileName, newline='') as f1:
                    """ check for delimiter"""
                    reader1 = csv.reader(f1, delimiter="," )
                    data = list(reader1)
                
            """ import numeric data"""
            rows=len(data)
            frequency   = np.zeros(rows-1)
            sleeperReal = np.zeros(rows-1)
            sleeperImag = np.zeros(rows-1)
            
            for l, line in enumerate(data):
                if l == 0:
                    continue
                frequency[l-1]   = float(line[0])
                sleeperReal[l-1] = float(line[1])
                sleeperImag[l-1] = float(line[2])
                
        """ interpolate """
        sleeperReal_interpolate = interpolate.interp1d(frequency, sleeperReal, fill_value='extrapolate')
        sleeperReal_intp = sleeperReal_interpolate(Param.frequencies)
        
        sleeperImag_interpolate = interpolate.interp1d(frequency, sleeperImag, fill_value='extrapolate')
        sleeperImag_intp = sleeperImag_interpolate(Param.frequencies)
        
        Param.sleeperTF = sleeperReal_intp + 1j*sleeperImag_intp
        
        # plt.figure(20)
        # plt.plot(frequency, sleeperReal)
        # plt.plot(Param.frequencies, sleeperReal_intp)
        # plt.title('Interpolation of sleeperTF real part')
        
        # plt.figure(21)
        # plt.plot(frequency, sleeperImag)
        # plt.plot(Param.frequencies, sleeperImag_intp)
        # plt.title('Interpolation of sleeperTF imag part')
        self.close()
            
                
                
##############################################################################           
# Classes for simulation name, parameters and run 
##############################################################################


class Name(QWidget):
    def __init__(self):
        super(Name, self).__init__()
        self.text = QTextEdit(self)
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.cancelButton)
        self.setWindowTitle("Set simulation name")
        self.setLayout(layout)
        self.saveButton.clicked.connect(self.Save)
        self.cancelButton.clicked.connect(self.Cancel)
        self.show()
    
    def Save(self):
        Param.name = self.text.toPlainText() 
        print('save')
        self.close()
        
    def Cancel(self):
        self.close()
         
            
class SimuParam():
    def __init__(self):
        self.name = "Default"
        self.frequencies = np.arange(1,2011,10)
        self.railPadStiffness = 2000e6*(1+1j*0.2)
        self.ballastStiffness = 50e6*(1+1j*2.0)
        sleeperReal = np.zeros(len(np.arange(1,2011,10)))
        sleeperImag = np.zeros(len(np.arange(1,2011,10)))
        file = open("Default_B91_Sleeper_Transfer_Function.txt", "r")
        for l, line in enumerate(file):
            if l == 0:
                pass
            else:
                string = line.split()
                sleeperReal[l-1] = string[0]
                sleeperImag[l-1] = string[2]
        file.close()
        self.sleeperTF = sleeperReal + 1j*sleeperImag
        
        
class RunSimulation():
    def __init__(self):
        super(RunSimulation, self).__init__()
        FunctionsVerticalLinus.runSimu(Param.name,\
                                  Param.frequencies,\
                                  Param.railPadStiffness,\
                                  Param.sleeperTF) # ballast stiffness already included in sleeper TF
        #self.window = ShowResults()
        

# class ShowResults(QMainWindow):
#     def __init__(self):
#         super(ShowResults, self).__init__()
#         self.setCentralWidget(Param.name+"_TF.png")
#         self.setCentralWidget(Param.name+"_TDR.png")
#         self.show()
        
        
        
        
##############################################################################           
# Classes for simulation parameters and run simulation
##############################################################################
          

class Ui_MainWindow(QMainWindow):
    
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("Vertical Track Simulator")
        MainWindow.resize(1035, 807)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 160, 371, 391))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("vertical_track.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.Name = QtWidgets.QPushButton(self.centralwidget)
        self.Name.setGeometry(QtCore.QRect(500, 50, 75, 23))
        self.Name.setObjectName("Name")
        self.Freq = QtWidgets.QPushButton(self.centralwidget)
        self.Freq.setGeometry(QtCore.QRect(650, 150, 75, 23))
        self.Freq.setObjectName("Frequencies")
        self.RailPad = QtWidgets.QPushButton(self.centralwidget)
        self.RailPad.setGeometry(QtCore.QRect(650, 250, 75, 23))
        self.RailPad.setObjectName("Rail Pads")
        self.Ballast = QtWidgets.QPushButton(self.centralwidget)
        self.Ballast.setGeometry(QtCore.QRect(650, 450, 75, 23))
        self.Ballast.setObjectName("Ballast")
        self.Sleeper = QtWidgets.QPushButton(self.centralwidget)
        self.Sleeper.setGeometry(QtCore.QRect(650, 350, 75, 23))
        self.Sleeper.setObjectName("Sleepers")
        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(650, 550, 75, 23))
        self.Run.setObjectName("Run")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1035, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEditor = QtWidgets.QMenu(self.menubar)
        self.menuEditor.setObjectName("menuEdit")
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        MainWindow.setStatusBar(self.statusbar)
        
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.triggered.connect(self.FileNew)
        
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.FileOpen)
        
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.triggered.connect(self.FileSave)
        
        self.actionSimulation_Parameters = QtWidgets.QAction(MainWindow)
        self.actionSimulation_Parameters.setObjectName("actionSimulation_Parameters")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuEditor.addAction(self.actionSimulation_Parameters)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEditor.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.Name.clicked.connect(lambda state: self.popupButton2("Name"))
        self.Freq.clicked.connect(lambda state: self.popupButton2("Freq"))
        self.RailPad.clicked.connect(lambda state: self.popupButton2("RailPad"))
        self.Sleeper.clicked.connect(lambda state: self.popupButton2("Sleeper"))
        self.Ballast.clicked.connect(lambda state: self.popupButton2("Ballast"))
        self.Run.clicked.connect(lambda state: self.popupButton2("Run"))
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vertical Track Simulator"))
        self.Name.setText(_translate("MainWindow", "Name"))
        self.Freq.setText(_translate("MainWindow", "Frequencies"))
        self.RailPad.setText(_translate("MainWindow", "Rail Pads"))
        self.Ballast.setText(_translate("MainWindow", "Ballast"))
        self.Sleeper.setText(_translate("MainWindow", "Sleepers"))
        self.Run.setText(_translate("MainWindow", "Run"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEditor.setTitle(_translate("MainWindow", "Edit"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSimulation_Parameters.setText(_translate("MainWindow", "Simulation Parameters"))
        
    def FileNew(self):
        print("new")
        
    def FileOpen(self):
        print("open")
        
    def FileSave(self):
        print("save")
        
           
    def popupButton2(self, i):
       print("pop2")
       if i == "Name":
           self.window = Name()
       if i == "Freq":
           self.window = Frequencies()
       if i == "RailPad":
           self.window = RailPad()
       if i == "Ballast":
           self.window = Ballast()
       if i == "Sleeper":
           self.window = Sleeper()
       if i == "Run":
           funvert.runSimu(Param.name,\
                                  Param.frequencies,\
                                  Param.railPadStiffness,\
                                  Param.sleeperTF) # ballast stiffness already included in sleeper TF
       
     

if __name__ == "__main__":
    import sys
    Param = SimuParam()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

