import serial
import configparser
import serial.tools.list_ports
from designer.tela_config import *
from PyQt5.QtWidgets import QMessageBox, QWidget

class TelaConfig(QWidget):
    def __init__(self, parent=None):
        super(TelaConfig, self).__init__(parent)
        self.ui = Ui_FormConfig()
        self.ui.setupUi(self)

        self.cfg = configparser.ConfigParser()
        self.diciSerial = {}
        self.readData()
        self.verifyChecks()

        self.ui.checkBoxS1.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')
        self.ui.checkBoxS2.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')
        self.ui.checkBoxS3.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')
        self.ui.checkBoxS4.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')

        self.ui.checkBoxS1.clicked.connect(lambda: self.clickBoxS(self.ui.checkBoxS1.isChecked(), "S1"))
        self.ui.checkBoxS2.clicked.connect(lambda: self.clickBoxS(self.ui.checkBoxS2.isChecked(), "S2"))
        self.ui.checkBoxS3.clicked.connect(lambda: self.clickBoxS(self.ui.checkBoxS3.isChecked(), "S3"))
        self.ui.checkBoxS4.clicked.connect(lambda: self.clickBoxS(self.ui.checkBoxS4.isChecked(), "S4"))

        self.ui.btnSalvarConfig.clicked.connect(self.saveParam)
        self.ui.btnAtualizaConfig.clicked.connect(self.serial_ports)

        self.serial_baudrate("S1")
        self.serial_baudrate("S2")
        self.serial_baudrate("S3")
        self.serial_baudrate("S4")

        #self.serial_ports()

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

    def readData(self):
        self.cfg.read('config.ini')
        self.diciSerial["serial1"] = self.cfg.get('serial', 'serial1')
        self.diciSerial["baudrate1"] = self.cfg.get('serial', 'baudrate1')
        self.diciSerial["stat1"] = self.cfg.get('serial', 'stat1')
        self.diciSerial["serial2"] = self.cfg.get('serial', 'serial2')
        self.diciSerial["baudrate2"] = self.cfg.get('serial', 'baudrate2')
        self.diciSerial["stat2"] = self.cfg.get('serial', 'stat2')
        self.diciSerial["serial3"] = self.cfg.get('serial', 'serial3')
        self.diciSerial["baudrate3"] = self.cfg.get('serial', 'baudrate3')
        self.diciSerial["stat3"] = self.cfg.get('serial', 'stat3')
        self.diciSerial["serial4"] = self.cfg.get('serial', 'serial4')
        self.diciSerial["baudrate4"] = self.cfg.get('serial', 'baudrate4')
        self.diciSerial["stat4"] = self.cfg.get('serial', 'stat4')
        print("diciSerial: "+str(self.diciSerial) )
        return self.diciSerial

    def verifyChecks(self):
        if (self.diciSerial["stat1"] == "0"):
            self.ui.checkBoxS1.setChecked(False)
            self.ui.comboBoxS1.setEnabled(False)
            self.ui.comboBoxBaud1.setEnabled(False)
            self.ui.comboBoxS1.addItem(self.diciSerial["serial1"])
            self.ui.comboBoxBaud1.addItem(self.diciSerial["baudrate1"])
        elif (self.diciSerial["stat1"] == "1"):
            self.ui.checkBoxS1.setChecked(True)
            self.ui.comboBoxS1.setEnabled(True)
            self.ui.comboBoxBaud1.setEnabled(True)
            self.ui.comboBoxS1.addItem(self.diciSerial["serial1"])
            self.ui.comboBoxBaud1.addItem(self.diciSerial["baudrate1"])
        if (self.diciSerial["stat2"] == "0"):
            self.ui.checkBoxS2.setChecked(False)
            self.ui.comboBoxS2.setEnabled(False)
            self.ui.comboBoxBaud2.setEnabled(False)
            self.ui.comboBoxS2.addItem(self.diciSerial["serial2"])
            self.ui.comboBoxBaud2.addItem(self.diciSerial["baudrate2"])
        elif (self.diciSerial["stat2"] == "1"):
            self.ui.checkBoxS2.setChecked(True)
            self.ui.comboBoxS2.setEnabled(True)
            self.ui.comboBoxBaud2.setEnabled(True)
            self.ui.comboBoxS2.addItem(self.diciSerial["serial2"])
            self.ui.comboBoxBaud2.addItem(self.diciSerial["baudrate2"])
        if (self.diciSerial["stat3"] == "0"):
            self.ui.checkBoxS3.setChecked(False)
            self.ui.comboBoxS3.setEnabled(False)
            self.ui.comboBoxBaud3.setEnabled(False)
            self.ui.comboBoxS3.addItem(self.diciSerial["serial3"])
            self.ui.comboBoxBaud3.addItem(self.diciSerial["baudrate3"])
        elif (self.diciSerial["stat3"] == "1"):
            self.ui.checkBoxS3.setChecked(True)
            self.ui.comboBoxS3.setEnabled(True)
            self.ui.comboBoxBaud3.setEnabled(True)
            self.ui.comboBoxS3.addItem(self.diciSerial["serial3"])
            self.ui.comboBoxBaud3.addItem(self.diciSerial["baudrate3"])
        if (self.diciSerial["stat4"] == "0"):
            self.ui.checkBoxS4.setChecked(False)
            self.ui.comboBoxS4.setEnabled(False)
            self.ui.comboBoxBaud4.setEnabled(False)
            self.ui.comboBoxS4.addItem(self.diciSerial["serial4"])
            self.ui.comboBoxBaud4.addItem(self.diciSerial["baudrate4"])
        elif (self.diciSerial["stat4"] == "1"):
            self.ui.checkBoxS4.setChecked(True)
            self.ui.comboBoxS4.setEnabled(True)
            self.ui.comboBoxBaud4.setEnabled(True)
            self.ui.comboBoxS4.addItem(self.diciSerial["serial4"])
            self.ui.comboBoxBaud4.addItem(self.diciSerial["baudrate4"])

    def clickBoxS(self, state, ref):
        if state and ref == "S1":
            self.diciSerial["stat1"] = 1
            self.ui.comboBoxS1.setEnabled(True)
            self.ui.comboBoxBaud1.setEnabled(True)
        elif not state and ref == "S1":
            self.diciSerial["stat1"] = 0
            self.ui.comboBoxS1.setEnabled(False)
            self.ui.comboBoxBaud1.setEnabled(False)
        if state and ref == "S2":
            self.diciSerial["stat2"] = 1
            self.ui.comboBoxS2.setEnabled(True)
            self.ui.comboBoxBaud2.setEnabled(True)
        elif not state and ref == "S2":
            self.diciSerial["stat2"] = 0
            self.ui.comboBoxS2.setEnabled(False)
            self.ui.comboBoxBaud2.setEnabled(False)
        if state and ref == "S3":
            self.diciSerial["stat3"] = 1
            self.ui.comboBoxS3.setEnabled(True)
            self.ui.comboBoxBaud3.setEnabled(True)
        elif not state and ref == "S3":
            self.diciSerial["stat3"] = 0
            self.ui.comboBoxS3.setEnabled(False)
            self.ui.comboBoxBaud3.setEnabled(False)
        if state and ref == "S4":
            self.diciSerial["stat4"] = 1
            self.ui.comboBoxS4.setEnabled(True)
            self.ui.comboBoxBaud4.setEnabled(True)
        elif not state and ref == "S4":
            self.diciSerial["stat4"] = 0
            self.ui.comboBoxS4.setEnabled(False)
            self.ui.comboBoxBaud4.setEnabled(False)

    def saveParam(self):
        if self.ui.comboBoxS1.currentText() == self.ui.comboBoxS2.currentText() or self.ui.comboBoxS1.currentText() == self.ui.comboBoxS3.currentText() or self.ui.comboBoxS1.currentText() == self.ui.comboBoxS4.currentText():
            self.alertaSerial("Serial com mesmo nome!")
        elif self.ui.comboBoxS2.currentText() == self.ui.comboBoxS3.currentText() or self.ui.comboBoxS2.currentText() == self.ui.comboBoxS4.currentText():
            self.alertaSerial("Serial com mesmo nome!")
        elif self.ui.comboBoxS3.currentText() == self.ui.comboBoxS4.currentText():
            self.alertaSerial("Serial com mesmo nome!")
        else:
            if self.alertSave("Deseja realmente salvar?"):

                self.cfg.set('serial', 'serial1', self.ui.comboBoxS1.currentText())
                self.cfg.set('serial', 'baudrate1', self.ui.comboBoxBaud1.currentText())
                self.cfg.set('serial', 'stat1', str(self.diciSerial["stat1"]))

                self.cfg.set('serial', 'serial2', self.ui.comboBoxS2.currentText())
                self.cfg.set('serial', 'baudrate2', self.ui.comboBoxBaud2.currentText())
                self.cfg.set('serial', 'stat2', str(self.diciSerial["stat2"]))

                self.cfg.set('serial', 'serial3', self.ui.comboBoxS3.currentText())
                self.cfg.set('serial', 'baudrate3', self.ui.comboBoxBaud3.currentText())
                self.cfg.set('serial', 'stat3', str(self.diciSerial["stat3"]))

                self.cfg.set('serial', 'serial4', self.ui.comboBoxS4.currentText())
                self.cfg.set('serial', 'baudrate4', self.ui.comboBoxBaud4.currentText())
                self.cfg.set('serial', 'stat4', str(self.diciSerial["stat4"]))

                cfgfile = open('config.ini', 'w')
                self.cfg.write(cfgfile, space_around_delimiters=False)
                cfgfile.close()

    def serial_ports(self):
        ports = serial.tools.list_ports.comports()
        self.clearCheckAll()
        for p in ports:
            if self.ui.checkBoxS1.isChecked():
                if not (self.diciSerial["serial1"] == str(p.device)):
                    self.ui.comboBoxS1.addItem(str(p.device))
                    #self.ui.comboBoxS1.addItem("----")
                else:
                    self.ui.comboBoxS1.addItem(self.diciSerial["serial1"])
            if self.ui.checkBoxS2.isChecked():
                if not (self.diciSerial["serial2"] == str(p.device)):
                    self.ui.comboBoxS2.addItem(str(p.device))
                    #self.ui.comboBoxS2.addItem("----")
                else:
                    self.ui.comboBoxS2.addItem(self.diciSerial["serial2"])
            if self.ui.checkBoxS3.isChecked():
                if not (self.diciSerial["serial3"] == str(p.device)):
                    self.ui.comboBoxS3.addItem(str(p.device))
                    #self.ui.comboBoxS3.addItem("----")
                else:
                    self.ui.comboBoxS3.addItem(self.diciSerial["serial3"])
            if self.ui.checkBoxS4.isChecked():
                if not (self.diciSerial["serial4"] == str(p.device)):
                    self.ui.comboBoxS4.addItem(str(p.device))
                    #self.ui.comboBoxS4.addItem("----")
                else:
                    self.ui.comboBoxS4.addItem(self.diciSerial["serial4"])

    def clearCheckAll(self):
        if self.ui.checkBoxS1.isChecked():
            self.ui.comboBoxS1.clear()
        if self.ui.checkBoxS2.isChecked():
            self.ui.comboBoxS2.clear()
        if self.ui.checkBoxS3.isChecked():
            self.ui.comboBoxS3.clear()
        if self.ui.checkBoxS4.isChecked():
            self.ui.comboBoxS4.clear()

    def serial_baudrate(self, ref):
        listBaud = ["921600", "230400", "128000", "115200", "57600", "38400", "9600"]
        if ref == "S1":
            for baud in listBaud:
                    self.ui.comboBoxBaud1.addItem(baud)
        if ref == "S2":
            for baud in listBaud:
                self.ui.comboBoxBaud2.addItem(baud)
        if ref == "S3":
            for baud in listBaud:
                self.ui.comboBoxBaud3.addItem(baud)
        if ref == "S4":
            for baud in listBaud:
                self.ui.comboBoxBaud4.addItem(baud)

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

    def alertaSerial(self, msg):
        userInfo = QMessageBox.warning(self, "Erro!", msg, QMessageBox.Ok)
        if userInfo == QMessageBox.Ok:
            return True

