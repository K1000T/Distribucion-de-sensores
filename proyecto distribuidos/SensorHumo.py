# SensorHumo.py

import datetime
import random
import threading
from Sensor import Sensor
from time import sleep
import zmq
from threading import Thread
from Aspersor import Aspersor

class SensorHumo(Sensor, Thread):
    def __init__(self, parametro1, parametro2):
        Sensor.__init__(self, parametro1, parametro2)
        Thread.__init__(self) 
        self.valores_booleanos = (True, False, "Error")

    def run(self):
        aspersor = Aspersor()
        while True:
            self.tomarMuestra(aspersor)
            sleep(3)

    def tomarMuestra(self, aspersor):
        probabilidades = {
            "humo_detectado": self.pCorrecto,
            "error": self.pError,
        }
        eleccion = random.choices(list(probabilidades.keys()), probabilidades.values())[0]

        if eleccion == "humo_detectado":
            self.muestra['valor'] = random.choice([True, False])
        else:
            self.muestra['valor'] = "error"

        self.muestra['tipo'] = "alerta humo"
        self.muestra['hora'] = str(datetime.datetime.now())

        self.enviarAlertaProxy()
        if self.muestra['valor'] == True:
            self.enviarMensajeAspersor(aspersor)
            self.generarSistemaCalidad()

    def generarSistemaCalidad(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        socket.send_string("Alerta: Sistema de Calidad")
        response = socket.recv_string()
        print(f"Sensor humo: recibe '{response}' del sistema de calidad")
        socket.close()
        context.term()

    def enviarMensajeAspersor(self, aspersor):
        aspersor.activarAspersor()

    def enviarAlertaProxy(self):
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