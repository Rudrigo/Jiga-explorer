import logging
import espFlasher
import guiTeste
import main
import guiIdMac
from PyQt5.QtCore import QThread, pyqtSignal
import configparser
from designer.tela3_Jiga import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import jsonFiles
import commandTest
import gpioControl
from mqttConnect import MqttClient

class WorkerGravPl1(QThread):
    threadSignalPl1 = pyqtSignal(str)
    def __init__(self, parent=None, *args,):
        super(WorkerGravPl1, self).__init__(parent)
        self.is_killed = False
        self.diciParam = args[0]
        self.esp = espFlasher.EspFlasher()
        self.diciNSerial ={}
        logging.basicConfig(filename='log.txt', encoding='utf-8', format = '%(asctime)s %(levelname)-8s %(message)s',level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        self.cmdSerial = commandTest.CommdTest()
        self.cmdGpio = gpioControl.GpioAdsControl()
        self.cmdGpio.cmdReleCH1(1, 1, 1)
        self.cmdGpio.cmdReleIN(0, 1)
        self.macMemo = '0'
        self.mqtt_client = MqttClient(broker=self.diciParam["server"], client_id='201-jiga',
                                      username=self.diciParam["username"], password=self.diciParam["password"])
        self.value = ''
        self.count = 0

    def run(self):
        # Do something...
        if (self.diciParam["placa1"] == True): #------------------------ PLACA 1 --------------------------------------
            logging.debug("Placa 1 ------------------------------")
            if not self.is_killed:
                try:
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Inicia processo de gravação...")

                    self.cmdGpio.cmdReleCH1(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                    QThread.msleep(1000)
                    self.cmdGpio.cmdReleCH1(1, 0, 1)
                    QThread.msleep(1000)
                    self.cmdGpio.cmdReleCH1(0, 0, 0)

                    val = self.esp.readChipInfo(self.diciParam['serial1'], '115200')
                    if val == 0:
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Aguarde a reeconexão serial")
                        QThread.msleep(2000)
                        self.cmdGpio.cmdReleCH1(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                        QThread.msleep(1000)
                        self.cmdGpio.cmdReleCH1(1, 0, 1)
                        QThread.msleep(1000)
                        self.cmdGpio.cmdReleCH1(0, 0, 0)
                        val = self.esp.readChipInfo(self.diciParam['serial1'], '115200')

                    nameFirm = 'Firmware: '+self.diciParam['name4']

                    self.macMemo = val['mac']
                    self.diciNSerial['mac1'] = self.macMemo
                    self.diciParam['mac1'] = self.macMemo
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1] </font> Serial: " + self.diciParam['serial1'] + " Baud: " + self.diciParam['baudrate1'])

                    while(True):
                        self.mqtt_client.connect()
                        self.value = self.mqtt_client.connectGota(self.diciParam, 'mac1', test={})

                        if not self.value == 'ERRO':
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1] </font>MAC: <font color='GreenYellow' size='3'>" +self.diciParam['mac1'] + "</font>")
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1] </font>Serial Number: <font color='GreenYellow' size='3'>" +self.value+ "</font>")
                            self.saveN1Reg(self.diciParam['mac1'], str(self.value))
                            break
                        else:
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1] </font> <font color='red' size='3'>Repetindo consulta ao GOTA!</font>")
                            self.count = self.count+1

                        if self.count == 5:
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1] </font> <font color='red' size='3'>Erro Servidor GOTA!</font>")
                            self.saveN1Reg('0', '0')
                            self.count = 0
                            break

                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> " + nameFirm)

                    logging.info("MAC placa 1: "+self.macMemo)
                    logging.info(nameFirm)

                except:
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> USB Sem conexão - Placa 1 <font color='red' size='3'>[ERRO]</font>")
                    self.is_killed = True

            if not self.is_killed:  # GRAVANDO 1º BLOCO DE FIRMWARE (BOOT-LOAD)
                print(self.diciParam)
                self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Gravando firmware de teste")
                result = self.esp.writeFirmwareMult(self.diciParam['serial1'], self.diciParam['baudrate1'],
                                                    self.diciParam['mem1'], self.diciParam['path1'],
                                                    self.diciParam['mem2'], self.diciParam['path2'],
                                                    self.diciParam['mem3'], self.diciParam['path3'])
                for i in result.split(';'):
                    if i == '0':
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Gravação bootload <font color='white' size='3'>[OK]</font>")
                        logging.info("Gravação bootload placa 1 [OK]")

                    if i == '2':
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> "+result)
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Erro de gravação bootload <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação bootload placa 1 [ERRO]")
                            self.is_killed = True

            if not self.is_killed: # GRAVANDO 2º BLOCO DE FIRMWARE (TESTE)

                QThread.msleep(500)
                self.cmdGpio.cmdReleCH1(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(2000)
                self.cmdGpio.cmdReleCH1(1, 0, 1)
                QThread.msleep(2000)
                self.cmdGpio.cmdReleCH1(0, 0, 0)

                result1 = self.esp.writeFirmwareOne(self.diciParam['serial1'], self.diciParam['baudrate1'],
                                                        self.diciParam['mem4'], self.diciParam['path4'])
                for i in result1.split(';'):
                    if i == '0':
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Gravação firmware <font color='white' size='3'>[OK]</font>")
                        logging.info("Gravação firmware placa 1 [OK]")

                    if i == '2':
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> "+result1)
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Erro de gravação firmware <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação firmware placa 1 [ERRO]")
                            self.is_killed = True
                print(result1)

        if self.is_killed:
            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font><font color='red' size='3'> Processo finalizado!</font>\r\n")
            logging.info("Processo interrompido [INFO]")
            self.cmdGpio.cmdReleCH1(1, 1, 1)
        else:
            print("FIM")
            print(self.diciNSerial)
            print(self.diciNSerial['mac1'])
            self.threadSignalPl1.emit('MAC1;'+self.diciNSerial['mac1'])

            self.cmdGpio.cmdReleCH1(1, 1, 1)
            self.threadSignalPl1.emit("FIM")

    def kill(self):
        self.is_killed = True
        print("Kill True!")

    def saveN1Reg(self, mac, serie):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        cfg.set('numeroserial',  'numero1', serie)
        cfg.set('numeroserial', 'mac1', mac)
        cfgfile = open('config.ini', 'w')
        cfg.write(cfgfile, space_around_delimiters=False)
        cfgfile.close()

class WorkerGravPl2(QThread):
    threadSignalPl2 = pyqtSignal(str)
    def __init__(self, parent=None, *args,):
        super(WorkerGravPl2, self).__init__(parent)
        self.is_killed = False
        self.diciParam = args[0]
        self.esp = espFlasher.EspFlasher()
        self.diciNSerial ={}
        logging.basicConfig(filename='log.txt', encoding='utf-8', format = '%(asctime)s %(levelname)-8s %(message)s',level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        self.cmdSerial = commandTest.CommdTest()
        self.cmdGpio = gpioControl.GpioAdsControl()
        self.cmdGpio.cmdReleCH2(1, 1, 1)
        self.cmdGpio.cmdReleIN(0, 1)
        self.macMemo = '0'
        self.mqtt_client = MqttClient(broker=self.diciParam["server"], client_id='202-jiga',
                                      username=self.diciParam["username"], password=self.diciParam["password"])
        self.value = ''
        self.count = 0

    def run(self):
        # Do something...
        if (self.diciParam["placa2"] == True): #------------------------ PLACA 2 --------------------------------------
            logging.debug("Placa 2 ------------------------------")
            if not self.is_killed:
                try:
                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Inicia processo de gravação......")

                    self.cmdGpio.cmdReleCH2(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                    QThread.msleep(1000)
                    self.cmdGpio.cmdReleCH2(1, 0, 1)
                    QThread.msleep(1000)
                    self.cmdGpio.cmdReleCH2(0, 0, 0)

                    val = self.esp.readChipInfo(self.diciParam['serial2'], '115200')
                    nameFirm = 'Firmware: '+self.diciParam['name4']

                    self.macMemo = val['mac']
                    self.diciNSerial['mac2'] = self.macMemo
                    self.diciParam['mac2'] = self.macMemo

                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Serial: " + self.diciParam['serial2'] + " Baud: " + self.diciParam['baudrate2'])

                    while(True):
                        self.mqtt_client.connect()
                        self.value = self.mqtt_client.connectGota(self.diciParam, 'mac2', test={})
                        if not self.value == 'ERRO':
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> MAC: <font color='GreenYellow' size='3'>" + self.diciParam['mac2'] + "</font>")
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Serial Number: <font color='GreenYellow' size='3'>" + self.value + "</font>")
                            self.saveN2Reg(self.diciParam['mac2'], str(self.value))
                            break
                        else:
                            self.threadSignalPl2.emit( "<font color= 'SlateBlue' size='2'>[PLACA-2]</font> <font color='red' size='3'> Repetindo consulta ao GOTA!</font>")
                            self.count = self.count + 1

                        if self.count == 5:
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> <font color='red' size='3'> Erro Servidor GOTA!</font>")
                            self.saveN2Reg('0', '0')
                            self.count = 0
                            break

                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> " + nameFirm)

                    logging.info("MAC placa 2: "+self.macMemo)
                    logging.info(nameFirm)

                except:
                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> USB Sem conexão - Placa 2 <font color='red' size='3'>[ERRO]</font>")
                    self.is_killed = True

            if not self.is_killed:  # GRAVANDO 1º BLOCO DE FIRMWARE (BOOT-LOAD)

                self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Gravando firmware de teste")
                result = self.esp.writeFirmwareMult(self.diciParam['serial2'], self.diciParam['baudrate2'],
                                                        self.diciParam['mem1'], self.diciParam['path1'], self.diciParam['mem2'],
                                                        self.diciParam['path2'], self.diciParam['mem3'],
                                                        self.diciParam['path3'])
                for i in result.split(';'):
                    if i == '0':
                        self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Gravação bootload <font color='white' size='3'>[OK]</font>")
                        logging.info("Gravação bootload placa 2 [OK]")

                    if i == '2':
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> "+result)
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Erro de gravação bootload <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação bootload placa 2 [ERRO]")
                            self.is_killed = True

            if not self.is_killed: # GRAVANDO 2º BLOCO DE FIRMWARE (TESTE)
                QThread.msleep(500)
                self.cmdGpio.cmdReleCH2(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(2000)
                self.cmdGpio.cmdReleCH2(1, 0, 1)
                QThread.msleep(2000)
                self.cmdGpio.cmdReleCH2(0, 0, 0)

                result1 = self.esp.writeFirmwareOne(self.diciParam['serial2'], self.diciParam['baudrate2'],
                                                        self.diciParam['mem4'], self.diciParam['path4'])
                for i in result1.split(';'):
                    if i == '0':
                        self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Gravação firmware <font color='white' size='3'>[OK]</font>")
                        logging.info("Gravação firmware placa 2 [OK]")

                    if i == '2':
                            self.threadSignalPl2.emit(result1)
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Erro de gravação firmware <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação firmware placa 2 [ERRO]")
                            self.is_killed = True
                print(result1)

        if self.is_killed:
            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font><font color='red' size='3'> Processo finalizado!</font>\r\n")
            logging.info("Processo interrompido [INFO]")
            self.cmdGpio.cmdReleCH2(1, 1, 1)
        else:
            print("FIM")
            print(self.diciNSerial)
            print(self.diciNSerial['mac2'])

            self.threadSignalPl2.emit('MAC2;' + self.diciNSerial['mac2'])

            self.cmdGpio.cmdReleCH2(1, 1, 1)
            self.threadSignalPl2.emit("FIM")

    def kill(self):
        self.is_killed = True
        print("Kill True!")

    def saveN2Reg(self, mac, serie):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        cfg.set('numeroserial',  'numero2', serie)
        cfg.set('numeroserial', 'mac2', mac)
        cfgfile = open('config.ini', 'w')
        cfg.write(cfgfile, space_around_delimiters=False)
        cfgfile.close()

class WorkerGravPl3(QThread):
    threadSignalPl3 = pyqtSignal(str)
    def __init__(self, parent=None, *args,):
        super(WorkerGravPl3, self).__init__(parent)
        self.is_killed = False
        self.diciParam = args[0]
        self.esp = espFlasher.EspFlasher()
        self.diciNSerial ={}
        logging.basicConfig(filename='log.txt', encoding='utf-8', format = '%(asctime)s %(levelname)-8s %(message)s',level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        self.cmdSerial = commandTest.CommdTest()
        self.cmdGpio = gpioControl.GpioAdsControl()
        self.cmdGpio.cmdReleCH1(1, 1, 1)
        self.cmdGpio.cmdReleIN(0, 1)
        self.macMemo = '0'
        self.mqtt_client = MqttClient(broker=self.diciParam["server"], client_id='203-jiga',
                                      username=self.diciParam["username"], password=self.diciParam["password"])
        self.value = ''
        self.count = 0

    def run(self):
        # Do something...
        if (self.diciParam["placa3"] == True): #------------------------ PLACA 3 --------------------------------------
            logging.debug("Placa 3 ------------------------------")
            if not self.is_killed:
                try:

                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Inicia processo de gravação...")

                    self.cmdGpio.cmdReleCH3(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                    QThread.msleep(1000)
                    self.cmdGpio.cmdReleCH3(1, 0, 1)
                    QThread.msleep(1000)
                    self.cmdGpio.cmdReleCH3(0, 0, 0)

                    val = self.esp.readChipInfo(self.diciParam['serial3'], '115200')
                    nameFirm = 'Firmware: '+self.diciParam['name4']

                    self.macMemo = val['mac']
                    self.diciNSerial['mac3'] = self.macMemo
                    self.diciParam['mac3'] = self.macMemo
                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Serial: " + self.diciParam['serial3'] + " Baud: " + self.diciParam['baudrate3'])

                    while(True):
                        self.mqtt_client.connect()
                        self.value = self.mqtt_client.connectGota(self.diciParam, 'mac3', test={})

                        if not self.value == 'ERRO':
                            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> MAC: <font color='GreenYellow' size='3'>" +self.diciParam['mac3'] + "</font>")
                            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Serial Number: <font color='GreenYellow' size='3'>" + self.value + "</font>")
                            self.saveN3Reg(self.diciParam['mac3'], str(self.value))
                            break
                        else:
                            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> <font color='red' size='3'> Repetindo consulta ao GOTA!</font>")
                            self.count = self.count + 1

                        if self.count == 5:
                            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> <font color='red' size='3'> Erro Servidor GOTA!</font>")
                            self.saveN3Reg('0', '0')
                            self.count = 0
                            break

                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> " + nameFirm)

                    logging.info("MAC placa 3: " + self.macMemo)
                    logging.info(nameFirm)
                except:
                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> USB Sem conexão - Placa 3 <font color='red' size='3'>[ERRO]</font>")
                    self.is_killed = True

            if not self.is_killed:  # GRAVANDO 1º BLOCO DE FIRMWARE (BOOT-LOAD)

                self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Gravando firmware de teste")
                result = self.esp.writeFirmwareMult(self.diciParam['serial3'], self.diciParam['baudrate3'],
                                                        self.diciParam['mem1'], self.diciParam['path1'], self.diciParam['mem2'],
                                                        self.diciParam['path2'], self.diciParam['mem3'],
                                                        self.diciParam['path3'])
                for i in result.split(';'):
                    if i == '0':
                        self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Gravação bootload <font color='white' size='3'>[OK]</font>")
                        logging.info("Gravação bootload placa 3 [OK]")

                    if i == '2':
                            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> "+result)
                            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Erro de gravação bootload <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação bootload placa 3 [ERRO]")
                            self.is_killed = True

            if not self.is_killed: # GRAVANDO 2º BLOCO DE FIRMWARE (TESTE)

                QThread.msleep(500)
                self.cmdGpio.cmdReleCH3(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(2000)
                self.cmdGpio.cmdReleCH3(1, 0, 1)
                QThread.msleep(2000)
                self.cmdGpio.cmdReleCH3(0, 0, 0)

                result1 = self.esp.writeFirmwareOne(self.diciParam['serial3'], self.diciParam['baudrate3'],
                                                        self.diciParam['mem4'], self.diciParam['path4'])
                for i in result1.split(';'):
                    if i == '0':
                        self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Gravação firmware <font color='white' size='3'>[OK]</font>")
                        logging.info("Gravação firmware placa 3 [OK]")

                    if i == '2':
                            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> "+result1)
                            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Erro de gravação firmware <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação firmware placa 3 [ERRO]")
                            self.is_killed = True
                print(result1)

        if self.is_killed:
            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font><font color='red' size='3'> Processo finalizado!</font>\r\n")
            logging.info("Processo interrompido [INFO]")
            self.cmdGpio.cmdReleCH3(1, 1, 1)
        else:
            print("FIM")
            print(self.diciNSerial)
            print(self.diciNSerial['mac3'])
            self.threadSignalPl3.emit('MAC3;' + self.diciNSerial['mac3'])

            self.cmdGpio.cmdReleCH3(1, 1, 1)
            self.threadSignalPl3.emit("FIM")


    def kill(self):
        self.is_killed = True
        print("Kill True!")

    def saveN3Reg(self, mac, serie):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        cfg.set('numeroserial',  'numero3', serie)
        cfg.set('numeroserial', 'mac3', mac)
        cfgfile = open('config.ini', 'w')
        cfg.write(cfgfile, space_around_delimiters=False)
        cfgfile.close()

class WorkerGravPl4(QThread):
    threadSignalPl4 = pyqtSignal(str)
    def __init__(self, parent=None, *args,):
        super(WorkerGravPl4, self).__init__(parent)
        self.is_killed = False
        self.diciParam = args[0]
        self.esp = espFlasher.EspFlasher()
        self.diciNSerial ={}
        logging.basicConfig(filename='log.txt', encoding='utf-8', format = '%(asctime)s %(levelname)-8s %(message)s',level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        self.cmdSerial = commandTest.CommdTest()
        self.cmdGpio = gpioControl.GpioAdsControl()
        self.cmdGpio.cmdReleCH4(1, 1, 1)
        self.cmdGpio.cmdReleIN(0, 1)
        self.macMemo = '0'
        self.mqtt_client = MqttClient(broker=self.diciParam["server"], client_id='204-jiga',
                                      username=self.diciParam["username"], password=self.diciParam["password"])
        self.value = ''
        self.count = 0

    def run(self):
        # Do something...
        if (self.diciParam["placa4"] == True): #------------------------ PLACA 4 --------------------------------------
            logging.debug("Placa 4 ------------------------------")
            if not self.is_killed:
                try:

                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Inicia processo de gravação...")

                    self.cmdGpio.cmdReleCH4(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                    QThread.msleep(1000)
                    self.cmdGpio.cmdReleCH4(1, 0, 1)
                    QThread.msleep(1000)
                    self.cmdGpio.cmdReleCH4(0, 0, 0)

                    val = self.esp.readChipInfo(self.diciParam['serial4'], '115200')
                    nameFirm = 'Firmware: '+self.diciParam['name4']

                    self.macMemo = val['mac']
                    self.diciNSerial['mac4'] = self.macMemo
                    self.diciParam['mac4'] = self.macMemo
                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Serial: " + self.diciParam['serial4'] + " Baud: " + self.diciParam['baudrate4'])

                    while (True):
                        self.mqtt_client.connect()
                        self.value = self.mqtt_client.connectGota(self.diciParam, 'mac4', test={})

                        if not self.value == 'ERRO':
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> MAC: <font color='GreenYellow' size='3'>" +self.diciParam['mac4'] + "</font>")
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Serial Number: <font color='GreenYellow' size='3'>" + self.value + "</font>")
                            self.saveN4Reg(self.diciParam['mac4'], str(self.value))
                            break
                        else:
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> <font color='red' size='3'> Repetindo consulta ao GOTA!</font>")
                            self.count = self.count + 1

                        if self.count == 5:
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> <font color='red' size='3'> Erro Servidor GOTA!</font>")
                            self.saveN4Reg('0', '0')
                            self.count = 0
                            break

                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4] </font> "+ nameFirm)

                    logging.info("MAC placa 4: " + self.macMemo)
                    logging.info(nameFirm)
                except:
                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> USB Sem conexão - Placa 4 <font color='red' size='3'>[ERRO]</font>")
                    self.is_killed = True

            if not self.is_killed:  # GRAVANDO 1º BLOCO DE FIRMWARE (BOOT-LOAD)

                self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Gravando firmware de teste")
                result = self.esp.writeFirmwareMult(self.diciParam['serial4'], self.diciParam['baudrate4'],
                                                        self.diciParam['mem1'], self.diciParam['path1'], self.diciParam['mem2'],
                                                        self.diciParam['path2'], self.diciParam['mem3'],
                                                        self.diciParam['path3'])
                for i in result.split(';'):
                    if i == '0':
                        self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Gravação bootload <font color='white' size='3'>[OK]</font>")
                        logging.info("Gravação bootload placa 4 [OK]")

                    if i == '2':
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> "+result)
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Erro de gravação bootload <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação bootload placa 4 [ERRO]")
                            self.is_killed = True

            if not self.is_killed: # GRAVANDO 2º BLOCO DE FIRMWARE (TESTE)

                QThread.msleep(500)
                self.cmdGpio.cmdReleCH4(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(2000)
                self.cmdGpio.cmdReleCH4(1, 0, 1)
                QThread.msleep(2000)
                self.cmdGpio.cmdReleCH4(0, 0, 0)

                result1 = self.esp.writeFirmwareOne(self.diciParam['serial4'], self.diciParam['baudrate4'],
                                                        self.diciParam['mem4'], self.diciParam['path4'])
                for i in result1.split(';'):
                    if i == '0':
                        self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Gravação firmware <font color='white' size='3'>[OK]</font>")
                        logging.info("Gravação firmware placa 4 [OK]")

                    if i == '2':
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font>"+result1)
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Erro de gravação firmware <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação firmware placa 4 [ERRO]")
                            self.is_killed = True
                print(result1)

        if self.is_killed:
            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font><font color='red' size='3'> Processo finalizado!</font>\r\n")
            logging.info("Processo interrompido [INFO]")
            self.cmdGpio.cmdReleCH4(1, 1, 1)
        else:
            print("FIM")
            print(self.diciNSerial)
            print(self.diciNSerial['mac4'])
            self.threadSignalPl4.emit('MAC4;' + self.diciNSerial['mac4'])

            self.cmdGpio.cmdReleCH4(1, 1, 1)
            self.threadSignalPl4.emit("FIM")

    def kill(self):
        self.is_killed = True
        print("Kill True!")

    def saveN4Reg(self, mac, serie):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        cfg.set('numeroserial',  'numero4', serie)
        cfg.set('numeroserial', 'mac4', mac)
        cfgfile = open('config.ini', 'w')
        cfg.write(cfgfile, space_around_delimiters=False)
        cfgfile.close()

class TelaGravacao(QMainWindow):
    def __init__(self,  *args, **kw):
        super(TelaGravacao, self).__init__()
        self.ui = Ui_MainWindowGrav()
        self.ui.setupUi(self)

        self.typeCheck = "0"
        self.diciPlacas = {}
        self.diciSerialStat = {}
        self.diciValidType = {}
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini')

        self.ui.textEditLogGrav.clear()
        self.ui.textEditLogGrav.setStyleSheet('background-color: black; font: bold 14px; color: green')
        self.ui.textEditLogGrav.append("Log iniciado!!!")
        #if not args:
            #self.ui.textEditLogGrav.append("Último número de série gravado: <font color='white' size='3'>" + self.cfg.get('numeroserial','registro') + "</font>")

        self.ui.checkBoxGrav1.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/pcb_off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/pcb_on.png);margin-left: 5%;}')
        self.ui.checkBoxGrav2.setStyleSheet('QCheckBox {spacing: 10px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/pcb_off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/pcb_on.png);margin-left: 5%;}')
        self.ui.checkBoxGrav3.setStyleSheet('QCheckBox {spacing: 10px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/pcb_off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/pcb_on.png);margin-left: 5%;}')
        self.ui.checkBoxGrav4.setStyleSheet('QCheckBox {spacing: 10px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/pcb_off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/pcb_on.png);margin-left: 5%;}')

        self.ui.checkBoxGrav1.clicked.connect(lambda: self.clickBoxGrav(self.ui.checkBoxGrav1.isChecked(), "1"))
        self.ui.checkBoxGrav2.clicked.connect(lambda: self.clickBoxGrav(self.ui.checkBoxGrav2.isChecked(), "2"))
        self.ui.checkBoxGrav3.clicked.connect(lambda: self.clickBoxGrav(self.ui.checkBoxGrav3.isChecked(), "3"))
        self.ui.checkBoxGrav4.clicked.connect(lambda: self.clickBoxGrav(self.ui.checkBoxGrav4.isChecked(), "4"))

        self.ui.checkBoxConex.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')
        self.ui.checkBoxCalibra.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')
        self.ui.checkBoxProdu.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')

        self.ui.checkBoxConex.clicked.connect(lambda: self.clickBoxFirmwareTip("1"))
        self.ui.checkBoxCalibra.clicked.connect(lambda: self.clickBoxFirmwareTip("2"))
        self.ui.checkBoxProdu.clicked.connect(lambda: self.clickBoxFirmwareTip("3"))

        self.ui.btnStartGrav.clicked.connect(self.startTestGrav)
        self.ui.btnStopGrav.clicked.connect(self.stopTestGrav)
        self.ui.btnClearGrav.clicked.connect(self.clearTextsGrav)

        self.readParam()
        if (self.diciSerialStat["stat1"] == "0"):
            self.ui.labelP1.setStyleSheet('color: red')
        else: self.ui.checkBoxGrav1.setChecked(True)
        if (self.diciSerialStat["stat2"] == "0"):
            self.ui.labelP2.setStyleSheet('color: red')
        else: self.ui.checkBoxGrav2.setChecked(True)
        if (self.diciSerialStat["stat3"] == "0"):
            self.ui.labelP3.setStyleSheet('color: red')
        else: self.ui.checkBoxGrav3.setChecked(True)
        if (self.diciSerialStat["stat4"] == "0"):
            self.ui.labelP4.setStyleSheet('color: red')
        else: self.ui.checkBoxGrav4.setChecked(True)

        try:
            self.arg = args[0]
            #print("self.arg************************")
            #print(self.arg)
            tipo = self.arg["modeRec"]
            if tipo == "CONE_ON":
                self.ui.checkBoxConex.setChecked(True)
                self.clickBoxFirmwareTip("1")
                self.validaType("1")
                self.startTestGrav() #aqui
            if tipo == "CALI_ON":
                self.ui.checkBoxCalibra.setChecked(True)
                self.clickBoxFirmwareTip("2")
                self.validaType("2") #aqui
                self.startTestGrav()
            if tipo == "PROD_ON":
                self.ui.checkBoxProdu.setChecked(True)
                self.clickBoxFirmwareTip("3")
                self.validaType("3")
                self.startTestGrav()

            #print("self.arg ************************")
            #print(self.arg)
        except:
            pass

    def clickBoxGrav(self, state, ref):
        if state :
            self.ui.textEditLogGrav.append("Placa "+ref+" ON...")
            if (ref == "1"):
                if self.validaSerial(ref):
                    self.alertaSerial("Serial 1 desativada!")
                    self.ui.checkBoxGrav1.setChecked(False)
            if (ref == "2"):
                if self.validaSerial(ref):
                    self.alertaSerial("Serial 2 desativada!")
                    self.ui.checkBoxGrav2.setChecked(False)
            if (ref == "3"):
                if self.validaSerial(ref):
                    self.alertaSerial("Serial 3 desativada!")
                    self.ui.checkBoxGrav3.setChecked(False)
            if (ref == "4"):
                if self.validaSerial(ref):
                    self.alertaSerial("Serial 4 desativada!")
                    self.ui.checkBoxGrav4.setChecked(False)
        else:
            self.ui.textEditLogGrav.append("Placa "+ref+" OFF...")

    def displayShow(self):
        self.show()

    def closeEvent(self, event):
        try:
            print("try")
            print(self.diciPlacas)
            if self.arg["modeRec"] != 'OFF':
                print("try if")
                self.tTeste()
            else:
                print("try else")
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
                    self.origem = main.Tela()
                    self.origem.show()
                else:
                    event.ignore()
        except:
            print("except")
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
                self.origem = main.Tela()
                self.origem.show()
            else:
                event.ignore()

    def tTeste(self):
        self.telaTeste = guiTeste.TelaTeste()
        self.telaTeste.displayShow()
        self.close()

    def clearTextsGrav(self):
        self.ui.textEditLogGrav.clear()

    def startTestGrav(self):
        try:
            if self.workrGrav.isRunning():
                self.ui.textEditLogGrav.append("<font color='red' size='3'>Processo em andamento...</font>\r\n")
            else:
                breakpoint(exit())
        except:
            print("self.diciValidType ************************")
            print(self.diciValidType)
            self.ui.textEditLogGrav.clear()
            self.ui.textEditLogGrav.append("Log iniciado!!!")
            cfg = configparser.ConfigParser()
            cfg.read('config.ini')
            val = cfg.get('numeroserial', 'registro')
            #self.ui.textEditLogGrav.append("Último número de série gravado: <font color='white' size='3'>" + val + "</font>")

            if (not self.ui.checkBoxGrav1.isChecked() and
                    not self.ui.checkBoxGrav2.isChecked() and
                    not self.ui.checkBoxGrav3.isChecked() and
                    not self.ui.checkBoxGrav4.isChecked()):
                self.alertaSerial("Atenção selecione uma ou mias placas")
            elif (not self.ui.checkBoxConex.isChecked() and
                    not self.ui.checkBoxCalibra.isChecked() and
                    not self.ui.checkBoxProdu.isChecked()):
                self.alertaSerial("Atenção selecione um tipo")
            else:
                self.ui.textEditLogGrav.append("Iniciando testes....")
                self.diciPlacas["esptoolFlash"] = cfg.get('firmware', 'esptoolFlash')
                #self.diciPlacas["bootloader"] = cfg.get('firmware', 'path1')
                self.diciPlacas["path1"] = cfg.get('firmware', 'path1')
                self.diciPlacas["mem1"] = cfg.get('memoria', 'end1')
                #self.diciPlacas["partitions"] = cfg.get('firmware', 'path2')
                self.diciPlacas["path2"] = cfg.get('firmware', 'path2')
                self.diciPlacas["mem2"] = cfg.get('memoria', 'end2')
                #self.diciPlacas["ota_data_initial"] = cfg.get('firmware', 'path3')
                self.diciPlacas["path3"] = cfg.get('firmware', 'path3')
                self.diciPlacas["mem3"] = cfg.get('memoria', 'end3')

                if self.typeCheck == "1": # Conex
                    self.validaType("1")
                    self.diciPlacas["name"] = self.diciValidType["name"]
                    self.diciPlacas["path4"] = self.diciValidType["path"]
                    self.diciPlacas["stat"] = self.diciValidType["stat"]

                if self.typeCheck == "2":  # Calibra
                    self.validaType("2")
                    self.diciPlacas["name"] = self.diciValidType["name"]
                    self.diciPlacas["path4"] = self.diciValidType["path"]
                    self.diciPlacas["stat"] = self.diciValidType["stat"]

                if self.typeCheck == "3":  # Produ
                    self.validaType("3")
                    self.diciPlacas["name"] = self.diciValidType["name"]
                    self.diciPlacas["path4"] = self.diciValidType["path"]
                    self.diciPlacas["stat"] = self.diciValidType["stat"]

                self.diciPlacas["mem4"] = cfg.get('memoria', 'end4')

                self.diciPlacas["placa1"] = self.ui.checkBoxGrav1.isChecked()
                self.diciPlacas["serial1"] = self.diciSerialStat["serial1"]
                self.diciPlacas["baudrate1"] = self.diciSerialStat["baudrate1"]
                self.diciPlacas["name1"] = self.diciValidType["name"]
                #self.diciPlacas["path1"] = self.diciValidType["path"]
                self.diciPlacas["stat1"] = self.diciValidType["stat"]
                self.diciPlacas["mac1"] = '0'

                self.diciPlacas["placa2"] = self.ui.checkBoxGrav2.isChecked()
                self.diciPlacas["serial2"] = self.diciSerialStat["serial2"]
                self.diciPlacas["baudrate2"] = self.diciSerialStat["baudrate2"]
                self.diciPlacas["name2"] = self.diciValidType["name"]
                #self.diciPlacas["path2"] = self.diciValidType["path"]
                self.diciPlacas["stat2"] = self.diciValidType["stat"]
                self.diciPlacas["mac2"] = '0'

                self.diciPlacas["placa3"] = self.ui.checkBoxGrav3.isChecked()
                self.diciPlacas["serial3"] = self.diciSerialStat["serial3"]
                self.diciPlacas["baudrate3"] = self.diciSerialStat["baudrate3"]
                self.diciPlacas["name3"] = self.diciValidType["name"]
                #self.diciPlacas["path3"] = self.diciValidType["path"]
                self.diciPlacas["stat3"] = self.diciValidType["stat"]
                self.diciPlacas["mac3"] = '0'

                self.diciPlacas["placa4"] = self.ui.checkBoxGrav4.isChecked()
                self.diciPlacas["serial4"] = self.diciSerialStat["serial4"]
                self.diciPlacas["baudrate4"] = self.diciSerialStat["baudrate4"]
                self.diciPlacas["name4"] = self.diciValidType["name"]
                #self.diciPlacas["path4"] = self.diciValidType["path"]
                self.diciPlacas["stat4"] = self.diciValidType["stat"]
                self.diciPlacas["mac4"] = '0'

                self.diciPlacas["server"] = cfg.get('mqtt', 'server')
                self.diciPlacas["port"] = cfg.get('mqtt', 'port')
                self.diciPlacas["qos"] = cfg.get('mqtt', 'qos')
                self.diciPlacas["username"] = cfg.get('mqtt', 'username')
                self.diciPlacas["password"] = cfg.get('mqtt', 'password')
                self.diciPlacas["topicpub"] = cfg.get('mqtt', 'topicpub')
                self.diciPlacas["topicsub"] = cfg.get('mqtt', 'topicsub')

                self.diciPlacas["nserial"] = cfg.get('numeroserial', 'registro')
                print(self.diciPlacas)
                self.zeraNS()
                #self.startThreadGravacao(self.diciPlacas)
                if self.diciPlacas["placa1"]:
                    print("Thread placa 1 on")
                    print(self.diciPlacas)
                    self.startThreadGravPl1(self.diciPlacas)
                if self.diciPlacas["placa2"]:
                    print("Thread placa 2 on")
                    self.startThreadGravPl2(self.diciPlacas)
                if self.diciPlacas["placa3"]:
                    print("Thread placa 3 on")
                    self.startThreadGravPl3(self.diciPlacas)
                if self.diciPlacas["placa4"]:
                    print("Thread placa 4 on")
                    self.startThreadGravPl4(self.diciPlacas)

    def stopTestGrav(self):
        try:
            if self.workrGrav.isRunning():
                self.ui.textEditLogGrav.append("<font color='red' size='3'>Parando processo...</font>\r\n")
                self.workrGrav.kill()
            if self.workrGrav2.isRunning():
                self.ui.textEditLogGrav.append("<font color='red' size='3'>Parando processo...</font>\r\n")
                self.workrGrav2.kill()
            if self.workrGrav3.isRunning():
                self.ui.textEditLogGrav.append("<font color='red' size='3'>Parando processo...</font>\r\n")
                self.workrGrav3.kill()
            if self.workrGrav4.isRunning():
                self.ui.textEditLogGrav.append("<font color='red' size='3'>Parando processo...</font>\r\n")
                self.workrGrav4.kill()
        except:
            self.ui.textEditLogGrav.append("<font color='red' size='3'>Processo finalizado!</font>\r\n")

    def clickBoxFirmwareTip(self, ref):
        if ref == "1":
            self.ui.textEditLogGrav.append("Tipo: " + ref + " Conexão")
            self.ui.checkBoxCalibra.setChecked(False)
            self.ui.checkBoxProdu.setChecked(False)
            self.typeCheck = "1"
        if ref == "2":
            self.ui.textEditLogGrav.append("Tipo: " + ref + " Calibração")
            self.ui.checkBoxConex.setChecked(False)
            self.ui.checkBoxProdu.setChecked(False)
            self.typeCheck = "2"
        if ref == "3":
            self.ui.textEditLogGrav.append("Tipo: " + ref + " Produção")
            self.ui.checkBoxConex.setChecked(False)
            self.ui.checkBoxCalibra.setChecked(False)
            self.typeCheck = "3"

    def readParam(self):
        self.cfg.read('config.ini')
        self.diciSerialStat["stat1"] = self.cfg.get('serial', 'stat1')
        self.diciSerialStat["serial1"] = self.cfg.get('serial', 'serial1')
        self.diciSerialStat["baudrate1"] = self.cfg.get('serial', 'baudrate1')
        self.diciSerialStat["stat2"] = self.cfg.get('serial', 'stat2')
        self.diciSerialStat["serial2"] = self.cfg.get('serial', 'serial2')
        self.diciSerialStat["baudrate2"] = self.cfg.get('serial', 'baudrate2')
        self.diciSerialStat["stat3"] = self.cfg.get('serial', 'stat3')
        self.diciSerialStat["serial3"] = self.cfg.get('serial', 'serial3')
        self.diciSerialStat["baudrate3"] = self.cfg.get('serial', 'baudrate3')
        self.diciSerialStat["stat4"] = self.cfg.get('serial', 'stat4')
        self.diciSerialStat["serial4"] = self.cfg.get('serial', 'serial4')
        self.diciSerialStat["baudrate4"] = self.cfg.get('serial', 'baudrate4')

    def validaSerial(self, ref):
        if (self.diciSerialStat["stat1"] == "0" and ref == "1"):
            return True
        if (self.diciSerialStat["stat2"] == "0" and ref == "2"):
            return True
        if (self.diciSerialStat["stat3"] == "0" and ref == "3"):
            return True
        if (self.diciSerialStat["stat4"] == "0" and ref == "4"):
            return True

    def validaType(self, ref):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        if (ref == "1"):  #Conex
            print("#Conex")
            if (cfg.get('conexao', 'stat1') == "1"):
                self.diciValidType["name"] = cfg.get('conexao', 'name1')
                self.diciValidType["path"] = cfg.get('conexao', 'path1')
                self.diciValidType["stat"] = cfg.get('conexao', 'stat1')
                #return self.diciValidType
            if (cfg.get('conexao', 'stat2') == "1"):
                self.diciValidType["name"] = cfg.get('conexao', 'name2')
                self.diciValidType["path"] = cfg.get('conexao', 'path2')
                self.diciValidType["stat"] = cfg.get('conexao', 'stat2')
                #return self.diciValidType
            if (cfg.get('conexao', 'stat3') == "1"):
                self.diciValidType["name"] = cfg.get('conexao', 'name3')
                self.diciValidType["path"] = cfg.get('conexao', 'path3')
                self.diciValidType["stat"] = cfg.get('conexao', 'stat3')
                #return self.diciValidType
            if (cfg.get('conexao', 'stat4') == "1"):
                self.diciValidType["name"] = cfg.get('conexao', 'name4')
                self.diciValidType["path"] = cfg.get('conexao', 'path4')
                self.diciValidType["stat"] = cfg.get('conexao', 'stat4')
                #return self.diciValidType
        if ( ref == "2"):  #Calibra
            print("#Calibra")
            if (cfg.get('calibracao', 'stat1') == "1"):
                self.diciValidType["name"] = cfg.get('calibracao', 'name1')
                self.diciValidType["path"] = cfg.get('calibracao', 'path1')
                self.diciValidType["stat"] = cfg.get('calibracao', 'stat1')
                #return self.diciValidType
            if (cfg.get('calibracao', 'stat2') == "1"):
                self.diciValidType["name"] = cfg.get('calibracao', 'name2')
                self.diciValidType["path"] = cfg.get('calibracao', 'path2')
                self.diciValidType["stat"] = cfg.get('calibracao', 'stat2')
                #return self.diciValidType
            if (cfg.get('calibracao', 'stat3') == "1"):
                self.diciValidType["name"] = cfg.get('calibracao', 'name3')
                self.diciValidType["path"] = cfg.get('calibracao', 'path3')
                self.diciValidType["stat"] = cfg.get('calibracao', 'stat3')
                #return self.diciValidType
            if (cfg.get('calibracao', 'stat4') == "1"):
                self.diciValidType["name"] = cfg.get('calibracao', 'name4')
                self.diciValidType["path"] = cfg.get('calibracao', 'path4')
                self.diciValidType["stat"] = cfg.get('calibracao', 'stat4')
                #return self.diciValidType
        if (ref == "3"):  #Produ
            print("#Produ")
            if (cfg.get('producao', 'stat1') == "1"):
                self.diciValidType["name"] = cfg.get('producao', 'name1')
                self.diciValidType["path"] = cfg.get('producao', 'path1')
                self.diciValidType["stat"] = cfg.get('producao', 'stat1')
                #return self.diciValidType
            if (cfg.get('producao', 'stat2') == "1"):
                self.diciValidType["name"] = cfg.get('producao', 'name2')
                self.diciValidType["path"] = cfg.get('producao', 'path2')
                self.diciValidType["stat"] = cfg.get('producao', 'stat2')
                #return self.diciValidType
            if (cfg.get('producao', 'stat3') == "1"):
                self.diciValidType["name"] = cfg.get('producao', 'name3')
                self.diciValidType["path"] = cfg.get('producao', 'path3')
                self.diciValidType["stat"] = cfg.get('producao', 'stat3')
                #return self.diciValidType
            if (cfg.get('producao', 'stat4') == "1"):
                self.diciValidType["name"] = cfg.get('producao', 'name4')
                self.diciValidType["path"] = cfg.get('producao', 'path4')
                self.diciValidType["stat"] = cfg.get('producao', 'stat4')
                #return self.diciValidType"""
        print("self.diciValidType**********")
        print(self.diciValidType)

    def alertaSerial(self, msg):
        userInfo = QMessageBox.information(self, "Ação Proibida", msg, QMessageBox.Ok)
        if userInfo == QMessageBox.Ok:
            return True

    def tNumero(self, param):
        self.telaIdMac = guiIdMac.TelaIdMac(param)
        self.telaIdMac.displayShow()

    def startThreadGravPl1(self, param):
        self.workrGrav = WorkerGravPl1(self, param)
        self.workrGrav.threadSignalPl1.connect(self.on_threadSignalGravPl1)
        self.workrGrav.start()

    def on_threadSignalGravPl1(self, inf):
        print('PLACA 1 MAC '+ str(inf))
        x = inf.split(';')
        if(x[0] == 'MAC1'):
            self.diciPlacas["mac1"] = x[1]
            self.atualizarNSMac(self.diciPlacas)

        if (inf == "FIM"):
            print("FIM")
            #self.tNumero(self.diciPlacas)

        else:
            self.ui.textEditLogGrav.append(str(inf))

    def startThreadGravPl2(self, param):
        self.workrGrav2 = WorkerGravPl2(self, param)
        self.workrGrav2.threadSignalPl2.connect(self.on_threadSignalGravPl2)
        self.workrGrav2.start()

    def on_threadSignalGravPl2(self, inf):
        print('PLACA 2 MAC '+ str(inf))
        x = inf.split(';')
        if(x[0] == 'MAC2'):
            self.diciPlacas["mac2"] = x[1]
            self.atualizarNSMac(self.diciPlacas)

        if (inf == "FIM"):
            print("FIM")

        else:
            self.ui.textEditLogGrav.append(str(inf))

    def startThreadGravPl3(self, param):
        self.workrGrav3 = WorkerGravPl3(self, param)
        self.workrGrav3.threadSignalPl3.connect(self.on_threadSignalGravPl3)
        self.workrGrav3.start()

    def on_threadSignalGravPl3(self, inf):
        print('PLACA 3 MAC '+ str(inf))
        x = inf.split(';')
        if(x[0] == 'MAC3'):
            self.diciPlacas["mac3"] = x[1]
            self.atualizarNSMac(self.diciPlacas)

        if (inf == "FIM"):
            print("FIM")

        else:
            self.ui.textEditLogGrav.append(str(inf))

    def startThreadGravPl4(self, param):
        self.workrGrav4 = WorkerGravPl4(self, param)
        self.workrGrav4.threadSignalPl4.connect(self.on_threadSignalGravPl4)
        self.workrGrav4.start()

    def on_threadSignalGravPl4(self, inf):
        print('PLACA 4 MAC '+ str(inf))
        x = inf.split(';')
        if(x[0] == 'MAC4'):
            self.diciPlacas["mac4"] = x[1]
            self.atualizarNSMac(self.diciPlacas)

        if (inf == "FIM"):
            print("FIM")

        else:
            self.ui.textEditLogGrav.append(str(inf))

    def atualizarNSMac(self, param):
        print("Numero serial inicio "+str(param['nserial']))
        distStatus = {}
        cond = False

        if param['placa1']:
            if self.workrGrav.isRunning():
                distStatus['placa1'] = "Running"
            elif self.workrGrav.isFinished():
                distStatus['placa1'] = "Finished"
        else:
            distStatus['placa1'] = "Disable"
        if param['placa2']:
            if self.workrGrav2.isRunning():
                distStatus['placa2'] = "Running"
            elif self.workrGrav2.isFinished():
                distStatus['placa2'] = "Finished"
        else:
            distStatus['placa2'] = "Disable"
        if param['placa3']:
            if self.workrGrav3.isRunning():
                distStatus['placa3'] = "Running"
            elif self.workrGrav3.isFinished():
                distStatus['placa3'] = "Finished"
        else:
            distStatus['placa3'] = "Disable"
        #if param['placa4'] and param['mac4'] != "0":
        if param['placa4']:
            if self.workrGrav4.isRunning():
                distStatus['placa4'] = "Running"
            if self.workrGrav4.isFinished():
                distStatus['placa4'] = "Finished"
        else:
            distStatus['placa4'] = "Disable"

        if (param['placa1']):
            distStatus['placa1Status'] = True
        else:
            distStatus['placa1Status'] = False

        if (param['placa2']):
            distStatus['placa2Status'] = True
        else:
            distStatus['placa2Status'] = False

        if (param['placa3']):
            distStatus['placa3Status'] = True
        else:
            distStatus['placa3Status'] = False

        if (param['placa4']):
            distStatus['placa4Status'] = True
        else:
            distStatus['placa4Status'] = False

        count = 0

        for status in distStatus.values():
            if status == 'Running':
                cond = False
                break
            else:
                cond = True

        if cond:
            try:
                if param['mac1'] == "0":
                    verify1 = True

            except:
                pass
            # -----------------------------------------------------------------------------------------------
            try:
                if param['mac2'] == "0":
                    verify2 = True

            except:
                pass
            # -----------------------------------------------------------------------------------------------
            try:
                if param['mac3'] == "0":
                    verify3 = True

            except:
                pass
            # -----------------------------------------------------------------------------------------------
            try:
                if param['mac4'] == "0":
                    verify4 = True

            except:
                pass
            self.saveNRec(str(int(param['nserial'])+count))

            try:
                self.tNumero(self.arg)
            except:
                self.tNumero(self.diciPlacas)

        else:
            print("Thread running...")

    def saveNRec(self, value):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        cfg.set('numeroserial',  'registro', value)
        cfgfile = open('config.ini', 'w')
        cfg.write(cfgfile, space_around_delimiters=False)
        cfgfile.close()

    def zeraNS(self):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        cfg.set('numeroserial', 'numero1', '0')
        cfg.set('numeroserial', 'mac1', '0')
        cfg.set('numeroserial', 'numero2', '0')
        cfg.set('numeroserial', 'mac2', '0')
        cfg.set('numeroserial', 'numero3', '0')
        cfg.set('numeroserial', 'mac3', '0')
        cfg.set('numeroserial', 'numero4', '0')
        cfg.set('numeroserial', 'mac4', '0')
        cfgfile = open('config.ini', 'w')
        cfg.write(cfgfile, space_around_delimiters=False)
        cfgfile.close()