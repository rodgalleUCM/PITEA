
from interfaz.constantes import RESET, ROJO

#clase para invocar comandos
class Invoker:
    def __init__(self):
        self.comandos = {}

    def obtener_comandos(self):
        return self.comandos
    
    def registrar_comando(self, nombre, comando):
        self.comandos[nombre] = comando
    
    def ejecutar_comando(self, nombre):
        if nombre in self.comandos:
            self.comandos[nombre].ejecutar()
        else:
            print(ROJO + "Comando no reconocido." + RESET)