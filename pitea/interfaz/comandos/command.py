
from abc import ABC, abstractmethod

# Clase abstracta Command
# Esta clase es la clase base de todos los comandos
class Command(ABC):
    
    def __init__(self,descripcion):
        self.descripcion = descripcion

    @abstractmethod
    def ejecutar(self):
        pass

    
