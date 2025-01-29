from abc import ABC, abstractmethod
from PIL import Image
from pitea.constantes import (
    RUTA_IMAGEN_CONTENEDORA,
    RUTA_DATOS_CIFRADOS_DESOCULTACION,
    RUTA_DATOS_CIFRADO,
)


class OcultadorImagen(ABC):
    nombre = ""

    def __init__(self, ruta_imagen):
        if ruta_imagen:
            self.formato = ruta_imagen.split(".")[-1]
            self.imagen = Image.open(ruta_imagen)
            self.pixeles = self.imagen.load()
            self.ancho, self.alto = self.imagen.size

    @abstractmethod
    def ocultar(self, datos_imagen,altura_imagen = None,anchura_imagen=None):
        pass

    @abstractmethod
    def desocultar(self):
        pass

    def ocultar_guardar(self,altura_imagen= None,anchura_imagen=None):
        with open(RUTA_DATOS_CIFRADO, "rb") as f:
            datos = f.read()

        imagen, formato = self.ocultar(datos,altura_imagen,anchura_imagen)

        imagen.save(str(RUTA_IMAGEN_CONTENEDORA) % formato)

        print(
            f"Imagen contenedora guardada en {str(RUTA_IMAGEN_CONTENEDORA) % formato}"
        )

        return imagen, formato

    def desocultar_guardar(self):
        datos_extraidos = self.desocultar()

        with open(RUTA_DATOS_CIFRADOS_DESOCULTACION, "wb") as f:
            f.write(datos_extraidos)

        print(f"Datos cifrados guardados en {RUTA_DATOS_CIFRADOS_DESOCULTACION}")
