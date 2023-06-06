from django.shortcuts import render
import requests
import json
API_HOST = "localhost"
API_PORT = "5000"
def minha_pagina(request):
    msgErr = ""
    try:
        opcoes_raspberry = json.loads(requests.get("http://"+API_HOST+":"+API_PORT+"/getSubscribedTopic").content.decode())
        videos = json.loads(requests.get("http://"+API_HOST+":"+API_PORT+"/getVideo").content.decode())
    except Exception as e:
        msgErr = e.__str__
        return render(request, 'FailedConnect.html', {
            "API_HOST": API_HOST,
            "API_PORT" : API_PORT,
            "msgErr": msgErr
            })
            
    context = {
        'opcoes_raspberry': opcoes_raspberry,
        'opcoes_videos' : videos
    }

    return render(request, 'minha_pagina.html', context)

def new_minha_pagina(request):
    msgErr = ""
    try:
        opcoes_raspberry = json.loads(requests.get("http://"+API_HOST+":"+API_PORT+"/getSubscribedTopic").content.decode())
        videos = json.loads(requests.get("http://"+API_HOST+":"+API_PORT+"/getVideo").content.decode())
    except Exception as e:
        msgErr = e.__str__
        return render(request, 'FailedConnect.html', {
            "API_HOST": API_HOST,
            "API_PORT" : API_PORT,
            "msgErr": msgErr
            })
            
    context = {
        "API_HOST": API_HOST,
        "API_PORT" : API_PORT,
        'opcoes_raspberry': opcoes_raspberry,
        'opcoes_videos' : videos
    }

    return render(request, 'new_minha_pagina.html', context)