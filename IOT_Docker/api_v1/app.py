from flask import Flask, request, jsonify
#from flask_crontab import Crontab
import requests
import threading
import paho.mqtt.client as mqtt
import signal
import os
from mqttController import MQTTClient

dev = {
    "hostname" : "localhost",
    "port" : 2222,
    "ALLOWED_EXTENSIONS" : ['mp4','jpg','png'],
    "VIDEOS_PATH" : "../videos"
}
prod = {
    "hostname" : "iot_docker-mosquitto-mqtt-1",
    "port" : 1883,
    "ALLOWED_EXTENSIONS" : ['mp4'],
    "VIDEOS_PATH" : "../videos"
}

ALLOWED_EXTENSIONS = dev["ALLOWED_EXTENSIONS"]
VIDEOS_PATH = dev["VIDEOS_PATH"]


ListenerMQTT = MQTTClient.getMQTTClient(hostname=dev["hostname"], port=dev["port"], subscribeList=["raspberrypi1", "raspberrypi2"])
t1 = threading.Thread(target=ListenerMQTT.getClient().loop_start)



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = VIDEOS_PATH


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
     videoName = request.args.get("videoName",None)
     topic = request.args.get("topic",None)
     #if there are parameters variables videoName and topic
     if(videoName and topic):
        #if there is not a '.' and if the filename is not in the videos folder
        if(not '.' in videoName or not videoName in os.listdir(VIDEOS_PATH)):
            return f'videoName not found in videos folder {videoName}', 404
        if(not topic in MQTTClient.getMQTTClient().getSubscribedList()):
            return f'API MQTT Client is not subscribe to '+topic, 404
        MQTTClient.getMQTTClient().setVideoToRasberryPi(videoName,topic)
        print(MQTTClient.getMQTTClient().getLastMsgByTopic(topic))
        return f'OK'
     return "missing url parameters, you should use 'videoName' and 'topic parameters'",500

@app.route('/getSubscribedTopic', methods=["GET"])
def getSubscribedTopic():
    return jsonify(MQTTClient.getMQTTClient().getSubscribedList())

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