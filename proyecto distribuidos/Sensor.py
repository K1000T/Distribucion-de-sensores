class Sensor:
    muestra = {
        'tipo': '',
        'valor': '',
        'tiempo': ''
    }

    def __init__(self, parametro1, parametro2):
        self.tipo = parametro1
        self.configFile = parametro2
        self.pCorrecto = -1
        self.pFueraRango = -1
        self.pError = -1

        self.leerArchivo()

    def tomarMuestra(self):
        print("Muestra de humo tomada")

    def enviarMuestraProxy(self):
        print("Muestra de humo enviada")

    def leerArchivo(self):
        # Abrir el archivo para lectura ('r')
        with open(self.configFile, 'r') as archivo:
            # Leer todas las líneas del archivo
            lineas = archivo.readlines()

            # Procesar cada línea
            for linea in lineas:
                # Dividir la línea por el delimitador ';'
                partes = linea.strip().split(';')

                # Convertir cada parte a entero (o flotante si fuera necesario)
                numeros = [float(parte) for parte in partes]

                # Hacer algo con los números (aquí simplemente los imprimo)
                print(numeros)
                self.pCorrecto = numeros[0]
                self.pFueraRango = numeros[1]
                self.pError = numeros[2]
