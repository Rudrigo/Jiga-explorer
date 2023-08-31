from designer.tela_producao import *
from PyQt5.QtWidgets import QMessageBox, QWidget
import configparser

class TelaProducao(QWidget):
    def __init__(self, parent=None):
        super(TelaProducao, self).__init__(parent)
        self.ui = Ui_FormProducao()
        self.ui.setupUi(self)

    def displayShow(self):
        self.show()

        self.diciTiposProdu = {}
        self.cfg = configparser.ConfigParser()

        self.readTiposProdu()
        self.ui.lineEditNome_1.setText(self.diciTiposProdu['name1'])
        self.ui.lineEditPath_1.setText(self.diciTiposProdu['path1'])
        if self.diciTiposProdu['stat1'] == '1': self.ui.checkBox_1.setChecked(True)

        self.ui.lineEditNome_2.setText(self.diciTiposProdu['name2'])
        self.ui.lineEditPath_2.setText(self.diciTiposProdu['path2'])
        if self.diciTiposProdu['stat2'] == '1': self.ui.checkBox_2.setChecked(True)

        self.ui.lineEditNome_3.setText(self.diciTiposProdu['name3'])
        self.ui.lineEditPath_3.setText(self.diciTiposProdu['path3'])
        if self.diciTiposProdu['stat3'] == '1': self.ui.checkBox_3.setChecked(True)

        self.ui.lineEditNome_4.setText(self.diciTiposProdu['name4'])
        self.ui.lineEditPath_4.setText(self.diciTiposProdu['path4'])
        if self.diciTiposProdu['stat4'] == '1': self.ui.checkBox_4.setChecked(True)

        self.ui.checkBox_1.clicked.connect(lambda: self.clickBoxTiposProdu(self.ui.checkBox_1.isChecked(), "1"))
        self.ui.checkBox_2.clicked.connect(lambda: self.clickBoxTiposProdu(self.ui.checkBox_2.isChecked(), "2"))
        self.ui.checkBox_3.clicked.connect(lambda: self.clickBoxTiposProdu(self.ui.checkBox_3.isChecked(), "3"))
        self.ui.checkBox_4.clicked.connect(lambda: self.clickBoxTiposProdu(self.ui.checkBox_4.isChecked(), "4"))

        self.ui.btnSalvarProducao.clicked.connect(self.saveParam)

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

    def readTiposProdu(self):
        self.cfg.read('config.ini')
        self.diciTiposProdu["name1"] = self.cfg.get('producao', 'name1')
        self.diciTiposProdu["path1"] = self.cfg.get('producao', 'path1')
        self.diciTiposProdu["stat1"] = self.cfg.get('producao', 'stat1')
        self.diciTiposProdu["name2"] = self.cfg.get('producao', 'name2')
        self.diciTiposProdu["path2"] = self.cfg.get('producao', 'path2')
        self.diciTiposProdu["stat2"] = self.cfg.get('producao', 'stat2')
        self.diciTiposProdu["name3"] = self.cfg.get('producao', 'name3')
        self.diciTiposProdu["path3"] = self.cfg.get('producao', 'path3')
        self.diciTiposProdu["stat3"] = self.cfg.get('producao', 'stat3')
        self.diciTiposProdu["name4"] = self.cfg.get('producao', 'name4')
        self.diciTiposProdu["path4"] = self.cfg.get('producao', 'path4')
        self.diciTiposProdu["stat4"] = self.cfg.get('producao', 'stat4')
        return self.diciTiposProdu

    def clickBoxTiposProdu(self, state, ref):
        if state and ref == "1":
            self.diciTiposProdu["stat1"] = '1'
            self.ui.checkBox_1.setChecked(True)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposProdu["stat2"] = '0'
            self.diciTiposProdu["stat3"] = '0'
            self.diciTiposProdu["stat4"] = '0'
        if state and ref == "2":
            self.diciTiposProdu["stat2"] = '1'
            self.ui.checkBox_2.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposProdu["stat1"] = '0'
            self.diciTiposProdu["stat3"] = '0'
            self.diciTiposProdu["stat4"] = '0'
        if state and ref == "3":
            self.diciTiposProdu["stat3"] = '1'
            self.ui.checkBox_3.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposProdu["stat1"] = '0'
            self.diciTiposProdu["stat2"] = '0'
            self.diciTiposProdu["stat4"] = '0'
        if state and ref == "4":
            self.diciTiposProdu["stat4"] = '1'
            self.ui.checkBox_4.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.diciTiposProdu["stat1"] = '0'
            self.diciTiposProdu["stat2"] = '0'
            self.diciTiposProdu["stat3"] = '0'

    def saveParam(self):
        if self.alertSave("Deseja realmente salvar?"):
            self.cfg.set('producao', 'name1', self.ui.lineEditNome_1.text())
            self.cfg.set('producao', 'path1', self.ui.lineEditPath_1.text())
            self.cfg.set('producao', 'stat1', self.diciTiposProdu["stat1"])
            self.cfg.set('producao', 'name2', self.ui.lineEditNome_2.text())
            self.cfg.set('producao', 'path2', self.ui.lineEditPath_2.text())
            self.cfg.set('producao', 'stat2', self.diciTiposProdu["stat2"])
            self.cfg.set('producao', 'name3', self.ui.lineEditNome_3.text())
            self.cfg.set('producao', 'path3', self.ui.lineEditPath_3.text())
            self.cfg.set('producao', 'stat3', self.diciTiposProdu["stat3"])
            self.cfg.set('producao', 'name4', self.ui.lineEditNome_4.text())
            self.cfg.set('producao', 'path4', self.ui.lineEditPath_4.text())
            self.cfg.set('producao', 'stat4', self.diciTiposProdu["stat4"])
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