from django.shortcuts import render

def minha_pagina(request):
    opcoes_raspberry = ['raspberryPi1', 'raspberryPi2', 'raspberryPi3']  # Substitua com a sua lista de valores

    if 'selecao' in request.GET:
        selecao = request.GET['selecao']
        # Aqui você pode implementar a lógica para buscar os valores correspondentes à seleção

        # Exemplo: valores da segunda dropdown com base na seleção do primeiro dropdown
        if selecao == 'raspberryPi 1':
            valores_dropdown2 = ['Valor 1', 'Valor 2', 'Valor 3']
        elif selecao == 'raspberryPi 2':
            valores_dropdown2 = ['Valor A', 'Valor B', 'Valor C']
        else:
            valores_dropdown2 = ['Valor X', 'Valor Y', 'Valor Z']
    else:
        selecao = None
        valores_dropdown2 = []

    context = {
        'opcoes_raspberry': opcoes_raspberry,
        'selecao': selecao,
        'valores_dropdown2': valores_dropdown2
    }

    return render(request, 'minha_pagina.html', context)
