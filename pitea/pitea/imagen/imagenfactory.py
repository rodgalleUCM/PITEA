from pitea.AbstractFactory import AbstractFactory
from pitea.imagen.OcultadorImagenLSB import OcultadorImagenLSB
from pitea.imagen.OcultadorImagenText import OcultadorImagenText
from pitea.imagen.OcultadorImagenNone import OcultadorImagenNone


class OcultadorImagenFactory(AbstractFactory):
    lista_ocultadores = [OcultadorImagenLSB,OcultadorImagenText,OcultadorImagenNone]

    @staticmethod
    def get_builder(modo_cifrado, ruta_imagen,modo_cifrador,input_text= None):
        for ocultador in OcultadorImagenFactory.lista_ocultadores:
            if ocultador.nombre == modo_cifrado:
                return ocultador(ruta_imagen,modo_cifrador,input_text)

        # Si llega aqui esque ninguno ha coincidido
        raise ValueError(f"Tipo de archivo desconocido: {modo_cifrado}")
