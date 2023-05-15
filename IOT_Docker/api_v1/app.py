from flask import Flask
#from flask_crontab import Crontab
import requests
import threading
import paho.mqtt.client as mqtt
import signal
from mqttController import MQTTClient

ListenerMQTT = MQTTClient.getMQTTClient("localhost", 2222)
t1 = threading.Thread(target=ListenerMQTT.getClient().loop_start)



app = Flask(__name__)

#function to terminated when ctrl + c is pressed
def terminateThread(signum, frame):
    print("CTRL + C")
    ListenerMQTT.getClient().disconnect()
    ListenerMQTT.getClient().loop_stop(force=True)
    raise KeyboardInterrupt

@app.route('/')
def hello_world():
    MQTTClient.getMQTTClient().subscribe("/teste/")
    return 'Hello World'

@app.route('/e')
def hello_world():
    MQTTClient.getMQTTClient().unsubscribe("/teste/")
    return 'Hello World'
 
# main driver function
if __name__ == '__main__':
    signal.signal(signal.SIGINT, terminateThread)
    t1.start()
    ListenerMQTT.getClient().loop_stop(force=True)
    app.run()