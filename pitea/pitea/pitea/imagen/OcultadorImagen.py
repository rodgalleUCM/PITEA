from abc import ABC, abstractmethod
from PIL import Image
class OcultadorImagen(ABC) :
       
    def __init__(self,ruta_imagen):
        self.formato = ruta_imagen.split(".")[-1]
        self.imagen = Image.open(ruta_imagen)
        self.pixeles = self.imagen.load()
        self.ancho, self.alto = self.imagen.size

    @abstractmethod
    def ocultar(datos) :
        pass
    @abstractmethod
    def desocultar() :
        pass