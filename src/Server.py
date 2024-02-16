import time
import gc
import paho.mqtt.client as mqtt


from Threads import TestThread
from Threads import MQTTThread
from Threads import WebServerThread


class Server:
    def __init__(self):
        self.debug = True  # this variable enables and disables the print output
        self.running = True  # the state of the server

        # MQTT Server
        self.MQTT_IP = "192.168.1.254"
        self.MQTT_Port = 1883

        self.publishTopic = "/Home/Server/mainP"

        self.tasks = []

        self.threads = []
        self.setup()
        self.main()

    def setup(self):
        # init Threads
        #self.threads.append(TestThread.TestThread(name="TestThread", sleepTime=5, debug=self.debug))
        self.threads.append(MQTTThread.MQTTThread(name="MQTTThread", sleepTime=5, serverData=self.tasks, debug=self.debug))
        self.threads.append(WebServerThread.WebServerThread(name="WebServerThread", serverTasks=self.tasks, serverThreads=self.threads, sleepTime=5,  debug=self.debug))

        # MQTT Setup
        self.client = mqtt.Client()  # init MQTT client
        self.client.connect(host=self.MQTT_IP, port=self.MQTT_Port, keepalive=60)  # connection to my privat MQTT server

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
            print(str(self.tasks))
            if len(self.tasks) > 0:
                data = self.tasks[0].split(".")

                if data[0] == "Start":
                    isRunning = False
                    for thread in self.threads:
                        if thread.name == data[1]:
                            isRunning = True
                    if not isRunning:
                        match data[1]:
                            case "TestThread":
                                self.threads.append(TestThread.TestThread(name="TestThread", sleepTime=5, debug=self.debug))
                            case "WebServerThread":
                                self.threads.append(WebServerThread.WebServerThread(name="WebServerThread", sleepTime=5, serverData=self.tasks, debug=self.debug))
                            case "MQTTThread":
                                self.threads.append(MQTTThread.MQTTThread(name="MQTTThread", sleepTime=5, serverData=self.tasks, debug=self.debug))
                        self.threads[len(self.threads) - 1].start()
                        self.MQTTSendData(self.threads[len(self.threads) - 1].name + " | started!")
                    elif self.debug:
                        print("Thread was already Started")

                elif data[0] == "Stop":
                    if data[1] == "Server":
                        self.running = False
                    for thread in self.threads:
                        if thread.name == data[1] or not self.running:
                            thread.running = False
                            self.threads.remove(thread)
                            self.MQTTSendData(thread.name + " | stopped!")
                            print(thread.name + " | stopped!")
                            thread.join()
                            del thread
                            gc.collect()  # to completely delete the thread
                elif data[0] == "GET":
                    match data[1]:
                        case "amountThreads":
                            print(len(self.threads))
                        case "activeThreads":
                            for thread in self.threads:
                                print(thread.name)

                self.tasks.pop(0)
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
