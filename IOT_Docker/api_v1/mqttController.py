import paho.mqtt.client as mqtt
import sys
import datetime
import json
class MQTTClient():
    instance = None
    def __init__(self, hostname, port, subscribeList) -> None:
        self.client = mqtt.Client()
        self.subscribeList = subscribeList
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(hostname, port, 60)
        self.lastMsgByTopic = {}
        

    @classmethod
    def getMQTTClient(cls,subscribeList:list = [], hostname="localhost", port=1883 ):
        if cls.instance == None:
            cls.instance = cls(hostname,port,tuple(subscribeList))
        return cls.instance
    
    def subscribe(self,topic):
        if topic in self.subscribeList:
            print(topic+" already subscribed")
            return
        try:
            self.client.subscribe(topic)
            l = list(self.subscribeList)
            l.append(topic)
            self.subscribeList = tuple(l)
            print("subscribed to: "+topic)
        except:
            print("erro in function self.client.subscribe("+topic+")")
            return False
        return True
    
    def isSubscribe(self, topic):
        return topic in self.subscribeList

    def unsubscribe(self,topic):
        if not topic in self.subscribeList:
            print(topic+" already unsubscribed")
            return
        try:
            self.client.unsubscribe(topic)
            l = list(self.subscribeList)
            l.remove(topic)
            self.subscribeList = tuple(l)
            print("unsubscribed to: "+topic)
        except:
            print("erro in function self.client.unsubscribe("+topic+")")
            return False
        return True

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        #subscribe all topics
        for i in self.subscribeList:
            client.subscribe(str(i))

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

