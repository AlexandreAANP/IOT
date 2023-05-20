from flask import Flask, request
#from flask_crontab import Crontab
import requests
import threading
import paho.mqtt.client as mqtt
import signal
import os
from mqttController import MQTTClient

ALLOWED_EXTENSIONS = ['mp4']
VIDEOS_PATH = "../videos"
ListenerMQTT = MQTTClient.getMQTTClient(hostname="localhost", port=2222, subscribeList=["raspberrypi1", "raspberrypi2"])
t1 = threading.Thread(target=ListenerMQTT.getClient().loop_start)



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../videos'


#function to terminated when ctrl + c is pressed
def terminateThread(signum, frame):
    print("CTRL + C")
    ListenerMQTT.getClient().disconnect()
    ListenerMQTT.getClient().loop_stop(force=True)
    raise KeyboardInterrupt

@app.route('/')
def hello_world():
    MQTTClient.getMQTTClient().subscribe("/teste/")
    print(MQTTClient.getMQTTClient().isSubscribe("/teste/"))
    return 'Hello World'


@app.route('/setVideo', methods=["GET"])
def setRaspBerryPiVideo():
     videoName=request.args.get("videoName",None)
     topic = request.args.get("topic",None)
     #if there are parameters variables videoName and topic
     if(videoName and topic):
        print(os.listdir(VIDEOS_PATH))
        #if there is not a '.' and if the filename is not in the videos folder
        if(not '.'in videoName and not videoName in os.listdir(VIDEOS_PATH)):
            return f'videoName not found in videos folder {videoName}', 404
        
     return "missing url parameters, you should use 'videoName' and 'topic parameters'",500

@app.route('/uploadvideo', methods=["POST"])
def uploadVideo():
    file = request.files['image']
    if file:
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                return "Uploaded", 200
    return "Invalid Format File", 500

 
# main driver function
if __name__ == '__main__':
    signal.signal(signal.SIGINT, terminateThread)
    t1.start()
    ListenerMQTT.getClient().loop_stop(force=True)
    app.run(debug=True)