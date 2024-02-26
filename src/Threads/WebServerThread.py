import threading
import time
import os
import signal
from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import multiprocessing

app = Flask(__name__)
ServerTasks = ""
ServerThreads = ""

class WebServerThread(threading.Thread):
    def __init__(self, name, serverTasks, serverThreads, sleepTime=10, debug=False):
        threading.Thread.__init__(self)
        self.name = name
        self.sleepTime = sleepTime
        self.debug = debug
        self.running = True
        global ServerTasks
        ServerTasks = serverTasks
        global ServerThreads
        ServerThreads = serverThreads

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
    @cross_origin()
    def apiGET(apiRequest):
        global ServerTasks, ServerThreads
        answer = ""
        match apiRequest:
            case "serverStatus":
                answer = "Running"
            case "allRunningThreads":
                for thread in ServerThreads:
                    answer += thread.name + " "
            case "amountOfRunningThreads":
                answer = len(ServerThreads)
            case "amountOfServerTasks":
                answer = len(ServerTasks)
            case "currentServerTasks":
                answer = ServerTasks
            case _:
                answer = "ERROR - requestNotFound"

        data = {
            "answer": answer
        }

        return jsonify(data)

        #return render_template('apiGET.html', answer=str(answer))

    @app.route('/API/POST/<apiRequest>')
    @cross_origin()
    def apiPOST(apiRequest):
        global ServerTasks
        ServerTasks.append(apiRequest)

        data = {
            "answer": "Send successfully!"
        }

        return jsonify(data)
        #return render_template('apiGET.html', answer=str("Send successfully!"))





