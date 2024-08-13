import zmq
import datetime

VALOR_MAX_TEMPERATURA = 39.4  # Supongamos que el valor máximo permitido para la temperatura es 39.4 grados Celsius

class Proxy:

    def __init__(self):
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind("tcp://localhost:5556")
        self.sender = self.context.socket(zmq.PUSH)
        self.sender.connect("tcp://localhost:5557")

    def recibirMuestras(self):
        while True:
            muestra = self.receiver.recv_pyobj()
            if self.validarMuestra(muestra):
                self.enviarMedidaCloud(muestra)

    def validarMuestra(self, muestra):
        if 'valor' in muestra and 'tipo' in muestra and 'hora' in muestra:
            return True
        else:
            print(f"Muestra inválida recibida: {muestra}")
            return False

    def calcularPromedioTemperatura(self, muestras_temperatura):
        valores_temperatura = [muestra['valor'] for muestra in muestras_temperatura if muestra['valor'] is not None]
        if valores_temperatura:
            promedio = sum(valores_temperatura) / len(valores_temperatura)
            return promedio
        else:
            return None

    def enviarMedidaCloud(self, muestra):
        self.sender.send_pyobj(muestra)
        if muestra['tipo'] == 'temperatura':
            self.procesarMedidaTemperatura(muestra)
        elif muestra['tipo'] == 'humedad':
            # Enviar la muestra de humedad directamente a la nube
            self.enviarMedidaHumedad(muestra)

    def procesarMedidaTemperatura(self, muestra):
        promedio_temp = self.calcularPromedioTemperatura([muestra])
        if promedio_temp is not None:
            fecha = datetime.datetime.strptime(muestra['hora'], '%Y-%m-%d %H:%M:%S.%f')
            print(f"Promedio de temperatura ({fecha}): {promedio_temp} grados Celsius")
            if promedio_temp > VALOR_MAX_TEMPERATURA:
                # Si la temperatura promedio supera el límite, enviar alerta al sistema de calidad de Fog
                self.enviarAlertaFog(muestra)

    def enviarAlertaFog(self, muestra):
        # Aquí implementarías la lógica para enviar la alerta al sistema de calidad de Fog
        print("Se ha activado una alerta debido a que la temperatura supera el valor máximo del rango establecido.")

    def enviarMedidaHumedad(self, muestra):
        # Enviar la muestra de humedad a la nube
        self.sender.send_pyobj(muestra)

    def stop(self):
        self.receiver.close()
        self.sender.close()
        self.context.term()

if __name__ == "__main__":
    proxy = Proxy()
    proxy.recibirMuestras()


