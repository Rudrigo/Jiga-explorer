import configparser
from designer.tela_conexao import *
from PyQt5.QtWidgets import QMessageBox, QWidget


class TelaConexao(QWidget):
    def __init__(self, parent=None):
        super(TelaConexao, self).__init__(parent)
        self.ui = Ui_FormConexao()
        self.ui.setupUi(self)

        self.diciTiposConexao = {}
        self.cfg = configparser.ConfigParser()

        self.readTiposConex()

        self.ui.lineEditNome_1.setText(self.diciTiposConexao['name1'])
        self.ui.lineEditPath_1.setText(self.diciTiposConexao['path1'])
        if self.diciTiposConexao['stat1'] == '1': self.ui.checkBox_1.setChecked(True)

        self.ui.lineEditNome_2.setText(self.diciTiposConexao['name2'])
        self.ui.lineEditPath_2.setText(self.diciTiposConexao['path2'])
        if self.diciTiposConexao['stat2'] == '1': self.ui.checkBox_2.setChecked(True)

        self.ui.lineEditNome_3.setText(self.diciTiposConexao['name3'])
        self.ui.lineEditPath_3.setText(self.diciTiposConexao['path3'])
        if self.diciTiposConexao['stat3'] == '1': self.ui.checkBox_3.setChecked(True)

        self.ui.lineEditNome_4.setText(self.diciTiposConexao['name4'])
        self.ui.lineEditPath_4.setText(self.diciTiposConexao['path4'])
        if self.diciTiposConexao['stat4'] == '1': self.ui.checkBox_4.setChecked(True)

        self.ui.checkBox_1.clicked.connect(lambda: self.clickBoxTiposConex(self.ui.checkBox_1.isChecked(), "1"))
        self.ui.checkBox_2.clicked.connect(lambda: self.clickBoxTiposConex(self.ui.checkBox_2.isChecked(), "2"))
        self.ui.checkBox_3.clicked.connect(lambda: self.clickBoxTiposConex(self.ui.checkBox_3.isChecked(), "3"))
        self.ui.checkBox_4.clicked.connect(lambda: self.clickBoxTiposConex(self.ui.checkBox_4.isChecked(), "4"))

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

    def readTiposConex(self):
        self.cfg.read('config.ini')
        self.diciTiposConexao["name1"] = self.cfg.get('conexao', 'name1')
        self.diciTiposConexao["path1"] = self.cfg.get('conexao', 'path1')
        self.diciTiposConexao["stat1"] = self.cfg.get('conexao', 'stat1')

        self.diciTiposConexao["name2"] = self.cfg.get('conexao', 'name2')
        self.diciTiposConexao["path2"] = self.cfg.get('conexao', 'path2')
        self.diciTiposConexao["stat2"] = self.cfg.get('conexao', 'stat2')

        self.diciTiposConexao["name3"] = self.cfg.get('conexao', 'name3')
        self.diciTiposConexao["path3"] = self.cfg.get('conexao', 'path3')
        self.diciTiposConexao["stat3"] = self.cfg.get('conexao', 'stat3')

        self.diciTiposConexao["name4"] = self.cfg.get('conexao', 'name4')
        self.diciTiposConexao["path4"] = self.cfg.get('conexao', 'path4')
        self.diciTiposConexao["stat4"] = self.cfg.get('conexao', 'stat4')
        return self.diciTiposConexao

    def clickBoxTiposConex(self, state, ref):
        if state and ref == "1":
            self.diciTiposConexao["stat1"] = '1'
            self.ui.checkBox_1.setChecked(True)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposConexao["stat2"] = '0'
            self.diciTiposConexao["stat3"] = '0'
            self.diciTiposConexao["stat4"] = '0'
        if state and ref == "2":
            self.diciTiposConexao["stat2"] = '1'
            self.ui.checkBox_2.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposConexao["stat1"] = '0'
            self.diciTiposConexao["stat3"] = '0'
            self.diciTiposConexao["stat4"] = '0'
        if state and ref == "3":
            self.diciTiposConexao["stat3"] = '1'
            self.ui.checkBox_3.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_4.setChecked(False)
            self.diciTiposConexao["stat1"] = '0'
            self.diciTiposConexao["stat2"] = '0'
            self.diciTiposConexao["stat4"] = '0'
        if state and ref == "4":
            self.diciTiposConexao["stat4"] = '1'
            self.ui.checkBox_4.setChecked(True)
            self.ui.checkBox_1.setChecked(False)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.diciTiposConexao["stat1"] = '0'
            self.diciTiposConexao["stat2"] = '0'
            self.diciTiposConexao["stat3"] = '0'

    def saveParam(self):
        if self.alertSave("Deseja realmente salvar?"):
            self.cfg.set('conexao', 'name1', self.ui.lineEditNome_1.text())
            self.cfg.set('conexao', 'path1', self.ui.lineEditPath_1.text())
            self.cfg.set('conexao', 'stat1', self.diciTiposConexao["stat1"])
            self.cfg.set('conexao', 'name2', self.ui.lineEditNome_2.text())
            self.cfg.set('conexao', 'path2', self.ui.lineEditPath_2.text())
            self.cfg.set('conexao', 'stat2', self.diciTiposConexao["stat2"])
            self.cfg.set('conexao', 'name3', self.ui.lineEditNome_3.text())
            self.cfg.set('conexao', 'path3', self.ui.lineEditPath_3.text())
            self.cfg.set('conexao', 'stat3', self.diciTiposConexao["stat3"])
            self.cfg.set('conexao', 'name4', self.ui.lineEditNome_4.text())
            self.cfg.set('conexao', 'path4', self.ui.lineEditPath_4.text())
            self.cfg.set('conexao', 'stat4', self.diciTiposConexao["stat4"])
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




