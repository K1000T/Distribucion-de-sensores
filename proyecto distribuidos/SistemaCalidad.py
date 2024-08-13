import zmq

class SistemaCalidad:

    def __init__(self):
        print("Creando sistema de calidad")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

    def EsperarAlerta(self):
        try:
            while True:
                message = self.socket.recv_string()
                self.ImprimirAlerta(message)
                self.socket.send_string("Alerta impresa en pantalla")
        except zmq.ZMQError as e:
            print(f"Error en el socket: {e}")
        finally:
            self.socket.close()
            self.context.term()

    def ImprimirAlerta(self, message):
        print(f"Sistema de Calidad: recibe '{message}'")

if __name__ == "__main__":
    sistema_calidad = SistemaCalidad()
    sistema_calidad.EsperarAlerta()
  
   