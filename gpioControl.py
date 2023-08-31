import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import time

class GpioAdsControl():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.pinRele5V = 17
        self.pinReleIN2 = 27

        self.pinCH1Pwr = 20    #IN1
        self.pinCH1Flash = 26  #IN2
        self.pinCH1Btn = 16    #IN3

        self.pinCH2Pwr = 19    #IN4
        self.pinCH2Flash = 13  #IN5
        self.pinCH2Btn = 12    #IN6

        self.pinCH3Pwr = 6    # IN7
        self.pinCH3Flash = 5  # IN8
        self.pinCH3Btn = 1    # IN9

        self.pinCH4Pwr = 0    # IN10
        self.pinCH4Flash = 7  # IN11
        self.pinCH4Btn = 8    # IN12

        #self.pinExtra = 11  # IN13

        #---------------- GPIO SETUP ---------------------
        GPIO.setup(self.pinRele5V, GPIO.OUT)
        GPIO.setup(self.pinReleIN2, GPIO.OUT)

        GPIO.setup(self.pinCH1Pwr, GPIO.OUT)
        GPIO.setup(self.pinCH1Flash, GPIO.OUT)
        GPIO.setup(self.pinCH1Btn, GPIO.OUT)

        GPIO.setup(self.pinCH2Pwr, GPIO.OUT)
        GPIO.setup(self.pinCH2Flash, GPIO.OUT)
        GPIO.setup(self.pinCH2Btn, GPIO.OUT)

        GPIO.setup(self.pinCH3Pwr, GPIO.OUT)
        GPIO.setup(self.pinCH3Flash, GPIO.OUT)
        GPIO.setup(self.pinCH3Btn, GPIO.OUT)

        GPIO.setup(self.pinCH4Pwr, GPIO.OUT)
        GPIO.setup(self.pinCH4Flash, GPIO.OUT)
        GPIO.setup(self.pinCH4Btn, GPIO.OUT)

        #GPIO.setup(self.pinExtra, GPIO.OUT)

        # ---------------- GPIO ESTADO INICIAL ---------------------
        GPIO.output(self.pinRele5V, 1)
        GPIO.output(self.pinReleIN2, 1)

        GPIO.output(self.pinCH1Pwr,   1)  #IN1
        GPIO.output(self.pinCH1Flash, 1)  #IN2
        GPIO.output(self.pinCH1Btn,   1)  #IN3

        GPIO.output(self.pinCH2Pwr,   1)  #IN4
        GPIO.output(self.pinCH2Flash, 1)  #IN5
        GPIO.output(self.pinCH2Btn,   1)  #IN6

        GPIO.output(self.pinCH3Pwr,   1)  #IN7
        GPIO.output(self.pinCH3Flash, 1)  #IN8
        GPIO.output(self.pinCH3Btn,   1)  #IN9

        GPIO.output(self.pinCH4Pwr,   1)  #IN10
        GPIO.output(self.pinCH4Flash, 1)  #IN11
        GPIO.output(self.pinCH4Btn,   1)  #IN12

        #GPIO.output(self.pinExtra, 1) # IN13

        self.adc1 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        self.adc2 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
        self.adc3 = Adafruit_ADS1x15.ADS1115(address=0x4a, busnum=1)
        self.adc4 = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=1)
        self.gain = 1

    def cmdReleIN(self, stat1, stat2):
        GPIO.output(self.pinRele5V, stat1)
        GPIO.output(self.pinReleIN2, stat2)

    def cmdReleCH1(self, stat1, stat2, stat3): #Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
        GPIO.output(self.pinCH1Pwr, stat1)
        GPIO.output(self.pinCH1Flash, stat2)
        GPIO.output(self.pinCH1Btn, stat3)

    def cmdReleCH2(self, stat1, stat2, stat3): #Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
        GPIO.output(self.pinCH2Pwr, stat1)
        GPIO.output(self.pinCH2Flash, stat2)
        GPIO.output(self.pinCH2Btn, stat3)

    def cmdReleCH3(self, stat1, stat2, stat3):  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
        GPIO.output(self.pinCH3Pwr, stat1)
        GPIO.output(self.pinCH3Flash, stat2)
        GPIO.output(self.pinCH3Btn, stat3)

    def cmdReleCH4(self, stat1, stat2, stat3):  # Pwr(Chave-bat), Flash(Gpio0), Btn(Chave-display)
        GPIO.output(self.pinCH4Pwr, stat1)
        GPIO.output(self.pinCH4Flash, stat2)
        GPIO.output(self.pinCH4Btn, stat3)

    #def cmdReleExtra(self, stat):
        #GPIO.output(self.pinExtra, stat)

    """def readAD(self):
        while(1):
            value = self.adc.read_adc(0, gain=self.gain)
            voltage = float("{:.2f}".format(value*(4.096/32767)))
            print('Valor pin 0: '+str(voltage))
            if (voltage > 2.00):
               GPIO.output(self.pinRelePwr,1)
               GPIO.output(self.pinReleFlash,0)
            else:
               GPIO.output(self.pinRelePwr,0)
               GPIO.output(self.pinReleFlash,1)
            time.sleep(0.5)"""

    def readVoltPl1(self, ch):
        for i in range(5):
            value = self.adc1.read_adc(ch, gain=self.gain)
        voltage = float("{:.2f}".format(value * (4.096 / 32767)))
        print('Voltage: ' + str(voltage))
        return voltage

    def readVoltPl2(self, ch):
        for i in range(5):
            value = self.adc2.read_adc(ch, gain=self.gain)
        voltage = float("{:.2f}".format(value * (4.096 / 32767)))
        print('Voltage: ' + str(voltage))
        return voltage

    def readVoltPl3(self, ch):
        for i in range(5):
            value = self.adc3.read_adc(ch, gain=self.gain)
        voltage = float("{:.2f}".format(value * (4.096 / 32767)))
        print('Voltage: ' + str(voltage))
        return voltage

    def readVoltPl4(self, ch):
        for i in range(5):
            value = self.adc4.read_adc(ch, gain=self.gain)
        voltage = float("{:.2f}".format(value * (4.096 / 32767)))
        print('Voltage: ' + str(voltage))
        return voltage

"""if __name__ == '__main__':
    cGpio = GpioAdsControl()
    while(True):
        time.sleep(1)
        cGpio.cmdReleCH1(1, 1, 1)
        time.sleep(1)
        cGpio.cmdReleCH1(0, 1, 1)
        time.sleep(1)
        cGpio.cmdReleCH1(0, 0, 1)
        time.sleep(1)
        cGpio.cmdReleCH1(0, 0, 0)

        time.sleep(1)
        cGpio.cmdReleCH2(1, 1, 1)
        time.sleep(1)
        cGpio.cmdReleCH2(0, 1, 1)
        time.sleep(1)
        cGpio.cmdReleCH2(0, 0, 1)
        time.sleep(1)
        cGpio.cmdReleCH2(0, 0, 0)

        time.sleep(1)
        cGpio.cmdReleCH3(1, 1, 1)
        time.sleep(1)
        cGpio.cmdReleCH3(0, 1, 1)
        time.sleep(1)
        cGpio.cmdReleCH3(0, 0, 1)
        time.sleep(1)
        cGpio.cmdReleCH3(0, 0, 0)

        time.sleep(1)
        cGpio.cmdReleCH4(1, 1, 1)
        time.sleep(1)
        cGpio.cmdReleCH4(0, 1, 1)
        time.sleep(1)
        cGpio.cmdReleCH4(0, 0, 1)
        time.sleep(1)
        cGpio.cmdReleCH4(0, 0, 0)

        #time.sleep(1)
        #cGpio.cmdReleExtra(1)
        #time.sleep(1)
        #cGpio.cmdReleExtra(0)

        time.sleep(1)
        cGpio.cmdReleIN(1, 1)
        time.sleep(1)
        cGpio.cmdReleIN(0, 1)
        time.sleep(1)
        cGpio.cmdReleIN(0, 0)

        time.sleep(1)
        cGpio.readVoltPl1(0)
        time.sleep(1)
        cGpio.readVoltPl1(1)
        time.sleep(1)
        cGpio.readVoltPl1(2)
        time.sleep(1)
        cGpio.readVoltPl1(3)"""