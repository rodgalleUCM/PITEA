from pitea.AbstractFactory import AbstractFactory
from pitea.imagen.OcultadorImagenLSB import OcultadorImagenLSB

class OcultadorImagenFactory(AbstractFactory) :
    @staticmethod
    def get_builder(modo_cifrado,ruta_imagen):
   

        if modo_cifrado == 'lsb':
            return OcultadorImagenLSB(ruta_imagen)
       
        else:
            raise ValueError(f"Tipo de archivo desconocido: {modo_cifrado}")