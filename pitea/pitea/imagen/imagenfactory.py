from pitea.AbstractFactory import AbstractFactory
from pitea.imagen.OcultadorImagenLSB import OcultadorImagenLSB


class OcultadorImagenFactory(AbstractFactory):
    lista_ocultadores = [OcultadorImagenLSB]

    @staticmethod
    def get_builder(modo_cifrado, ruta_imagen):
        for ocultador in OcultadorImagenFactory.lista_ocultadores:
            if ocultador.nombre == modo_cifrado:
                return ocultador(ruta_imagen)

        # Si llega aqui esque ninguno ha coincidido
        raise ValueError(f"Tipo de archivo desconocido: {modo_cifrado}")
