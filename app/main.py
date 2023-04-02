import kivy
import api
import time
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
kivy.require('1.9.0')

RELOAD_TIME = 1

class myRoot(BoxLayout):
    def __init__(self):
        super(myRoot, self).__init__()
        #faz refresh do status dos sockets
        self.change_status_Socket1(api.get_Socket1_Status())
        self.change_status_Socket1(api.get_Socket2_Status())
        #começa um thread a cada RELOAD_TIME segundos executando o metodo reload_status
        t = threading.Thread(target=self.reload_status, daemon=True)
        t.start()


    def reload_status(self):
        while True:
            time.sleep(RELOAD_TIME)
            print("Socket1 status - "+str(api.get_Socket1_Status()))
            print("Socket2 status - "+str(api.get_Socket2_Status()))
            self.change_status_Socket1(api.get_Socket1_Status())
            self.change_status_Socket2(api.get_Socket2_Status())

    def change_status_Socket1(self, status :int):
        #no caso de o texto corresponde com parametro status ent retorna, ou seja, n faz mais nada
        if (self.socket1.text == "status: Ligado" and status == 1) or (self.socket1.text == "status: Desligado" and status == 0):
            return
        if(status == 1):
            self.socket1.text = "status: Ligado"
        else:
            self.socket1.text  = "status: Desligado"

    def ligarSocket1(self):
        if(api.set_Socket1_Status(1)):
            self.change_status_Socket1(1)

    def desligarSocket1(self):
        if(api.set_Socket1_Status(0)):
            self.change_status_Socket1(0)

    def change_status_Socket2(self, status :int):
        #no caso de o texto corresponde com parametro status ent retorna, ou seja, n faz mais nada
        if (self.socket2.text == "status: Ligado" and status == 1) or (self.socket2.text == "status: Desligado" and status == 0):
            return
        if(status == 1):
            self.socket2.text = "status: Ligado"
        else:
            self.socket2.text  = "status: Desligado"

    def ligarSocket2(self):
        if api.set_Socket2_Status(1):
            self.change_status_Socket2(1)

    def desligarSocket2(self):
        if api.set_Socket2_Status(0):
            self.change_status_Socket2(0)
    

class app(App):

    def build(self):
        return myRoot()
    
myapp = app()
myapp.run()