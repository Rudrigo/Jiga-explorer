from PyQt5.QtWidgets import QMessageBox, QWidget
from designer.tela_calibra import *
import configparser

class TelaCalibra(QWidget):
    def __init__(self, parent=None):
        super(TelaCalibra, self).__init__(parent)
        self.ui = Ui_FormCalibra()
        self.ui.setupUi(self)

        self.diciTiposCablib = {}
        self.cfg = configparser.ConfigParser()

        self.readTiposCalib()
        self.ui.lineEditNome_1.setText(self.diciTiposCablib['name1'])
        self.ui.lineEditPath_1.setText(self.diciTiposCablib['path1'])
        if self.diciTiposCablib['stat1'] == '1': self.ui.checkBox_1.setChecked(True)

        self.ui.lineEditNome_2.setText(self.diciTiposCablib['name2'])
        self.ui.lineEditPath_2.setText(self.diciTiposCablib['path2'])
        if self.diciTiposCablib['stat2'] == '1': self.ui.checkBox_2.setChecked(True)

        self.ui.lineEditNome_3.setText(self.diciTiposCablib['name3'])
        self.ui.lineEditPath_3.setText(self.diciTiposCablib['path3'])
        if self.diciTiposCablib['stat3'] == '1': self.ui.checkBox_3.setChecked(True)

        self.ui.lineEditNome_4.setText(self.diciTiposCablib['name4'])
        self.ui.lineEditPath_4.setText(self.diciTiposCablib['path4'])
        if self.diciTiposCablib['stat4'] == '1': self.ui.checkBox_4.setChecked(True)

        self.ui.checkBox_1.clicked.connect(lambda: self.clickBoxTiposCalib(self.ui.checkBox_1.isChecked(), "1"))
        self.ui.checkBox_2.clicked.connect(lambda: self.clickBoxTiposCalib(self.ui.checkBox_2.isChecked(), "2"))
        self.ui.checkBox_3.clicked.connect(lambda: self.clickBoxTiposCalib(self.ui.checkBox_3.isChecked(), "3"))
        self.ui.checkBox_4.clicked.connect(lambda: self.clickBoxTiposCalib(self.ui.checkBox_4.isChecked(), "4"))

        self.ui.btnSalvarCalibra.clicked.connect(self.saveParam)

    def displayShow(self):
        self.show()

    def closeEvent(self, event):
        close = QMessageBox()
        close.setIcon(QMessageBox.Question)
        close.setWindowTitle("Confirmar AÇÃO")
        close.setText("Deseja realmente sair desta tela?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        buttonY = close.button(QMessageBox.Yes)
        buttonY.setText("Sim")
        buttonC = close.button(QMessageBox.Cancel)
        buttonC.setText("Não")
        close.exec_()
        if close.clickedButton() == buttonY:
            event.accept()
        else:
            event.ignore()

    def readTiposCalib(self):
        self.cfg.read('config.ini')
        self.diciTiposCablib["name1"] = self.cfg.get('calibracao', 'name1')
        self.diciTiposCablib["path1"] = self.cfg.get('calibracao', 'path1')
        self.diciTiposCablib["stat1"] = self.cfg.get('calibracao', 'stat1')
        self.diciTiposCablib["name2"] = self.cfg.get('calibracao', 'name2')
        self.diciTiposCablib["path2"] = self.cfg.get('calibracao', 'path2')
        self.diciTiposCablib["stat2"] = self.cfg.get('calibracao', 'stat2')
        self.diciTiposCablib["name3"] = self.cfg.get('calibracao', 'name3')
        self.diciTiposCablib["path3"] = self.cfg.get('calibracao', 'path3')
        self.diciTiposCablib["stat3"] = self.cfg.get('calibracao', 'stat3')
        self.diciTiposCablib["name4"] = self.cfg.get('calibracao', 'name4')
        self.diciTiposCablib["path4"] = self.cfg.get('calibracao', 'path4')
        self.diciTiposCablib["stat4"] = self.cfg.get('calibracao', 'stat4')
        return self.diciTiposCablib

    def clickBoxTiposCalib(self, state, ref):
        if state and ref == "1":
            self.diciTiposCablib["stat1"] = '1'
            self.ui.checkBox_1.setChecked(True)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposCablib["stat2"] = '0'
            self.diciTiposCablib["stat3"] = '0'
            self.diciTiposCablib["stat4"] = '0'
        if state and ref == "2":
            self.diciTiposCablib["stat2"] = '1'
            self.ui.checkBox_2.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposCablib["stat1"] = '0'
            self.diciTiposCablib["stat3"] = '0'
            self.diciTiposCablib["stat4"] = '0'
        if state and ref == "3":
            self.diciTiposCablib["stat3"] = '1'
            self.ui.checkBox_3.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposCablib["stat1"] = '0'
            self.diciTiposCablib["stat2"] = '0'
            self.diciTiposCablib["stat4"] = '0'
        if state and ref == "4":
            self.diciTiposCablib["stat4"] = '1'
            self.ui.checkBox_4.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.diciTiposCablib["stat1"] = '0'
            self.diciTiposCablib["stat2"] = '0'
            self.diciTiposCablib["stat3"] = '0'

    def saveParam(self):
        if self.alertSave("Deseja realmente salvar?"):
            self.cfg.set('calibracao', 'name1', self.ui.lineEditNome_1.text())
            self.cfg.set('calibracao', 'path1', self.ui.lineEditPath_1.text())
            self.cfg.set('calibracao', 'stat1', self.diciTiposCablib["stat1"])
            self.cfg.set('calibracao', 'name2', self.ui.lineEditNome_2.text())
            self.cfg.set('calibracao', 'path2', self.ui.lineEditPath_2.text())
            self.cfg.set('calibracao', 'stat2', self.diciTiposCablib["stat2"])
            self.cfg.set('calibracao', 'name3', self.ui.lineEditNome_3.text())
            self.cfg.set('calibracao', 'path3', self.ui.lineEditPath_3.text())
            self.cfg.set('calibracao', 'stat3', self.diciTiposCablib["stat3"])
            self.cfg.set('calibracao', 'name4', self.ui.lineEditNome_4.text())
            self.cfg.set('calibracao', 'path4', self.ui.lineEditPath_4.text())
            self.cfg.set('calibracao', 'stat4', self.diciTiposCablib["stat4"])
            cfgfile = open('config.ini', 'w')
            self.cfg.write(cfgfile, space_around_delimiters=False)
            cfgfile.close()

    def alertSave(self, msg):
        userInfo = QMessageBox()
        userInfo.setIcon(QMessageBox.Question)
        userInfo.setWindowTitle("Confirmar AÇÃO")
        userInfo.setText(msg)
        userInfo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = userInfo.button(QMessageBox.Yes)
        buttonY.setText("Sim")
        buttonN = userInfo.button(QMessageBox.No)
        buttonN.setText("Não")
        userInfo.exec_()
        if userInfo.clickedButton() == buttonY:
            #self.close()
            return True
        elif userInfo.clickedButton() == buttonN:
            return False