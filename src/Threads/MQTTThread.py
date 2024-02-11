import threading
import time

import paho.mqtt.client as mqtt

class MQTTThread(threading.Thread):
    def __init__(self, name, sleepTime=10, serverData="", debug=False):
        threading.Thread.__init__(self)
        self.name = name
        self.sleepTime = sleepTime
        self.debug = debug
        self.running = True

        self.serverData = serverData

        # MQTT Server
        self.MQTT_IP = "192.168.1.254"
        self.MQTT_Port = 1883

        # MQTT Topics
        self.subscribeTopic = "/Home/Server/mainS"
        self.publishTopic = "/Home/Server/mainP"

        # MQTT client
        self.client = mqtt.Client()  # init MQTT client
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(host=self.MQTT_IP, port=self.MQTT_Port, keepalive=60)  # connection to my privat MQTT server


    def onConnect(self, client, userdata, flags, rc):
        if self.debug:
            print("Connected with MQTT Server: " + self.MQTT_IP)
        client.subscribe(self.subscribeTopic)
        client.connected_flag = True
        client.disconnect_flag = False

    def onMessage(self, client, userdata, msg):
        topic = str(msg.topic)
        message = str(msg.payload.decode("utf-8"))
        if (self.debug):
            print(topic + " | " + message)

        self.serverData.append(message)

    def __del__(self):
        print(self.name + " | deleted!")

    def run(self):
        print(self.name + " | started!")
        time.sleep(1)
        self.client.loop_start()

        while self.running:
            print(self.name + " | running!")
            time.sleep(self.sleepTime)

        self.client.loop_stop()

        print(self.name + " | stopped!")

