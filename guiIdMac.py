import configparser
from designer.tela_id_mac import *
from PyQt5.QtWidgets import QMessageBox, QWidget

class TelaIdMac(QWidget):
    def __init__(self, *args, **kw):
        super(TelaIdMac, self).__init__()
        self.ui = Ui_FormIdMac()
        self.ui.setupUi(self)

        self.diciSerieNumFile = {}
        self.diciSerieNum = args[0]

        print("self.diciSerieNum ************************")
        print(self.diciSerieNum)

        self.cfg = configparser.ConfigParser()
        self.readSerie()

        self.ui.lineEditMac1.setText(self.diciSerieNumFile["mac1"])
        self.ui.lineEditNSerie1.setText(self.diciSerieNumFile["numero1"])

        self.ui.lineEditMac2.setText(self.diciSerieNumFile["mac2"])
        self.ui.lineEditNSerie2.setText(self.diciSerieNumFile['numero2'])

        self.ui.lineEditMac3.setText(self.diciSerieNumFile["mac3"])
        self.ui.lineEditNSerie3.setText(self.diciSerieNumFile['numero3'])

        self.ui.lineEditMac4.setText(self.diciSerieNumFile["mac4"])
        self.ui.lineEditNSerie4.setText(self.diciSerieNumFile['numero4'])

    def displayShow(self):
        self.show()

    def closeEvent(self, event):
        event.accept()
        """close = QMessageBox()
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
            event.ignore()"""

    def readSerie(self):
        self.cfg.read('config.ini')

        self.diciSerieNumFile["mac1"] = self.cfg.get('numeroserial', 'mac1')
        self.diciSerieNumFile["numero1"] = self.cfg.get('numeroserial', 'numero1')
        #self.ui.lineEditMac1.setText(self.diciSerieNum["mac1"])
        #self.ui.lineEditNSerie1.setText(self.diciSerieNum["numero1"])
        #self.ui.lineEditMac1.setDisabled(True)
        #self.ui.lineEditNSerie1.setDisabled(True)

        self.diciSerieNumFile["mac2"] = self.cfg.get('numeroserial', 'mac2')
        self.diciSerieNumFile["numero2"] = self.cfg.get('numeroserial', 'numero2')
        #self.ui.lineEditMac2.setText(self.diciSerieNum["mac2"])
        #self.ui.lineEditNSerie2.setText(self.diciSerieNum["numero2"])
        #self.ui.lineEditMac2.setDisabled(True)
        #self.ui.lineEditNSerie2.setDisabled(True)

        self.diciSerieNumFile["mac3"] = self.cfg.get('numeroserial', 'mac3')
        self.diciSerieNumFile["numero3"] = self.cfg.get('numeroserial', 'numero3')
        #self.ui.lineEditMac3.setText(self.diciSerieNum["mac3"])
        #self.ui.lineEditNSerie3.setText(self.diciSerieNum["numero3"])
        #self.ui.lineEditMac3.setDisabled(True)
        #self.ui.lineEditNSerie3.setDisabled(True)

        self.diciSerieNumFile["mac4"] = self.cfg.get('numeroserial', 'mac4')
        self.diciSerieNumFile["numero4"] = self.cfg.get('numeroserial', 'numero4')
        #self.ui.lineEditMac4.setText(self.diciSerieNum["mac4"])
        #self.ui.lineEditNSerie4.setText(self.diciSerieNum["numero4"])
        #self.ui.lineEditMac4.setDisabled(True)
        #self.ui.lineEditNSerie4.setDisabled(True)

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
            self.close()
            #return True
        elif userInfo.clickedButton() == buttonN:
            return False




