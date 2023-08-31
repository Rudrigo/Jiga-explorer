import paho.mqtt.client as mqtt
import json
import time

class MqttClient:
    def __init__(self, broker, port=1883, client_id=None, username=None, password=None):

        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id)
        self.connected = False
        if username is not None and password is not None:
            self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.payload = ''

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conexão estabelecida com sucesso! - on_connect")
            self.connected = True
        else:
            print("Falha na conexão. Código de retorno =", rc)
            self.connected = False

    def on_publish(self, client, userdata, mid):
        print("Mensagem publicada com sucesso!")

    def on_message(self, client, userdata, msg):
        print(f"Nova mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
        self.payload = msg.payload.decode()

    def on_disconnect(self, client, userdata, msg):
        print("Disconectado!!!")

    def connect(self):
        print("Connect")
        self.client.connect(self.broker, port=self.port, keepalive=60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, message):
        if self.connected:
            self.client.publish(topic, message)
        else:
            print("Não conectado ao broker MQTT. - Publish")

    def subscribe(self, topic, qos=1):
        if self.connected:
            self.client.subscribe(topic, qos)
        else:
            print("Não conectado ao broker MQTT. - Subscribe")

    def connectGota(self, diciPay, mac, test=None):
        print(diciPay)
        time.sleep(2)
        pub = diciPay['topicpub'].split('#')
        sub = diciPay['topicsub'].split('#')
        topicPub = pub[0]+diciPay[mac]+pub[1]
        topicSub = sub[0]+(diciPay[mac].upper()).replace(":", "")+sub[1]
        pay = {"mac": diciPay[mac], "teste": test}
        print(topicPub)
        print(topicSub)
        print(pay)
        json_string = json.dumps(pay)
        self.client.subscribe(topicSub)
        self.client.publish(topicPub, json_string)
        time.sleep(1)
        count = 1
        while (True):
            time.sleep(1)
            if self.payload:
                parsed_data = json.loads(self.payload)
                self.payload = ''
                self.disconnect()
                return parsed_data["serial_number"]
            else:
                print("Loop payload")
                count = count+1
            if count >=5: #5
                self.disconnect()
                print("Erro no servidor gota!")
                return 'ERRO'


#if __name__ == '__main__':
    #dici = {'MAX': 'Max: 22.78*C', 'BME': 'BME: 3.07*C || 0.00% || 0Pa', 'BATTERY': 'Bateria: 4.0V',
    #'RTC': 'RTC: 06/05/04 03:02:01', 'FRAM': 'FRAM: OK', 'WIFI': 'Wi-Fi: Ok -> MAC: ec:62:60:a5:92:2c || RSSI: -48dBm', 'MQTT': 'MQTT_BROKER: OK'}

    #print(mountPay(dici))
    #print(dici['BME'])


    """distTest = {"max": "False", "bme": "False", "battery": "False", "rtc": "False", "fram": "False",
                     "display": "False", "buzzer": "False", "wifi": "False", "mqtt": "False"}

    for indice, valor in enumerate(distTest, start=1):
        #print(f"Item {indice}: {valor}")
        print(indice)
        print(valor)"""

    """pay = {}
    pay["mac1"] = "11:22:33:44:55:11"
    mqtt_client = MqttClient(broker="connectt.vps-kinghost.net", client_id='001', username="admin", password="##Cd9500$$")
    # Conectando ao broker
    mqtt_client.connect()
    time.sleep(2)
    value = mqtt_client.connectGota(pay, 'mac1')
    print(type(value))
    print(value)"""

    # Publicando uma mensagem em um tópico
    """topic = "senfio"
    message = "Olá, MQTT!"
    #mqtt_client.connect()
    time.sleep(2)
    #mqtt_client.publish(topic, message)
    time.sleep(2)
    # Assinando um tópico para receber mensagens
    mqtt_client.subscribe(topic)
    # Aguardando um tempo para receber mensagens
    time.sleep(5)
    # Desconectando
    #mqtt_client.disconnect()
    while(True):
        time.sleep(1)
        if mqtt_client.payload:
            print("mqtt_client.payload --------------------")
            print(mqtt_client.payload)
            mqtt_client.payload = ''
            mqtt_client.disconnect()
            break
        else:
            print("Loop payload")"""

