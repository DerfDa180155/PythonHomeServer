import threading
import time
import os
import signal
from flask import Flask, render_template, request
import multiprocessing

app = Flask(__name__)
ServerData = ""

class WebServerThread(threading.Thread):
    def __init__(self, name, sleepTime=10, serverData="", debug=False):
        threading.Thread.__init__(self)
        self.name = name
        self.sleepTime = sleepTime
        self.debug = debug
        self.running = True
        global ServerData
        ServerData = serverData

    def __del__(self):
        print(self.name + " | deleted!")

    def run(self):
        global app
        print(self.name + " | started!")
        time.sleep(1)

        while self.running:
            print(self.name + " | running!")
            app.run(debug=True, use_reloader=False, host='0.0.0.0')
            time.sleep(self.sleepTime)

        print(self.name + " | stopped!")

    @app.route('/')
    def index():
        return render_template('mainPage.html')

    @app.route('/API/GET/<apiRequest>')
    def apiGET(apiRequest):
        global ServerData
        print(ServerData)
        return render_template('apiGET.html', answer=str(ServerData))

    @app.route('/API/POST/<apiRequest>')
    def apiPOST(apiRequest):
        global ServerData
        ServerData.append(apiRequest)
        return "POST | " + str(apiRequest)





