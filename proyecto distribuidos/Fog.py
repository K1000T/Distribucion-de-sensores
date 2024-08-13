from Proxy import Proxy
from ServidorLocal import ServidorLocal
from SistemaCalidad import SistemaCalidad

class Fog:
    @staticmethod
    def crearProxy():
        print("Creando proxy")
        return Proxy()

    @staticmethod
    def crearServidor():
        print("Creando servidor")
        return ServidorLocal()

    @staticmethod
    def crearSistemaCalidad():
        print("Creando sistema de calidad")
        return SistemaCalidad()

if __name__ == "__main__":
    print("Creando fog")
    proxy = Fog.crearProxy()
    Fog.crearServidor()
    proxy.recibirMuestras()
