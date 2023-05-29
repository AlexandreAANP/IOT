from django.shortcuts import render
import requests
import json

def minha_pagina(request):
    opcoes_raspberry = json.loads(requests.get("http://localhost:5000/getSubscribedTopic").content.decode())
    videos = json.loads(requests.get("http://localhost:5000/getVideo").content.decode())
    context = {
        'opcoes_raspberry': opcoes_raspberry,
        'opcoes_videos' : videos
    }

    return render(request, 'minha_pagina.html', context)
