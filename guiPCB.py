from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from designer.tela_pcb import *
import configparser

class TelaPCB(QWidget):
    def __init__(self, parent=None):
        super(TelaPCB, self).__init__(parent)
        self.ui = Ui_Form_PCB()
        self.ui.setupUi(self)

        self.diciTipos = {}
        self.cfg = configparser.ConfigParser()

        self.readTipos()
        self.ui.lineEditNome1.setText(self.diciTipos['name1'])
        self.ui.lineEditPath1.setText(self.diciTipos['path1'])
        self.ui.lineEditNome2.setText(self.diciTipos['name2'])
        self.ui.lineEditPath2.setText(self.diciTipos['path2'])
        self.ui.lineEditNome3.setText(self.diciTipos['name3'])
        self.ui.lineEditPath3.setText(self.diciTipos['path3'])
        self.ui.lineEditNome4.setText(self.diciTipos['name4'])
        self.ui.lineEditPath4.setText(self.diciTipos['path4'])

        self.ui.btnSalvarPCB.clicked.connect(self.saveParam)

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

    def readTipos(self):
        self.cfg.read('config.ini')
        self.diciTipos["name1"] = self.cfg.get('firmware', 'name1')
        self.diciTipos["path1"] = self.cfg.get('firmware', 'path1')
        self.diciTipos["name2"] = self.cfg.get('firmware', 'name2')
        self.diciTipos["path2"] = self.cfg.get('firmware', 'path2')
        self.diciTipos["name3"] = self.cfg.get('firmware', 'name3')
        self.diciTipos["path3"] = self.cfg.get('firmware', 'path3')
        self.diciTipos["name4"] = self.cfg.get('firmware', 'name4')
        self.diciTipos["path4"] = self.cfg.get('firmware', 'path4')
        print(self.diciTipos)
        return self.diciTipos

    def saveParam(self):
        if self.alertSave("Deseja realmente salvar?"):
            #print(self.ui.lineEditPath4.text())
            #print("Save")
            self.cfg.set('firmware', 'name1', self.ui.lineEditNome1.text())
            self.cfg.set('firmware', 'path1', self.ui.lineEditPath1.text())
            self.cfg.set('firmware', 'name2', self.ui.lineEditNome2.text())
            self.cfg.set('firmware', 'path2', self.ui.lineEditPath2.text())
            self.cfg.set('firmware', 'name3', self.ui.lineEditNome3.text())
            self.cfg.set('firmware', 'path3', self.ui.lineEditPath3.text())
            self.cfg.set('firmware', 'name4', self.ui.lineEditNome4.text())
            self.cfg.set('firmware', 'path4', self.ui.lineEditPath4.text())

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