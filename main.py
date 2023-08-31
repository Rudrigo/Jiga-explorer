import gpioControl
import guiPCB
import sys
import guiTeste
import guiConfig
import guiServer
import guiCalibra
import guiConexao
import guiProducao
import guiGravacao
import configparser
from designer.tela1_Jiga import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

class Tela(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnTestePcb.clicked.connect(self.tTeste)
        self.ui.btnGravacao.clicked.connect(self.tGrav)
        self.ui.actionPCB.triggered.connect(self.tPCB)
        self.ui.actionProdu_o.triggered.connect(self.tProducao)
        self.ui.actionCalibra_o.triggered.connect(self.tCalibra)
        self.ui.actionServidor.triggered.connect(self.tServer)
        self.ui.actionConex_o.triggered.connect(self.tConexao)
        self.ui.actionConfigura_o.triggered.connect(self.tConfig)
        self.ui.actionSair.triggered.connect(self.close)

        self.ui.frame.setStyleSheet("border: 0px;")

        self.validaIni()

        self.cmdGpio = gpioControl.GpioAdsControl()
        self.cmdGpio.cmdReleCH1(1, 1, 1)
        self.cmdGpio.cmdReleCH2(1, 1, 1)
        self.cmdGpio.cmdReleIN(1, 1)

    def displayShow(self, msg):
        self.show()

    def closeEvent(self, event):
        close = QMessageBox()
        close.setIcon(QMessageBox.Question)
        close.setWindowTitle("Confirmar AÇÃO")
        close.setText("Deseja realmente sair do sistema?")
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

    def tTeste(self):
        self.telaTeste = guiTeste.TelaTeste()
        self.telaTeste.displayShow()
        self.hide()

    def tGrav(self):
        self.telaGrvacao = guiGravacao.TelaGravacao()
        self.telaGrvacao.displayShow()
        self.hide()

    def tPCB(self):
        self.telaPcb = guiPCB.TelaPCB()
        self.telaPcb.displayShow()

    def tProducao(self):
        self.telaProducao = guiProducao.TelaProducao()
        self.telaProducao.displayShow()

    def tCalibra(self):
        self.telaCalibra = guiCalibra.TelaCalibra()
        self.telaCalibra.displayShow()

    def tConexao(self):
        self.telaConexao = guiConexao.TelaConexao()
        self.telaConexao.displayShow()

    def tConfig(self):
        self.telaConfig = guiConfig.TelaConfig()
        self.telaConfig.displayShow()

    def tServer(self):
        self.telaServer = guiServer.TelaServer()
        self.telaServer.displayShow()

    def validaIni(self):
        cfg = configparser.ConfigParser()
        try:
            cfg.read("config.ini")
            cfg.get('DEFAULT', 'version')
        except configparser.NoOptionError:
            print("Erro: ")
            self.alert("Falha no arquivo Config.ini")

    def alert(self, msg):
        userInfo = QMessageBox.warning(self, "Atenção", msg, QMessageBox.Ok)
        if userInfo == QMessageBox.Ok:
            print("OK Alerta")
            return True


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = Tela()
    tela.displayShow('Principal')
    qt.exec_()




