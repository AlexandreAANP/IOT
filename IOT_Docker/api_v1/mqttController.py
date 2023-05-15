import paho.mqtt.client as mqtt
import sys
import datetime
import json
class MQTTClient():
    instance = None
    def __init__(self, hostname, port) -> None:
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(hostname, port, 60)
        self.lastMsgByTopic = {}

    @classmethod
    def getMQTTClient(cls,hostname="localhost", port=1883):
        if cls.instance == None:
            cls.instance = cls(hostname,port)
        return cls.instance
    
    def subscribe(self,topic):
        try:
            self.client.subscribe(topic)
            print("subscribed to: "+topic)
        except:
            print("erro in function self.client.subscribe("+topic+")")
            return False
        return True
    
    def unsubscribe(self,topic):
        try:
            self.client.unsubscribe(topic)
            print("unsubscribed to: "+topic)
        except:
            print("erro in function self.client.unsubscribe("+topic+")")
            return False
        return True

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        #subscribe all topics
        client.subscribe("/raspberry2/")
        client.subscribe("/raspberry1/")

    def on_message(self,client, userdata, msg):
        content = None
        try:
            #try convert json_str to python_dict 
            content = json.loads(str(msg.payload.decode()))
        except:
            #if fail convertion write log file
            with open("error.log", "+a") as f:
                f.write("\n\n"+str(datetime.datetime.now())+" Error msg wrong format\nMSG: ->"+str(msg.payload.decode()))
            return
        #update content by topic
        self.lastMsgByTopic[msg.topic] = content

        print( {
            "topic" : msg.topic,
            "content" : content
        })
        print(self.lastMsgByTopic)

    def getClient(self):
        return self.client
    
    def getLastMsg(self):
        return self.lastMsgByTopic.copy()
    
    def getLastMsgByTopic(self,topic):
        try:
            self.lastMsgByTopic[topic].copy()
        except:
            print("Topic doesn't have any message\nTopic: "+topic)
            return False
        return True

