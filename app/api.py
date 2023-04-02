import requests
import json

API_KEY = "ef8d760d5e3be51fa02b736f16eea85d"

def get_Socket1_Status():
    content = requests.get("http://emoncms.org/input/get/emontx/socket1&apikey="+API_KEY).content
    return json.loads(content)["value"]

def get_Socket2_Status():
    content = requests.get("http://emoncms.org/input/get/emontx/socket2&apikey="+API_KEY).content
    return json.loads(content)["value"]

def set_Socket1_Status(value :int):
    request = requests.get('https://emoncms.org/input/post?node=emontx&fulljson={"socket1":'+str(value)+'}&apikey='+API_KEY)
    return request.status_code == 200

def set_Socket2_Status(value :int):
    request = requests.get('https://emoncms.org/input/post?node=emontx&fulljson={"socket2":'+str(value)+'}&apikey='+API_KEY)
    return request.status_code == 200
