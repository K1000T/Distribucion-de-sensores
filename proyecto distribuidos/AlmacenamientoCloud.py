import threading
import datetime
import zmq
from collections import defaultdict
from time import sleep

LIMITE_HUMEDAD = 0.2

class AlmacenamientoCloud:
    def __init__(self):
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind("tcp://localhost:5557")
        self.humidades = defaultdict(lambda: defaultdict(list))  # {mes: {sensor: [humedades diarias]}}

        # Contexto y socket para enviar alertas
        self.alert_context = zmq.Context()
        self.alert_socket = self.alert_context.socket(zmq.REQ)
        self.alert_socket.connect("tcp://localhost:5555")

    def recibirMuestrasHumedad(self):
        while True:
            muestra = self.receiver.recv_pyobj()
            if muestra['tipo'] == 'humedad':
                # Asignar un valor predeterminado para el sensor
                sensor = 'humedad'
            else:
                tipo_parts = muestra['tipo'].split('_')
                if len(tipo_parts) >= 2:
                    sensor = tipo_parts[1]  # Obtener el sensor del campo 'tipo'
                else:
                    print("Advertencia: Formato incorrecto en el campo 'tipo'. No se pudo obtener el sensor.")
                    continue

            mes_actual = datetime.datetime.now().month
            valor = muestra['valor']
            self.humidades[mes_actual][sensor].append(valor)
            print(f"Muestra de humedad recibida: {muestra}")  # Mostrar la muestra recibida

    def calcularPromedioMensual(self):
        while True:
            for mes, sensores in self.humidades.items():
                promedio_mensual = {}
                for sensor, humedades in sensores.items():
                    promedio_mensual[sensor] = sum(humedades) / len(humedades)
                print("Promedio mensual de humedad:", promedio_mensual)
                self.generarAlertaCalidad(promedio_mensual)
            sleep(20)

    def generarAlertaCalidad(self, promedio_mensual):
        for sensor, promedio in promedio_mensual.items():
            if promedio < LIMITE_HUMEDAD:
                self.enviarAlertaCalidad()
            else:
                print("Almacenamiento Cloud: {promedio}" )

    def enviarAlertaCalidad(self):
        try:
            self.alert_socket.send_string("Alerta: Humedad mensual por debajo del límite")
            response = self.alert_socket.recv_string()
            print(f"Almacenamiento Cloud: recibe '{response}' del sistema de calidad")
        except zmq.ZMQError as e:
            print(f"Error al enviar/recibir la alerta: {e}")

    def stop(self):
        self.receiver.close()
        self.context.term()
        self.alert_socket.close()
        self.alert_context.term()

    def main(self):
        # Inicializar y ejecutar la capa de almacenamiento en la nube aquí
        self.__init__()
        
        # Crear un hilo para calcular el promedio mensual de humedad
        thread_calcular_promedio = threading.Thread(target=self.calcularPromedioMensual)
        thread_calcular_promedio.start()
        
        # Recibir muestras de humedad
        self.recibirMuestrasHumedad()

if __name__ == "__main__":
    cloud = AlmacenamientoCloud()
    cloud.main()

