import configparser
import serial
import time
from PyQt5.QtCore import QThread

class CommdTest():
    def __init__(self):
        print("Command Test")
        self.diciCommands = {}
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini')

        self.diciCommands['max'] = self.cfg.get('commandtest', 'max')
        self.diciCommands['bme'] = self.cfg.get('commandtest', 'bme')
        self.diciCommands['battery'] = self.cfg.get('commandtest', 'battery')
        self.diciCommands['rtc'] = self.cfg.get('commandtest', 'rtc')
        self.diciCommands['fram'] = self.cfg.get('commandtest', 'fram')
        #self.diciCommands['display'] = self.cfg.get('commandtest', 'display')
        #self.diciCommands['buzzer'] = self.cfg.get('commandtest', 'buzzer')
        self.diciCommands['wifi'] = self.cfg.get('commandtest', 'wifi')
        self.diciCommands['mqtt'] = self.cfg.get('commandtest', 'mqtt')

        print(self.diciCommands)

    def verifyPort(self, port):
        try:
            objVerify = serial.Serial(port)
            if objVerify:
                return True
        except serial.SerialException:
            return False

    # Função para enviar e receber comandos
    def enviar_e_receber_comandos(self, ser, comandos):
        for cmd in comandos:
            print(cmd)
            buffer = []
            ser.write(bytearray(str(cmd)+"\n", "ascii"))

            while (True):
                resposta = ser.readline()
                print(resposta)
                buffer.append(resposta)
                print(buffer)
                #print(f"Comando: {cmd.decode().strip()}, Resposta: {resposta.decode().strip()}")
                time.sleep(1)  # Pausa entre os comandos
            time.sleep(1)

    def cmdSendRecSerial(self, port, baud, cmd):
       # Abre a porta serial
        count = 0
        buffer = []
        with serial.Serial(port, baud, timeout=1) as ser:
            if ser.is_open:
                print(f"Conectado à porta {port} com sucesso.")
                try:
                    for commad in cmd.values():
                        print('commad')
                        print(commad)
                        #self.enviar_e_receber_comandos(ser, cmd.values())
                        ser.write(bytearray(str(commad)+"\n", "ascii"))
                        while (True):
                            response = ser.readline()
                            buffer.append(response)
                            if (response == b'Aguardando comando...\r\r\n'):
                                break
                            if count >= 100:
                                break
                            time.sleep(3)
                            count = count+1
                        print(buffer)
                        del buffer[:]
                except KeyboardInterrupt:
                    pass  # Interrompe a execução com Ctrl+C

        print("Conexão encerrada.")

    def writePort(self, port, baud, cmd):
        print('writePort')
        buffer = []
        print('cmd')
        print(cmd)
        time.sleep(2)
        count = 0
        try:
            Obj_porta = serial.Serial(port, baud, timeout=10)
            time.sleep(1)
            Obj_porta.write(bytearray(cmd+"\n", "ascii"))
            while(True):
                response = Obj_porta.readline() # Currently stops reading on timeout...
                if count >= 25 and cmd != 'WIFI' and cmd != 'MQTT':
                    print("Erro contagem > 25...")
                    count = 0
                    Obj_porta.close()
                    return 'Erro'
                if response:
                    buffer.append(response)
                    if(response == b'MQTT_BROKER: OK\r\r\n'):
                        break
                    elif(response == b'MQTT_BROKER: Erro de conex\xc3\xa3o\r\r\n'):
                        del buffer[:]
                        buffer.append(response)
                        break
                    elif(response == b'Wi-Fi: Erro de conex\xc3\xa3o\r\r\n'):
                        del buffer[:]
                        buffer.append(response)
                        break
                    elif(response == b'Aguardando comando...\r\r\n'):
                        break
                count = count+1
            Obj_porta.close()
            print("buffer")
            return buffer

        except serial.SerialException:
            print("ERRO: Verifique se ha algum dispositivo conectado na porta!")
            return 'Erro'

    def returnSerial(self, port, baud, cmd):
        print('returnSerial')
        if (cmd == 'BME'):
            result = self.writePort(port, baud, cmd)
            if result != 'Erro':
                if result[0] == b'Aguardando comando...\r\r\n':
                    result = self.writePort(port, baud, cmd)
                    print(type(result))
                    print(result)
                    val = str(result[2].strip().decode("utf-8"))
                    return val
                else:
                    print(type(result))
                    print(result)
                    val = str(result[2].strip().decode("utf-8"))
                    return val
            else:
                print('Repetindo o teste')

        elif (cmd == 'DISPLAY'):
            result = self.writePort(port, baud, cmd)
            if result != 'Erro':
                val = result[3].strip().decode("utf-8") + "," + result[4].strip().decode("utf-8") + "," + result[5].strip().decode("utf-8")
                return val

        elif (cmd == 'BUZ'):
            result = self.writePort(port, baud, cmd)
            if result != 'Erro':
                return 'Buzzer...'

        elif (cmd == 'MAX'):
            #print('MAX*****************')
            result = self.writePort(port, baud, cmd)
            print(result)
            if result != 'Erro':
                try:
                    #print("MAX 1**********************")
                    val = str(result[2].strip().decode("utf-8"))
                    return val
                except:
                    #print("MAX 2**********************")
                    val = result[0].strip().decode("utf-8")
                    return val

        elif (cmd == 'WIFI'):
            result = self.writePort(port, baud, cmd)
            if result[0] == b'Wi-Fi: Erro de conex\xc3\xa3o\r\r\n':
                return 'Erro Conexão WIFI'
            if result != 'Erro':
                try:
                    val = result[41].strip().decode("utf-8")
                    return val
                except:
                    val = result[0].strip().decode("utf-8")
                    return val

        elif (cmd == 'MQTT'):
            result = self.writePort(port, baud, cmd)
            if result[0] == b'MQTT_BROKER: Erro de conex\xc3\xa3o\r\r\n':
                return 'Erro Conexão MQTT'
            print("result MQTT")
            print(result)
            if result != 'Erro':
                try:
                    val = str(result[2].strip().decode("utf-8"))
                    return val
                except:
                    val = result[0].strip().decode("utf-8")
                    return val

        elif (cmd == 'RTC'):
            result = self.writePort(port, baud, cmd)
            if result != 'Erro':
                val = str(result[2].strip().decode("utf-8"))
                return val

        elif (cmd == 'FRAM'):
            result = self.writePort(port, baud, cmd)
            if result != 'Erro':
                val = str(result[2].strip().decode("utf-8"))
                return val

        elif (cmd == 'BATTERY'):
            result = self.writePort(port, baud, cmd)
            if result != 'Erro':
                val = str(result[2].strip().decode("utf-8"))
                return val

if __name__ == '__main__':
    cTest = CommdTest()
    cTest.cmdSendRecSerial('/dev/ttyUSB0', 115200, cTest.diciCommands)

    #print(cTest.timeOut(10))
    #if cTest.verifyPort('COM7'):
        #print('Porta OK')
    #else:
        #print('Porta Erro!')
    """for i in cTest.diciCommands.values(): #keys() or value()
        list = cTest.writePort('COM7', '115200', str(i))
        print(list)
        time.sleep(1)"""
    #list = cTest.writePort('/dev/ttyUSB0', '115200', 'WIFI')
    #print(list)
    #time.sleep(1)
    #list = cTest.writePort('/dev/ttyUSB0', '115200', 'MQTT')
    #print(list)
    #time.sleep(1)
