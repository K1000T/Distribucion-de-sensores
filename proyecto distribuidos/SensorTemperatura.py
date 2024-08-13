# SensorTemperatura.py

import random
import threading
import zmq
from Sensor import Sensor
from time import sleep
import datetime
from threading import Thread

class SensorTemperatura(Sensor, Thread):
    def __init__(self, parametro1, parametro2):
        Sensor.__init__(self, parametro1, parametro2)
        Thread.__init__(self)
        self.inicializado = threading.Event()
        self.rango_normal = (11, 29.4)
        self.inicializado.set()

    def run(self):
        while True:
            self.tomarMuestra()
            sleep(6)

    def tomarMuestra(self):
        self.inicializado.wait()
        probabilidades = {
            "correctos": self.pCorrecto,
            "fuera_rango": self.pFueraRango,
            "error": self.pError,
        }
        eleccion = random.choices(list(probabilidades.keys()), probabilidades.values())[0]

        if eleccion == "correctos":
            self.muestra['valor'] = random.uniform(*self.rango_normal)
        elif eleccion == "fuera_rango":
            self.muestra['valor'] = random.uniform(self.rango_normal[1], self.rango_normal[1] + 10)
        else:
            self.muestra['valor'] = random.uniform(-10, 0)
            
        self.muestra['tipo'] = "temperatura"
        self.muestra['hora'] = str(datetime.datetime.now())
        self.enviarMuestraProxy()
        sleep(6)

    def enviarMuestraProxy(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect("tcp://localhost:5556")

        try:
            socket.send_pyobj(self.muestra)
            print("Muestra enviada al Proxy.")
        except zmq.ZMQError as e:
            print(f"Error al enviar la muestra: {e}")
        finally:
            socket.close()
            context.term()
