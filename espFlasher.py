import configparser
import os
import subprocess
from datetime import time
#from subprocess import Popen, PIPE
import subprocess, signal, time
import esptool
import serial

class EspFlasher():
    def __init__(self, parent=None):
        print("Flash no ar")
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        self.esptoolFlash = cfg.get('firmware', 'esptoolFlash')

    def readChipInfo(self, port, baud):
        try:
            device = esptool.ESP32ROM(port, baud)
            print("device")
            print(device)
            print(device.connect())
            device.connect()
            print("device2")
            info = {}
            info["mac"] = "%02x:%02x:%02x:%02x:%02x:%02x" % device.read_mac()
            info["flash_id"] = device.flash_id()
            info["chip_name"] = device.CHIP_NAME
            device._port.close()
            return info
        except:
            print("Device desconectado")
            return 0

    def eraseFlash(self, port ):
        cmd = self.esptoolFlash+' --port '+port+' --chip esp32 erase_flash'
        print(cmd)
        result = os.system(cmd)
        print(type(result))
        print(result)
        if result == 0:
            print("Limpeza OK")
        if result == 2:
            print("Erro no prcesso de limpeza")

    def writeFirmwareMult(self, port, baud, mem1,  pathFile1, mem2,  pathFile2, mem3,  pathFile3):
        try:
            cmd = self.esptoolFlash + ' --port ' + port + ' --baud ' + baud + ' --chip esp32 write_flash --flash_mode dio --flash_freq 40m --flash_size detect ' +mem1+ ' ' +pathFile1+' '+mem2+' '+pathFile2+' '+mem3+' '+pathFile3
            print('Mult: '+cmd)
            """result = os.system(cmd)
            if result == 0:
                print("Gravação boot OK")
                return 0
            if result == 2:
                print("Erro no prcesso 1 de gravação")
                return 2"""
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            exit_code = process.wait()
            result = stdout.decode("utf-8")
            try:
                if exit_code == 0:
                    print("Gravação Firmware OK")
                    return '0;'+result
                if exit_code == 2:
                    print("Erro no prcesso 2 de gravação")
                    return '2;'+result
            except:
                print("Gravação erro")
        except serial.serialutil.SerialException:
            print("The port is at use")
            ser = serial.Serial(port, baud, timeout=1)
            ser.close()

    def writeFirmwareOne(self, port, baud, mem1,  pathFile1):
        try:
            cmd = self.esptoolFlash + ' --port ' + port + ' --baud ' + baud + ' --chip esp32 write_flash --flash_mode dio --flash_freq 40m --flash_size detect ' + mem1 + ' ' + pathFile1
            #cmd = self.esptoolFlash + " --port COM21 --baud 115200 --chip esp32 write_flash --flash_mode dio --flash_freq 40m --flash_size detect 0x10000 C:/Users/Rudrigo/Desktop/SENFIO/firmware/T1.bin"
            print('One: '+str(cmd))
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            exit_code = process.wait()
            result = stdout.decode("utf-8")
            try:
                if exit_code == 0:
                    print("Gravação Firmware OK")
                    return '0;'+result
                if exit_code == 2:
                    print("Erro no prcesso 2 de gravação")
                    return '2;'+result
            except:
                print("Gravação erro")
            """cmd = self.esptoolFlash + ' --port ' + port + ' --baud ' + baud + ' --chip esp32 write_flash --flash_mode dio --flash_freq 40m --flash_size detect ' + mem1 + ' ' + pathFile1
            print('One: ' + str(cmd))
            try:
                result = os.system(cmd)
                if result == 0:
                    print("Gravação Firmware OK")
                    return 0
                if result == 2:
                    print("Erro no prcesso 2 de gravação")
                    return 2
            except:
                print("Gravação erro")"""
        except serial.serialutil.SerialException:
            print("The port is at use")
            ser = serial.Serial(port, baud, timeout=1)
            ser.close()

    def killProcess(self, process):
        print("Kill process")


#if __name__ == '__main__':
    #flasher = EspFlasher()
    #val = flasher.readChipInfo("COM3", "115200")
    #print(val["mac"])
    #print(val)
    #flasher.eraseFlash("COM21")
    #print(flasher.writeFirmwareOne("/dev/ttyUSB1", "230400", "0x10000", "C:/Users/Rudrigo/Desktop/SENFIO/firmware/T1.bin"))
    #print(flasher.writeFirmwareOne("/dev/ttyUSB1", "230400", "0x10000", "/home/pi/Desktop/SENFIO/firmware/T12.bin"))
