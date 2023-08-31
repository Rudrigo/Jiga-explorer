from PyQt5.QtWidgets import QMessageBox, QWidget
from designer.tela_server import *
import configparser

class TelaServer(QWidget):
    def __init__(self, parent=None):
        super(TelaServer, self).__init__(parent)
        self.ui = Ui_FormServer()
        self.ui.setupUi(self)

        self.diciTiposServer = {}
        self.cfg = configparser.ConfigParser()
        self.readData()

        self.ui.lineEditServer.setText(self.diciTiposServer['server'])
        self.ui.lineEditPort.setText(self.diciTiposServer["port"])
        self.ui.lineEditQos.setText(self.diciTiposServer["qos"])
        self.ui.lineEditUser.setText(self.diciTiposServer["username"])
        self.ui.lineEditPasswd.setText(self.diciTiposServer["password"])
        self.ui.lineEditTpub.setText(self.diciTiposServer["topicpub"])
        self.ui.lineEditTsub.setText(self.diciTiposServer["topicsub"])

        self.ui.btnSalvarServer.clicked.connect(self.saveData)

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

    def saveData(self):
        if self.alertSave("Deseja realmente salvar?"):
            self.cfg.set('mqtt', 'server', self.ui.lineEditServer.text())
            self.cfg.set('mqtt', 'port', self.ui.lineEditPort.text())
            self.cfg.set('mqtt', 'qos', self.ui.lineEditQos.text())
            self.cfg.set('mqtt', 'username', self.ui.lineEditUser.text())
            self.cfg.set('mqtt', 'password', self.ui.lineEditPasswd.text())
            self.cfg.set('mqtt', 'topicpub', self.ui.lineEditTpub.text())
            self.cfg.set('mqtt', 'topicsub', self.ui.lineEditTsub.text())
            cfgfile = open('config.ini', 'w')
            self.cfg.write(cfgfile, space_around_delimiters=False)
            cfgfile.close()


    def readData(self):
        self.cfg.read('config.ini')
        self.diciTiposServer["server"] = self.cfg.get('mqtt', 'server')
        self.diciTiposServer["port"] = self.cfg.get('mqtt', 'port')
        self.diciTiposServer["qos"] = self.cfg.get('mqtt', 'qos')
        self.diciTiposServer["username"] = self.cfg.get('mqtt', 'username')
        self.diciTiposServer["password"] = self.cfg.get('mqtt', 'password')
        self.diciTiposServer["topicpub"] = self.cfg.get('mqtt', 'topicpub')
        self.diciTiposServer["topicsub"] = self.cfg.get('mqtt', 'topicsub')
        return self.diciTiposServer


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