import guiGravacao
import guiIdMac
import main
import configparser
from PyQt5.QtCore import QThread, pyqtSignal
from designer.tela2_Jiga import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import espFlasher
import logging
import jsonFiles
import commandTest
import gpioControl
from mqttConnect import MqttClient

class TesteWorkerPl1(QThread):
    threadSignalPl1 = pyqtSignal(str)
    def __init__(self, parent=None, *args,):
        super(TesteWorkerPl1, self).__init__(parent)
        self.is_killed = False
        self.diciParam = args[0]
        self.esp = espFlasher.EspFlasher()
        self.diciNSerial = {}
        logging.basicConfig(filename='log.txt', encoding='utf-8', format = '%(asctime)s %(levelname)-8s %(message)s',level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        self.cmdSerial = commandTest.CommdTest()
        self.cmdGpio = gpioControl.GpioAdsControl()
        self.cmdGpio.cmdReleCH1(1, 1, 1)
        self.cmdGpio.cmdReleIN(0, 1)
        self.macMemo = '0'
        self.jf = jsonFiles.JsonFiles()
        print(self.diciParam)
        self.mqtt_client = MqttClient(broker=self.diciParam["server"], client_id='101-jiga', username=self.diciParam["username"], password=self.diciParam["password"])
        self.value = ''
        self.diciPay = {}
        self.count = 0

    def run(self):
        # Do something...
        if (self.diciParam["placa1"] == True): #------------------------ PLACA 1 --------------------------------------
            logging.debug("Placa 1 ------------------------------")
            if not self.is_killed:
                try:
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Inicia processo...")
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
                    print(self.diciParam['mac1'])
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Serial: " + self.diciParam['serial1'] + " Baud: " + self.diciParam['baudrate1'])

                    while(True):
                        self.mqtt_client.connect()
                        self.value = self.mqtt_client.connectGota(self.diciParam, 'mac1', test={})

                        if not self.value == 'ERRO':
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> MAC: <font color='GreenYellow' size='3'>" +self.diciParam['mac1'] + "</font>")
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Serial Number: <font color='GreenYellow' size='3'>" +self.value+ "</font>")
                            self.saveN1Reg(self.diciParam['mac1'], str(self.value))
                            break
                        else:
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> <font color='red' size='3'> Repetindo consulta ao GOTA!</font>")
                            self.count = self.count+1

                        if self.count == 5:
                            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> <font color='red' size='3'> Erro Servidor GOTA!</font>")
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

                self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Gravando firmware de teste")
                result = self.esp.writeFirmwareMult(self.diciParam['serial1'], self.diciParam['baudrate1'],
                                                        self.diciParam['mem1'], self.diciParam['path1'], self.diciParam['mem2'],
                                                        self.diciParam['path2'], self.diciParam['mem3'],
                                                        self.diciParam['path3'])
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

            if not self.is_killed:

                print("Teste 1") #-------------- Desligar relê power, desligar relê flash, e ligar relê power
                self.cmdGpio.cmdReleCH1(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(3000)
                self.cmdGpio.cmdReleCH1(0, 1, 1)
                QThread.msleep(3000)
                self.cmdGpio.cmdReleCH1(0, 1, 0)

                self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Iniciando teste via comandos")
                voltHP = self.cmdGpio.readVoltPl1(0)
                voltLP = self.cmdGpio.readVoltPl1(1)
                if voltHP > 3.0:
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Tensão HP: " + str(voltHP) + "V <font color='white' size='3'>[OK]</font>")  # 1 = HP3.3v
                    logging.info("Tensão HP: " + str(voltHP)+"V")
                else:
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Tensão HP: " + str(voltHP) + "V <font color='red' size='3'>[ERRO]</font>")  # 1 = HP3.3v
                    logging.info("Tensão HP: " + str(voltHP)+"V")
                if voltLP > 3.0:
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Tensão LP: " + str(voltLP) + "V <font color='white' size='3'>[OK]</font>")  # 1 = HP3.3v
                    logging.info("Tensão LP: " + str(voltLP)+"V")
                else:
                    self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Tensão LP: " + str(voltLP) + "V <font color='red' size='3'>[ERRO]</font>")  # 1 = HP3.3v
                    logging.info("Tensão LP: " + str(voltLP)+"V")

                QThread.msleep(1000)
                self.cmdGpio.cmdReleCH1(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(1000)
                self.cmdGpio.cmdReleCH1(0, 1, 0)
                QThread.msleep(1000)

                for indice, valor in enumerate(self.cmdSerial.diciCommands.values(), start=1):
                    if indice == 1:
                        self.cmdSerial.returnSerial(self.diciParam['serial1'], '115200', str(valor))
                    if not self.is_killed:
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Teste: "+str(valor))

                        rest = self.cmdSerial.returnSerial(self.diciParam['serial1'], '115200', str(valor))
                        logging.info(str(rest)+ " [OK]")
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font><font color='white' size='3'> "+str(rest)+"</font>")

                        if valor == 'MAX':
                            self.diciPay['MAX'] = rest
                        elif valor == 'BME':
                            self.diciPay['BME'] = rest
                        elif valor == 'BATTERY':
                            self.diciPay['BATTERY'] = rest
                        elif valor == 'RTC':
                            self.diciPay['RTC'] = rest
                        elif valor == 'FRAM':
                            self.diciPay['FRAM'] = rest
                        elif valor == 'WIFI':
                            self.diciPay['WIFI'] = rest
                        elif valor == 'MQTT':
                            self.diciPay['MQTT'] = rest

                val = self.mountPay(self.diciPay)

                while (True):
                    self.mqtt_client.connect()
                    self.value = self.mqtt_client.connectGota(self.diciParam, 'mac1', test=val)
                    if not self.value == 'ERRO':
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> MAC: <font color='GreenYellow' size='3'>" +self.diciParam['mac1'] + "</font>")
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> Serial Number: <font color='GreenYellow' size='3'>" + self.value + "</font>")
                        self.saveN1Reg(self.diciParam['mac1'], str(self.value))
                        break
                    else:
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> <font color='red' size='3'> Repetindo consulta ao GOTA!</font>")
                        self.count = self.count + 1

                    if self.count == 5:
                        self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font> <font color='red' size='3'> Erro Servidor GOTA!</font>")
                        self.saveN1Reg('0', '0')
                        self.count = 0
                        break

        if self.is_killed:
            self.threadSignalPl1.emit("<font color= 'Chocolate' size='2'>[PLACA-1]</font><font color='red' size='3'> Processo finalizado!</font>\r\n")
            logging.info("Processo interrompido [INFO]")
            self.cmdGpio.cmdReleCH1(1, 1, 1)
        else:
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

    def mountPay(self, result):
        diciPay = {}
        # ----------------- MAX ----------
        try:
            input_stringMAX = result['MAX']
            value_partMAX = input_stringMAX.split()[1]
            value_partMAX = value_partMAX.rstrip('C')
            value_partMAX = value_partMAX.rstrip('*')
            extracted_valueMAX = float(value_partMAX)
            print(f' MAX : {extracted_valueMAX}')
            if extracted_valueMAX > 0 and extracted_valueMAX < 50:
                diciPay['MAX'] = 'True'
            else:
                diciPay['MAX'] = 'False'
        except:
            diciPay['MAX'] = 'False'
        # ----------------- BME ----------
        try:
            input_stringBME = result['BME']
            value_partBME = input_stringBME.split('||')[1]
            extracted_valueBME = float(value_partBME.strip().rstrip('%'))
            print(f' BME : {extracted_valueBME}')
            if extracted_valueBME == 0.00:
                diciPay['BME'] = 'False'
            else:
                diciPay['BME'] = 'True'
        except:
            diciPay['BME'] = 'True'
        # ----------------- BATTERY ----------
        try:
            input_stringBAT = result['BATTERY']
            value_partBAT = input_stringBAT.split(':')[1]
            extracted_valueBAT = float(value_partBAT.strip('V'))
            print(f' BATTERY : {extracted_valueBAT}')
            if extracted_valueBAT > 3.5 and extracted_valueBAT < 4.3:
                diciPay['BATTERY'] = 'True'
            else:
                diciPay['BATTERY'] = 'False'
        except:
            diciPay['BATTERY'] = 'False'
        # ----------------- RTC ----------
        try:
            input_stringRTC = result['RTC']
            value_partRTC = input_stringRTC.split(': ')[1]
            print(f' RTC : {value_partRTC}')
            if value_partRTC == '06/05/04 03:02:01':
                diciPay['RTC'] = 'True'
            else:
                diciPay['RTC'] = 'False'
        except:
            diciPay['RTC'] = 'False'
        # ----------------- FRAM ----------
        try:
            input_stringFRAM = result['FRAM']
            value_partFRAM = input_stringFRAM.split(': ')[1]
            print(f' FRAM : {value_partFRAM}')
            if value_partFRAM == 'OK':
                diciPay['FRAM'] = 'True'
            else:
                diciPay['FRAM'] = 'False'
        except:
            diciPay['FRAM'] = 'False'
        # ----------------- WIFI ----------
        try:
            input_stringWIFI = result['WIFI']
            value_partWIFI = input_stringWIFI.split(': ')[1]
            value_partWIFI = value_partWIFI.rstrip(' -> MAC')
            print(f' WIFI : {value_partWIFI}')
            if value_partWIFI == 'Ok':
                diciPay['WIFI'] = 'True'
            else:
                diciPay['WIFI'] = 'False'
        except:
            diciPay['WIFI'] = 'False'
        # ----------------- MQTT ----------
        try:
            input_stringMQTT = result['MQTT']
            value_partMQTT = input_stringMQTT.split(': ')[1]
            print(f' MQTT : {value_partMQTT}')
            if value_partMQTT == 'OK':
                diciPay['MQTT'] = 'True'
            else:
                diciPay['MQTT'] = 'False'
        except:
            diciPay['MQTT'] = 'False'
        # ----------------- Return ----------
        return diciPay

class TesteWorkerPl2(QThread):
    threadSignalPl2 = pyqtSignal(str)
    def __init__(self, parent=None, *args,):
        super(TesteWorkerPl2, self).__init__(parent)
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
        self.jf = jsonFiles.JsonFiles()
        self.mqtt_client = MqttClient(broker=self.diciParam["server"], client_id='102-jiga',username=self.diciParam["username"], password=self.diciParam["password"])
        self.value = ''
        self.diciPay = {}
        self.count = 0

    def run(self):
        # Do something...
        if (self.diciParam["placa2"] == True): #------------------------ PLACA 2 --------------------------------------
            logging.debug("Placa 2 ------------------------------")
            if not self.is_killed:
                try:
                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Inicia processo...")
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

                    while (True):
                        self.mqtt_client.connect()
                        self.value = self.mqtt_client.connectGota(self.diciParam, 'mac2', test={})

                        if not self.value == 'ERRO':
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> MAC: <font color='GreenYellow' size='3'>" +self.diciParam['mac2'] + "</font>")
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Serial Number: <font color='GreenYellow' size='3'>" + self.value + "</font>")
                            self.saveN2Reg(self.diciParam['mac2'], str(self.value))
                            break
                        else:
                            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> <font color='red' size='3'> Repetindo consulta ao GOTA!</font>")
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

            if not self.is_killed:

                print("Teste 2") #-------------- Desligar relê power, desligar relê flash, e ligar relê power
                self.cmdGpio.cmdReleCH2(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(500)
                self.cmdGpio.cmdReleCH2(0, 1, 1)
                QThread.msleep(3000)
                self.cmdGpio.cmdReleCH2(0, 1, 0)

                self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Iniciando teste via comandos")
                voltHP = self.cmdGpio.readVoltPl2(0)
                voltLP = self.cmdGpio.readVoltPl2(1)
                if voltHP > 3.0:
                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Tensão HP: " + str(voltHP) + "V <font color='white' size='3'>[OK]</font>")  # 1 = HP3.3v
                    logging.info("Tensão HP: " + str(voltHP)+"V")
                else:
                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Tensão HP: " + str(voltHP) + "V <font color='red' size='3'>[ERRO]</font>")  # 1 = HP3.3v
                    logging.info("Tensão HP: " + str(voltHP)+"V")
                if voltLP > 3.0:
                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Tensão LP: " + str(voltLP) + "V <font color='white' size='3'>[OK]</font>")  # 1 = HP3.3v
                    logging.info("Tensão LP: " + str(voltLP)+"V")
                else:
                    self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Tensão LP: " + str(voltLP) + "V <font color='red' size='3'>[ERRO]</font>")  # 1 = HP3.3v
                    logging.info("Tensão LP: " + str(voltLP)+"V")

                QThread.msleep(1000)
                self.cmdGpio.cmdReleCH2(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(1000)
                self.cmdGpio.cmdReleCH2(0, 1, 0)
                QThread.msleep(1000)

                for indice, valor in enumerate(self.cmdSerial.diciCommands.values(), start=1):
                    if indice == 1:
                        self.cmdSerial.returnSerial(self.diciParam['serial2'], '115200', str(valor))

                    if not self.is_killed:
                        self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Teste: "+str(valor))

                        rest = self.cmdSerial.returnSerial(self.diciParam['serial2'], '115200', str(valor))
                        logging.info(str(rest)+ " [OK]")
                        self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font><font color='white' size='3'> "+str(rest)+"</font>")

                        if valor == 'MAX':
                            self.diciPay['MAX'] = rest
                        elif valor == 'BME':
                            self.diciPay['BME'] = rest
                        elif valor == 'BATTERY':
                            self.diciPay['BATTERY'] = rest
                        elif valor == 'RTC':
                            self.diciPay['RTC'] = rest
                        elif valor == 'FRAM':
                            self.diciPay['FRAM'] = rest
                        elif valor == 'WIFI':
                            self.diciPay['WIFI'] = rest
                        elif valor == 'MQTT':
                            self.diciPay['MQTT'] = rest

                val = self.mountPay(self.diciPay)

                while (True):
                    self.mqtt_client.connect()
                    self.value = self.mqtt_client.connectGota(self.diciParam, 'mac2', test=val)

                    if not self.value == 'ERRO':
                        self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> MAC: <font color='GreenYellow' size='3'>" +self.diciParam['mac2'] + "</font>")
                        self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> Serial Number: <font color='GreenYellow' size='3'>" + self.value + "</font>")
                        self.saveN2Reg(self.diciParam['mac2'], str(self.value))
                        break

                    else:
                        self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> <font color='red' size='3'> Repetindo consulta ao GOTA!</font>")
                        self.count = self.count + 1

                    if self.count == 5:
                        self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font> <font color='red' size='3'> Erro Servidor GOTA!</font>")
                        self.saveN2Reg('0', '0')
                        self.count = 0
                        break

        if self.is_killed:
            self.threadSignalPl2.emit("<font color= 'SlateBlue' size='2'>[PLACA-2]</font><font color='red' size='3'> Processo finalizado!</font>\r\n")
            logging.info("Processo interrompido [INFO]")
            self.cmdGpio.cmdReleCH2(1, 1, 1)
        else:
            self.threadSignalPl2.emit('MAC2;' + self.diciNSerial['mac2'])
            self.cmdGpio.cmdReleCH2(1, 1, 1)
            self.threadSignalPl2.emit("FIM")

    def kill(self):
        self.is_killed = True

    def saveN2Reg(self, mac, serie):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        cfg.set('numeroserial',  'numero2', serie)
        cfg.set('numeroserial', 'mac2', mac)
        cfgfile = open('config.ini', 'w')
        cfg.write(cfgfile, space_around_delimiters=False)
        cfgfile.close()

    def mountPay(self, result):
        diciPay = {}
        # ----------------- MAX ----------
        try:
            input_stringMAX = result['MAX']
            value_partMAX = input_stringMAX.split()[1]
            value_partMAX = value_partMAX.rstrip('C')
            value_partMAX = value_partMAX.rstrip('*')
            extracted_valueMAX = float(value_partMAX)
            print(f' MAX : {extracted_valueMAX}')
            if extracted_valueMAX > 0 and extracted_valueMAX < 50:
                diciPay['MAX'] = 'True'
            else:
                diciPay['MAX'] = 'False'
        except:
            diciPay['MAX'] = 'False'
        # ----------------- BME ----------
        try:
            input_stringBME = result['BME']
            value_partBME = input_stringBME.split('||')[1]
            extracted_valueBME = float(value_partBME.strip().rstrip('%'))
            print(f' BME : {extracted_valueBME}')
            if extracted_valueBME == 0.00:
                diciPay['BME'] = 'False'
            else:
                diciPay['BME'] = 'True'
        except:
            diciPay['BME'] = 'True'
        # ----------------- BATTERY ----------
        try:
            input_stringBAT = result['BATTERY']
            value_partBAT = input_stringBAT.split(':')[1]
            extracted_valueBAT = float(value_partBAT.strip('V'))
            print(f' BATTERY : {extracted_valueBAT}')
            if extracted_valueBAT > 3.5 and extracted_valueBAT < 4.3:
                diciPay['BATTERY'] = 'True'
            else:
                diciPay['BATTERY'] = 'False'
        except:
            diciPay['BATTERY'] = 'False'
        # ----------------- RTC ----------
        try:
            input_stringRTC = result['RTC']
            value_partRTC = input_stringRTC.split(': ')[1]
            print(f' RTC : {value_partRTC}')
            if value_partRTC == '06/05/04 03:02:01':
                diciPay['RTC'] = 'True'
            else:
                diciPay['RTC'] = 'False'
        except:
            diciPay['RTC'] = 'False'
        # ----------------- FRAM ----------
        try:
            input_stringFRAM = result['FRAM']
            value_partFRAM = input_stringFRAM.split(': ')[1]
            print(f' FRAM : {value_partFRAM}')
            if value_partFRAM == 'OK':
                diciPay['FRAM'] = 'True'
            else:
                diciPay['FRAM'] = 'False'
        except:
            diciPay['FRAM'] = 'False'
        # ----------------- WIFI ----------
        try:
            input_stringWIFI = result['WIFI']
            value_partWIFI = input_stringWIFI.split(': ')[1]
            value_partWIFI = value_partWIFI.rstrip(' -> MAC')
            print(f' WIFI : {value_partWIFI}')
            if value_partWIFI == 'Ok':
                diciPay['WIFI'] = 'True'
            else:
                diciPay['WIFI'] = 'False'
        except:
            diciPay['WIFI'] = 'False'
        # ----------------- MQTT ----------
        try:
            input_stringMQTT = result['MQTT']
            value_partMQTT = input_stringMQTT.split(': ')[1]
            print(f' MQTT : {value_partMQTT}')
            if value_partMQTT == 'OK':
                diciPay['MQTT'] = 'True'
            else:
                diciPay['MQTT'] = 'False'
        except:
            diciPay['MQTT'] = 'False'
        # ----------------- Return ----------
        return diciPay

class TesteWorkerPl3(QThread):
    threadSignalPl3 = pyqtSignal(str)
    def __init__(self, parent=None, *args,):
        super(TesteWorkerPl3, self).__init__(parent)
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
        self.jf = jsonFiles.JsonFiles()
        self.mqtt_client = MqttClient(broker=self.diciParam["server"], client_id='001-jiga',
                                      username=self.diciParam["username"], password=self.diciParam["password"])
        self.value = ''
        self.diciPay = {}
        self.count = 0

    def run(self):
        # Do something...
        if (self.diciParam["placa3"] == True): #------------------------ PLACA 3 --------------------------------------
            logging.debug("Placa 3 ------------------------------")
            if not self.is_killed:
                try:
                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Inicia processo...")
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

                    while (True):
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
            if not self.is_killed:

                print("Teste 3") #-------------- Desligar relê power, desligar relê flash, e ligar relê power

                self.cmdGpio.cmdReleCH3(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(500)
                self.cmdGpio.cmdReleCH3(0, 1, 1)
                QThread.msleep(3000)
                self.cmdGpio.cmdReleCH3(0, 1, 0)

                self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Iniciando teste via comandos")
                voltHP = self.cmdGpio.readVoltPl3(0)
                voltLP = self.cmdGpio.readVoltPl3(1)
                if voltHP > 3.0:
                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Tensão HP: " + str(voltHP) + "V <font color='white' size='3'>[OK]</font>")  # 1 = HP3.3v
                    logging.info("Tensão HP: " + str(voltHP)+"V")
                else:
                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Tensão HP: " + str(voltHP) + "V <font color='red' size='3'>[ERRO]</font>")  # 1 = HP3.3v
                    logging.info("Tensão HP: " + str(voltHP)+"V")
                if voltLP > 3.0:
                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Tensão LP: " + str(voltLP) + "V <font color='white' size='3'>[OK]</font>")  # 1 = HP3.3v
                    logging.info("Tensão LP: " + str(voltLP)+"V")
                else:
                    self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Tensão LP: " + str(voltLP) + "V <font color='red' size='3'>[ERRO]</font>")  # 1 = HP3.3v
                    logging.info("Tensão LP: " + str(voltLP)+"V")

                QThread.msleep(1000)
                self.cmdGpio.cmdReleCH3(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(1000)
                self.cmdGpio.cmdReleCH3(0, 1, 0)
                QThread.msleep(1000)

                for indice, valor in enumerate(self.cmdSerial.diciCommands.values(), start=1):
                    if indice == 1:
                        self.cmdSerial.returnSerial(self.diciParam['serial3'], '115200', str(valor))
                    if not self.is_killed:
                        self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> Teste: "+str(valor))
                        rest = self.cmdSerial.returnSerial(self.diciParam['serial3'], '115200', str(valor))

                        logging.info(str(rest)+ " [OK]")
                        self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font><font color='white' size='3'> "+str(rest)+"</font>")

                        if valor == 'MAX':
                            self.diciPay['MAX'] = rest
                        elif valor == 'BME':
                            self.diciPay['BME'] = rest
                        elif valor == 'BATTERY':
                            self.diciPay['BATTERY'] = rest
                        elif valor == 'RTC':
                            self.diciPay['RTC'] = rest
                        elif valor == 'FRAM':
                            self.diciPay['FRAM'] = rest
                        elif valor == 'WIFI':
                            self.diciPay['WIFI'] = rest
                        elif valor == 'MQTT':
                            self.diciPay['MQTT'] = rest

                val = self.mountPay(self.diciPay)

                while (True):
                    self.mqtt_client.connect()
                    self.value = self.mqtt_client.connectGota(self.diciParam, 'mac3', test=val)

                    if not self.value == 'ERRO':
                        self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font> MAC: <font color='GreenYellow' size='3'>" + self.diciParam['mac3'] + "</font>")
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

        if self.is_killed:
            self.threadSignalPl3.emit("<font color= 'SkyBlue' size='2'>[PLACA-3]</font><font color='red' size='3'> Processo finalizado!</font>\r\n")
            logging.info("Processo interrompido [INFO]")
            self.cmdGpio.cmdReleCH3(1, 1, 1)
        else:
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

    def mountPay(self, result):
        diciPay = {}
        # ----------------- MAX ----------
        try:
            input_stringMAX = result['MAX']
            value_partMAX = input_stringMAX.split()[1]
            value_partMAX = value_partMAX.rstrip('C')
            value_partMAX = value_partMAX.rstrip('*')
            extracted_valueMAX = float(value_partMAX)
            print(f' MAX : {extracted_valueMAX}')
            if extracted_valueMAX > 0 and extracted_valueMAX < 50:
                diciPay['MAX'] = 'True'
            else:
                diciPay['MAX'] = 'False'
        except:
            diciPay['MAX'] = 'False'
        # ----------------- BME ----------
        try:
            input_stringBME = result['BME']
            value_partBME = input_stringBME.split('||')[1]
            extracted_valueBME = float(value_partBME.strip().rstrip('%'))
            print(f' BME : {extracted_valueBME}')
            if extracted_valueBME == 0.00:
                diciPay['BME'] = 'False'
            else:
                diciPay['BME'] = 'True'
        except:
            diciPay['BME'] = 'True'
        # ----------------- BATTERY ----------
        try:
            input_stringBAT = result['BATTERY']
            value_partBAT = input_stringBAT.split(':')[1]
            extracted_valueBAT = float(value_partBAT.strip('V'))
            print(f' BATTERY : {extracted_valueBAT}')
            if extracted_valueBAT > 3.5 and extracted_valueBAT < 4.3:
                diciPay['BATTERY'] = 'True'
            else:
                diciPay['BATTERY'] = 'False'
        except:
            diciPay['BATTERY'] = 'False'
        # ----------------- RTC ----------
        try:
            input_stringRTC = result['RTC']
            value_partRTC = input_stringRTC.split(': ')[1]
            print(f' RTC : {value_partRTC}')
            if value_partRTC == '06/05/04 03:02:01':
                diciPay['RTC'] = 'True'
            else:
                diciPay['RTC'] = 'False'
        except:
            diciPay['RTC'] = 'False'
        # ----------------- FRAM ----------
        try:
            input_stringFRAM = result['FRAM']
            value_partFRAM = input_stringFRAM.split(': ')[1]
            print(f' FRAM : {value_partFRAM}')
            if value_partFRAM == 'OK':
                diciPay['FRAM'] = 'True'
            else:
                diciPay['FRAM'] = 'False'
        except:
            diciPay['FRAM'] = 'False'
        # ----------------- WIFI ----------
        try:
            input_stringWIFI = result['WIFI']
            value_partWIFI = input_stringWIFI.split(': ')[1]
            value_partWIFI = value_partWIFI.rstrip(' -> MAC')
            print(f' WIFI : {value_partWIFI}')
            if value_partWIFI == 'Ok':
                diciPay['WIFI'] = 'True'
            else:
                diciPay['WIFI'] = 'False'
        except:
            diciPay['WIFI'] = 'False'
        # ----------------- MQTT ----------
        try:
            input_stringMQTT = result['MQTT']
            value_partMQTT = input_stringMQTT.split(': ')[1]
            print(f' MQTT : {value_partMQTT}')
            if value_partMQTT == 'OK':
                diciPay['MQTT'] = 'True'
            else:
                diciPay['MQTT'] = 'False'
        except:
            diciPay['MQTT'] = 'False'
        # ----------------- Return ----------
        return diciPay

class TesteWorkerPl4(QThread):
    threadSignalPl4 = pyqtSignal(str)
    def __init__(self, parent=None, *args,):
        super(TesteWorkerPl4, self).__init__(parent)
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
        self.jf = jsonFiles.JsonFiles()
        self.mqtt_client = MqttClient(broker=self.diciParam["server"], client_id='104-jiga',
                                      username=self.diciParam["username"], password=self.diciParam["password"])
        self.value = ''
        self.diciPay = {}
        self.count = 0

    def run(self):
        # Do something...
        if (self.diciParam["placa4"] == True): #------------------------ PLACA 4 --------------------------------------
            logging.debug("Placa 4 ------------------------------")
            if not self.is_killed:
                try:
                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Inicia processo...")

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

                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> " + nameFirm)

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
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> "+result1)
                            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Erro de gravação firmware <font color='red' size='3'>[ERRO]</font>")
                            logging.error("Erro de gravação firmware placa 4 [ERRO]")
                            self.is_killed = True
                print(result1)
            if not self.is_killed:

                print("Teste 1") #-------------- Desligar relê power, desligar relê flash, e ligar relê power
                #QThread.msleep(500)
                self.cmdGpio.cmdReleCH4(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(500)
                self.cmdGpio.cmdReleCH4(0, 1, 1)
                QThread.msleep(5000)
                self.cmdGpio.cmdReleCH4(0, 1, 0)

                self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Iniciando teste via comandos")
                voltHP = self.cmdGpio.readVoltPl4(0)
                voltLP = self.cmdGpio.readVoltPl4(1)
                if voltHP > 3.0:
                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Tensão HP: " + str(voltHP) + "V <font color='white' size='3'>[OK]</font>")  # 1 = HP3.3v
                    logging.info("Tensão HP: " + str(voltHP)+"V")
                else:
                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Tensão HP: " + str(voltHP) + "V <font color='red' size='3'>[ERRO]</font>")  # 1 = HP3.3v
                    logging.info("Tensão HP: " + str(voltHP)+"V")
                if voltLP > 3.0:
                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Tensão LP: " + str(voltLP) + "V <font color='white' size='3'>[OK]</font>")  # 1 = HP3.3v
                    logging.info("Tensão LP: " + str(voltLP)+"V")
                else:
                    self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4]</font> Tensão LP: " + str(voltLP) + "V <font color='red' size='3'>[ERRO]</font>")  # 1 = HP3.3v
                    logging.info("Tensão LP: " + str(voltLP)+"V")

                QThread.msleep(1000)
                self.cmdGpio.cmdReleCH4(1, 1, 1)  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
                QThread.msleep(1000)
                self.cmdGpio.cmdReleCH4(0, 1, 0)
                QThread.msleep(1000)

                for indice, valor in enumerate(self.cmdSerial.diciCommands.values(), start=1):
                    if indice == 1:
                        self.cmdSerial.returnSerial(self.diciParam['serial4'], '115200', str(valor))
                    if not self.is_killed:
                        self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4] </font>Teste: "+str(valor))
                        #list = self.cmdSerial.writePort(self.diciParam['serial4'], '115200', str(i))
                        rest = self.cmdSerial.returnSerial(self.diciParam['serial4'], '115200', str(valor))

                        logging.info(str(rest)+ " [OK]")
                        self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4] </font><font color='white' size='3'>"+str(rest)+"</font>")

                        if valor == 'MAX':
                            self.diciPay['MAX'] = rest
                        elif valor == 'BME':
                            self.diciPay['BME'] = rest
                        elif valor == 'BATTERY':
                            self.diciPay['BATTERY'] = rest
                        elif valor == 'RTC':
                            self.diciPay['RTC'] = rest
                        elif valor == 'FRAM':
                            self.diciPay['FRAM'] = rest
                        elif valor == 'WIFI':
                            self.diciPay['WIFI'] = rest
                        elif valor == 'MQTT':
                            self.diciPay['MQTT'] = rest

                val = self.mountPay(self.diciPay)

                while (True):
                    self.mqtt_client.connect()
                    self.value = self.mqtt_client.connectGota(self.diciParam, 'mac4', test=val)

                    if not self.value == 'ERRO':
                        self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4] </font>MAC: <font color='GreenYellow' size='3'>" +self.diciParam['mac4'] + "</font>")
                        self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4] </font>Serial Number: <font color='GreenYellow' size='3'>" + self.value + "</font>")
                        self.saveN4Reg(self.diciParam['mac4'], str(self.value))
                        break
                    else:
                        self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4] </font> <font color='red' size='3'>Repetindo consulta ao GOTA!</font>")
                        self.count = self.count + 1

                    if self.count == 5:
                        self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4] </font> <font color='red' size='3'>Erro Servidor GOTA!</font>")
                        self.saveN4Reg('0', '0')
                        self.count = 0
                        break


        if self.is_killed:
            self.threadSignalPl4.emit("<font color= 'Goldenrod' size='2'>[PLACA-4] </font><font color='red' size='3'>Processo finalizado!</font>\r\n")
            logging.info("Processo interrompido [INFO]")
            self.cmdGpio.cmdReleCH1(1, 1, 1)
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

    def mountPay(self, result):
        diciPay = {}
        # ----------------- MAX ----------
        try:
            input_stringMAX = result['MAX']
            value_partMAX = input_stringMAX.split()[1]
            value_partMAX = value_partMAX.rstrip('C')
            value_partMAX = value_partMAX.rstrip('*')
            extracted_valueMAX = float(value_partMAX)
            print(f' MAX : {extracted_valueMAX}')
            if extracted_valueMAX > 0 and extracted_valueMAX < 50:
                diciPay['MAX'] = 'True'
            else:
                diciPay['MAX'] = 'False'
        except:
            diciPay['MAX'] = 'False'
        # ----------------- BME ----------
        try:
            input_stringBME = result['BME']
            value_partBME = input_stringBME.split('||')[1]
            extracted_valueBME = float(value_partBME.strip().rstrip('%'))
            print(f' BME : {extracted_valueBME}')
            if extracted_valueBME == 0.00:
                diciPay['BME'] = 'False'
            else:
                diciPay['BME'] = 'True'
        except:
            diciPay['BME'] = 'True'
        # ----------------- BATTERY ----------
        try:
            input_stringBAT = result['BATTERY']
            value_partBAT = input_stringBAT.split(':')[1]
            extracted_valueBAT = float(value_partBAT.strip('V'))
            print(f' BATTERY : {extracted_valueBAT}')
            if extracted_valueBAT > 3.5 and extracted_valueBAT < 4.3:
                diciPay['BATTERY'] = 'True'
            else:
                diciPay['BATTERY'] = 'False'
        except:
            diciPay['BATTERY'] = 'False'
        # ----------------- RTC ----------
        try:
            input_stringRTC = result['RTC']
            value_partRTC = input_stringRTC.split(': ')[1]
            print(f' RTC : {value_partRTC}')
            if value_partRTC == '06/05/04 03:02:01':
                diciPay['RTC'] = 'True'
            else:
                diciPay['RTC'] = 'False'
        except:
            diciPay['RTC'] = 'False'
        # ----------------- FRAM ----------
        try:
            input_stringFRAM = result['FRAM']
            value_partFRAM = input_stringFRAM.split(': ')[1]
            print(f' FRAM : {value_partFRAM}')
            if value_partFRAM == 'OK':
                diciPay['FRAM'] = 'True'
            else:
                diciPay['FRAM'] = 'False'
        except:
            diciPay['FRAM'] = 'False'
        # ----------------- WIFI ----------
        try:
            input_stringWIFI = result['WIFI']
            value_partWIFI = input_stringWIFI.split(': ')[1]
            value_partWIFI = value_partWIFI.rstrip(' -> MAC')
            print(f' WIFI : {value_partWIFI}')
            if value_partWIFI == 'Ok':
                diciPay['WIFI'] = 'True'
            else:
                diciPay['WIFI'] = 'False'
        except:
            diciPay['WIFI'] = 'False'
        # ----------------- MQTT ----------
        try:
            input_stringMQTT = result['MQTT']
            value_partMQTT = input_stringMQTT.split(': ')[1]
            print(f' MQTT : {value_partMQTT}')
            if value_partMQTT == 'OK':
                diciPay['MQTT'] = 'True'
            else:
                diciPay['MQTT'] = 'False'
        except:
            diciPay['MQTT'] = 'False'
        # ----------------- Return ----------
        return diciPay

class TelaTeste(QMainWindow):
    def __init__(self, parent=None):
        super(TelaTeste, self).__init__(parent)
        self.ui = Ui_MainWindowTeste()
        self.ui.setupUi(self)

        self.diciSerialStat = {}
        self.diciPlacas = {}
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini')

        self.ui.textEditLog.clear()
        self.ui.textEditLog.setStyleSheet('background-color: black; font: bold 14px; color: green')
        self.ui.textEditLog.append("Log iniciado!!!")
        #self.ui.textEditLog.append("Último número de série gravado: <font color='white' size='3'>"+self.cfg.get('numeroserial', 'registro')+"</font>")

        self.ui.checkBox1.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/pcb_off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/pcb_on.png);margin-left: 5%;}')
        self.ui.checkBox2.setStyleSheet('QCheckBox {spacing: 10px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/pcb_off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/pcb_on.png);margin-left: 5%;}')
        self.ui.checkBox3.setStyleSheet('QCheckBox {spacing: 10px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/pcb_off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/pcb_on.png);margin-left: 5%;}')
        self.ui.checkBox4.setStyleSheet('QCheckBox {spacing: 10px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/pcb_off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/pcb_on.png);margin-left: 5%;}')

        self.ui.checkBox1.clicked.connect(lambda: self.clickBox(self.ui.checkBox1.isChecked(), "1"))
        self.ui.checkBox2.clicked.connect(lambda: self.clickBox(self.ui.checkBox2.isChecked(), "2"))
        self.ui.checkBox3.clicked.connect(lambda: self.clickBox(self.ui.checkBox3.isChecked(), "3"))
        self.ui.checkBox4.clicked.connect(lambda: self.clickBox(self.ui.checkBox4.isChecked(), "4"))

        self.ui.checkBoxConex.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')
        self.ui.checkBoxCalib.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')
        self.ui.checkBoxProd.setStyleSheet('QCheckBox {spacing: 100px;} QCheckBox::indicator {width: 60px;height:60px;}QCheckBox::indicator:unchecked{image: url(./designer/img/switch-off.png);margin-left: 5%; } QCheckBox::indicator:checked{image: url(./designer/img/switch-on.png);margin-left: 5%;}')

        self.ui.checkBoxConex.clicked.connect(lambda: self.clickBoxSelect(self.ui.checkBoxConex.isChecked(), "S1"))
        self.ui.checkBoxCalib.clicked.connect(lambda: self.clickBoxSelect(self.ui.checkBoxCalib.isChecked(), "S2"))
        self.ui.checkBoxProd.clicked.connect(lambda: self.clickBoxSelect(self.ui.checkBoxProd.isChecked(), "S3"))

        self.ui.btnStart.clicked.connect(self.startTest)
        self.ui.btnStop.clicked.connect(self.stopTest)
        self.ui.btnClear.clicked.connect(self.clearTexts)

        self.readParam()
        if (self.diciSerialStat["stat1"] == "0"):
            self.ui.labelP1.setStyleSheet('color: red')
        else: self.ui.checkBox1.setChecked(True)
        if (self.diciSerialStat["stat2"] == "0" ):
            self.ui.labelP2.setStyleSheet('color: red')
        else: self.ui.checkBox2.setChecked(True)
        if (self.diciSerialStat["stat3"] == "0" ):
            self.ui.labelP3.setStyleSheet('color: red')
        else: self.ui.checkBox3.setChecked(True)
        if (self.diciSerialStat["stat4"] == "0" ):
            self.ui.labelP4.setStyleSheet('color: red')
        else: self.ui.checkBox4.setChecked(True)

        self.diciPlacas["modeRec"] = "OFF"
        self.zeraNS()
        self.cmdGpioMax = gpioControl.GpioAdsControl()

    def clickBox(self, state, ref):
        if state :
            if (ref == "1"):
                if self.validaSerial(ref):
                    self.alertaSerial("Serial 1 desativada!")
                    self.ui.checkBox1.setChecked(False)
                else:
                    self.ui.textEditLog.append("Placa "+ref+" ON...")
            if (ref == "2"):
                if self.validaSerial(ref):
                    self.alertaSerial("Serial 2 desativada!")
                    self.ui.checkBox2.setChecked(False)
                else:
                    self.ui.textEditLog.append("Placa "+ref+" ON...")
            if (ref == "3"):
                if self.validaSerial(ref):
                    self.alertaSerial("Serial 3 desativada!")
                    self.ui.checkBox3.setChecked(False)
                else:
                    self.ui.textEditLog.append("Placa "+ref+" ON...")
            if (ref == "4"):
                if self.validaSerial(ref):
                    self.alertaSerial("Serial 4 desativada!")
                    self.ui.checkBox4.setChecked(False)
                else:
                    self.ui.textEditLog.append("Placa "+ref+" ON...")
        else:
            self.ui.textEditLog.append("Placa "+ref+" OFF...")

    def clickBoxSelect(self, state, ref):

        if (ref == "S1"):
            if state:
                self.ui.checkBoxCalib.setChecked(False)
                self.ui.checkBoxProd.setChecked(False)
                self.diciPlacas["modeRec"] = "CONE_ON"

        if (ref == "S2"):
            if state:
                self.ui.checkBoxConex.setChecked(False)
                self.ui.checkBoxProd.setChecked(False)
                self.diciPlacas["modeRec"] = "CALI_ON"

        if (ref == "S3"):
            if state:
                self.ui.checkBoxConex.setChecked(False)
                self.ui.checkBoxCalib.setChecked(False)
                self.diciPlacas["modeRec"] = "PROD_ON"

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
            self.origem = main.Tela()
            self.origem.show()
        else:
            event.ignore()

    def clearTexts(self):
        self.ui.textEditLog.clear()

    def startTest(self):
        try:
            if self.workrTeste.isRunning():
                self.ui.textEditLog.append("<font color='red' size='3'>Processo em andamento...</font>\r\n")
            else:
                breakpoint(exit())

        except:
            self.ui.textEditLog.clear()
            self.ui.textEditLog.append("Log iniciado!!!")
            cfg = configparser.ConfigParser()
            cfg.read('config.ini')
            val = cfg.get('numeroserial', 'registro')
            #self.ui.textEditLog.append("Último número de série gravado: <font color='white' size='3'>" + val + "</font>")

            if (not self.ui.checkBox1.isChecked() and
                    not self.ui.checkBox2.isChecked() and
                    not self.ui.checkBox3.isChecked() and
                    not self.ui.checkBox4.isChecked()):
                 self.alertaSerial("Atenção selecione uma ou mias placas")
            else:
                self.ui.textEditLog.append("Iniciando testes....")
                self.diciPlacas["esptoolFlash"] = cfg.get('firmware', 'esptoolFlash')

                self.diciPlacas["placa1"] = self.ui.checkBox1.isChecked()
                self.diciPlacas["serial1"] = self.diciSerialStat["serial1"]
                self.diciPlacas["baudrate1"] = self.diciSerialStat["baudrate1"]
                self.diciPlacas["name1"] = cfg.get('firmware', 'name1')
                self.diciPlacas["mem1"] = cfg.get('memoria', 'end1')
                self.diciPlacas["path1"] = cfg.get('firmware', 'path1')
                self.diciPlacas["mac1"] = '0'

                self.diciPlacas["placa2"] = self.ui.checkBox2.isChecked()
                self.diciPlacas["serial2"] = self.diciSerialStat["serial2"]
                self.diciPlacas["baudrate2"] = self.diciSerialStat["baudrate2"]
                self.diciPlacas["name2"] = cfg.get('firmware', 'name2')
                self.diciPlacas["mem2"] = cfg.get('memoria', 'end2')
                self.diciPlacas["path2"] = cfg.get('firmware', 'path2')
                self.diciPlacas["mac2"] = '0'

                self.diciPlacas["placa3"] = self.ui.checkBox3.isChecked()
                self.diciPlacas["serial3"] = self.diciSerialStat["serial3"]
                self.diciPlacas["baudrate3"] = self.diciSerialStat["baudrate3"]
                self.diciPlacas["name3"] = cfg.get('firmware', 'name3')
                self.diciPlacas["mem3"] = cfg.get('memoria', 'end3')
                self.diciPlacas["path3"] = cfg.get('firmware', 'path3')
                self.diciPlacas["mac3"] = '0'

                self.diciPlacas["placa4"] = self.ui.checkBox4.isChecked()
                self.diciPlacas["serial4"] = self.diciSerialStat["serial4"]
                self.diciPlacas["baudrate4"] = self.diciSerialStat["baudrate4"]
                self.diciPlacas["name4"] = cfg.get('firmware', 'name4')
                self.diciPlacas["mem4"] = cfg.get('memoria', 'end4')
                self.diciPlacas["path4"] = cfg.get('firmware', 'path4')
                self.diciPlacas["mac4"] = '0'

                self.diciPlacas["nserial"] = cfg.get('numeroserial', 'registro')

                self.diciPlacas["server"] = cfg.get('mqtt', 'server')
                self.diciPlacas["port"] = cfg.get('mqtt', 'port')
                self.diciPlacas["qos"] = cfg.get('mqtt', 'qos')
                self.diciPlacas["username"] = cfg.get('mqtt', 'username')
                self.diciPlacas["password"] = cfg.get('mqtt', 'password')
                self.diciPlacas["topicpub"] = cfg.get('mqtt', 'topicpub')
                self.diciPlacas["topicsub"] = cfg.get('mqtt', 'topicsub')

                self.cmdGpioMax.cmdReleIN(0,1)

                if self.diciPlacas["placa1"]:
                    print("Thread placa 1 on")
                    self.startThreadPl1(self.diciPlacas)
                if self.diciPlacas["placa2"]:
                    print("Thread placa 2 on")
                    self.startThreadPl2(self.diciPlacas)
                if self.diciPlacas["placa3"]:
                    print("Thread placa 3 on")
                    self.startThreadPl3(self.diciPlacas)
                if self.diciPlacas["placa4"]:
                    print("Thread placa 4 on")
                    self.startThreadPl4(self.diciPlacas)

    def stopTest(self):
        try:
            if self.workrTeste.isRunning():
                self.ui.textEditLog.append("<font color='red' size='3'>Parando processo...</font>\r\n")
                self.workrTeste.kill()
            if self.workrTeste2.isRunning():
                self.ui.textEditLog.append("<font color='red' size='3'>Parando processo...</font>\r\n")
                self.workrTeste2.kill()
            if self.workrTeste3.isRunning():
                self.ui.textEditLog.append("<font color='red' size='3'>Parando processo...</font>\r\n")
                self.workrTeste3.kill()
            if self.workrTeste4.isRunning():
                self.ui.textEditLog.append("<font color='red' size='3'>Parando processo...</font>\r\n")
                self.workrTeste4.kill()
        except:
            self.ui.textEditLog.append("<font color='red' size='3'>Processo finalizado!</font>\r\n")

    def readParam(self):
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
        #self.cfg.close()

    def validaSerial(self, ref):
        if (self.diciSerialStat["stat1"] == "0" and ref == "1"):
            return True
        if (self.diciSerialStat["stat2"] == "0" and ref == "2"):
            return True
        if (self.diciSerialStat["stat3"] == "0" and ref == "3"):
            return True
        if (self.diciSerialStat["stat4"] == "0" and ref == "4"):
            return True

    def alertaSerial(self, msg):
        userInfo = QMessageBox.information(self, "Ação Proibida", msg, QMessageBox.Ok)
        if userInfo == QMessageBox.Ok:
            return True

    def startThreadPl1(self, param):
        self.workrTeste = TesteWorkerPl1(self, param)
        self.workrTeste.threadSignalPl1.connect(self.on_threadSignalPl1)
        self.workrTeste.start()

    def on_threadSignalPl1(self, inf):
        print('PLACA 1 MAC '+ str(inf))
        x = inf.split(';')
        if(x[0] == 'MAC1'):
            self.diciPlacas["mac1"] = x[1]
            self.atualizarNSMac(self.diciPlacas)
        if (inf == "FIM"):
            print("FIM")
        else:
            self.ui.textEditLog.append(str(inf))

    def startThreadPl2(self, param):
        self.workrTeste2 = TesteWorkerPl2(self, param)
        self.workrTeste2.threadSignalPl2.connect(self.on_threadSignalPl2)
        self.workrTeste2.start()

    def on_threadSignalPl2(self, inf):
        print('PLACA 2 MAC ' + str(inf))
        x = inf.split(';')
        if (x[0] == 'MAC2'):
            self.diciPlacas["mac2"] = x[1]
            self.atualizarNSMac(self.diciPlacas)
        if (inf == "FIM"):
            print("FIM")
        else:
            self.ui.textEditLog.append(str(inf))

    def startThreadPl3(self, param):
        self.workrTeste3 = TesteWorkerPl3(self, param)
        self.workrTeste3.threadSignalPl3.connect(self.on_threadSignalPl3)
        self.workrTeste3.start()

    def on_threadSignalPl3(self, inf):
        print('PLACA 3 MAC ' + str(inf))
        x = inf.split(';')
        if (x[0] == 'MAC3'):
            self.diciPlacas["mac3"] = x[1]
            print("self.diciPlacas[mac3]")
            print(self.diciPlacas["mac3"])
            self.atualizarNSMac(self.diciPlacas)

        if (inf == "FIM"):
            print("FIM")

        else:
            self.ui.textEditLog.append(str(inf))

    def startThreadPl4(self, param):
        self.workrTeste4 = TesteWorkerPl4(self, param)
        self.workrTeste4.threadSignalPl4.connect(self.on_threadSignalPl4)
        self.workrTeste4.start()

    def on_threadSignalPl4(self, inf):
        x = inf.split(';')
        if (x[0] == 'MAC4'):
            self.diciPlacas["mac4"] = x[1]
            self.atualizarNSMac(self.diciPlacas)

        if (inf == "FIM"):
            pass
        else:
            self.ui.textEditLog.append(str(inf))

    def tNumero(self, param):
        self.telaIdMac = guiIdMac.TelaIdMac(param)
        self.telaIdMac.displayShow()

    def tGrav(self, param):
        self.telaGrvacao = guiGravacao.TelaGravacao(param)
        self.telaGrvacao.displayShow()
        self.hide()

    def saveNRegFile(self, op, mac, serie):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        if op == 1:
            cfg.set('numeroserial',  'numero1', serie)
            cfg.set('numeroserial', 'mac1', mac)
        if op == 2:
            cfg.set('numeroserial',  'numero2', serie)
            cfg.set('numeroserial', 'mac2', mac)
        if op == 3:
            cfg.set('numeroserial',  'numero3', serie)
            cfg.set('numeroserial', 'mac3', mac)
        if op == 4:
            cfg.set('numeroserial',  'numero4', serie)
            cfg.set('numeroserial', 'mac4', mac)
        cfgfile = open('config.ini', 'w')
        cfg.write(cfgfile, space_around_delimiters=False)
        cfgfile.close()

    def atualizarNSMac(self, param):
        print("Número serial início "+str(param['nserial']))
        distStatus = {}
        cond = False
        if param['placa1']:
            if self.workrTeste.isRunning():
                distStatus['placa1'] = "Running"
            elif self.workrTeste.isFinished():
                distStatus['placa1'] = "Finished"
        else:
            distStatus['placa1'] = "Disable"

        if param['placa2']:
            if self.workrTeste2.isRunning():
                distStatus['placa2'] = "Running"
            elif self.workrTeste2.isFinished():
                distStatus['placa2'] = "Finished"
        else:
            distStatus['placa2'] = "Disable"

        if param['placa3']:
            if self.workrTeste3.isRunning():
                distStatus['placa3'] = "Running"
            elif self.workrTeste3.isFinished():
                distStatus['placa3'] = "Finished"
        else:
            distStatus['placa3'] = "Disable"

        if param['placa4']:
            if self.workrTeste4.isRunning():
                distStatus['placa4'] = "Running"
            if self.workrTeste4.isFinished():
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
            #print(self.diciPlacas)
            #print(self.diciPlacas["modeRec"])
            if not self.diciPlacas["modeRec"] == 'OFF':
                self.tGrav(self.diciPlacas)
            else:
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
