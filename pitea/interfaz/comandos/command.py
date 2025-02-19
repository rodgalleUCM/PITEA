
from abc import ABC, abstractmethod

class Command(ABC):
    
    def __init__(self,descripcion):
        self.descripcion = descripcion

    @abstractmethod
    def ejecutar(self):
        pass

    
