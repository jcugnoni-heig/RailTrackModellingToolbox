from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
from PyQt5.uic import loadUi
import os
import sys
import shutil

class RunSingleSimuGUI(QDialog):

    def __init__(self):

        super(RunSingleSimuGUI, self).__init__()
        filepath=os.getcwd()
        self.working_directorypath=os.path.join(filepath,'working_directory')
        uiFilePath=os.path.join(filepath,'GUI_ImpulseModel.ui')
        loadUi(uiFilePath, self)
        self.setWindowTitle('Impulse Model')
        
        self.select_json_button.clicked.connect(self.jsonDownload)
        self.run_button.clicked.connect(self.Run)
        
    def jsonDownload(self):

        json_path = QFileDialog.getOpenFileName(self, "Open Json File",os.getcwd(), "JSON (*.json *.JSON)")
        self.json_path.setText(json_path[0])
        
    def Run(self):

        try:
            json = self.json_path.text()
            if json == "":
                QMessageBox.information(self, 'Error', 'Please select a *.json file.', QMessageBox.Ok,)
                return
        except:
            QMessageBox.information(self, 'Error', 'Please select a *.json file.', QMessageBox.Ok,)
            return
        
        # Launch the impulse model simulation within the image
        os.system("python3 /opt/RailTrackModellingToolbox/src/ImpulseModel/impulse.py " 
                  + json)


if __name__ == '__main__':
    app = QApplication([])
    widget = RunSingleSimuGUI()
    widget.show()
    sys.exit(app.exec_())
