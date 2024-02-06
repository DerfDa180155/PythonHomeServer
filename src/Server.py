import time
import gc
import paho.mqtt.client as mqtt

from Threads import TestThread


class Server:
    def __init__(self):
        self.debug = True  # this variable enables and disables the print output
        self.running = True  # the state of the server

        # MQTT Server
        self.MQTT_IP = "192.168.1.254"
        self.MQTT_Port = 1883

        # MQTT Topics
        self.subscribeTopic = "/Home/Server/mainS"
        self.publishTopic = "/Home/Server/mainP"

        self.threads = []
        self.setup()
        self.main()

    def setup(self):
        # init Threads
        self.threads.append(TestThread.TestThread(name="TestThread", sleepTime=5, debug=self.debug))

        # MQTT client
        self.client = mqtt.Client() # init MQTT client
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(host=self.MQTT_IP, port=self.MQTT_Port, keepalive=60) # connection to my privat MQTT server
        self.client.loop_start()

    def onConnect(self, client, userdata, flags, rc):
        if self.debug:
            print("Connected with MQTT Server: " + self.MQTT_IP)
        client.subscribe(self.subscribeTopic)
        client.connected_flag = True
        client.disconnect_flag = False

    def onMessage(self, client, userdata, msg):
        topic = str(msg.topic)
        message = str(msg.payload.decode("utf-8"))
        if(self.debug):
            print(topic + " | " + message)

        match message:
            case "StopServer":
                self.running = False
            case "PrintActiveThreads":
                for thread in self.threads:
                    print(thread.name)
            case "StartTestThread":
                checkRunning = False
                for thread in self.threads:
                    if thread.name == "TestThread" and thread.is_alive:
                        checkRunning = True

                if not checkRunning:
                    self.threads.append(TestThread.TestThread(name="TestThread", sleepTime=5, debug=self.debug))
                    self.threads[len(self.threads)-1].start()
                    self.MQTTSendData(self.threads[len(self.threads)-1].name + " | started!")
                elif self.debug:
                    print("Thread was already Started")
            case "StopTestThread":
                for thread in self.threads:
                    if thread.name == "TestThread":
                        thread.running = False
                        self.threads.remove(thread)
                        self.MQTTSendData(thread.name + " | stopped!")
                        thread.join()
                        del thread
                        gc.collect() # to completely delete the thread

    def MQTTSendData(self, data):
        self.client.publish(self.publishTopic, data)

    def main(self):
        if self.debug:
            print("Server started!")
        self.MQTTSendData("Server started!")
        time.sleep(2)

        # start all threads
        for thread in self.threads:
            thread.start()
            self.MQTTSendData(thread.name + " | started!")


        # main server loop
        while self.running:
            time.sleep(1)

        # stop all threads
        for thread in self.threads:
            thread.running = False

            if self.debug:
                print(thread.name + " | stopped")

            self.MQTTSendData(thread.name + " | stopped!")
            thread.join()

        if self.debug:
            print("Server stopped!")
        self.MQTTSendData("Server stopped!")
        time.sleep(3)

if __name__ == '__main__':
    Server()
