from pitea.AbstractFactory import AbstractFactory
from pitea.audio.OcultadorAudioLSB import OcultadorAudioLSB


class OcultadorAudioFactory(AbstractFactory):
    lista_ocultadores = [OcultadorAudioLSB]

    @staticmethod
    def get_builder(modo_cifrado, ruta_audio):
        for ocultador in OcultadorAudioFactory.lista_ocultadores:
            if ocultador.nombre == modo_cifrado:
                return ocultador(ruta_audio)

        # Si llega aqui esque ninguno ha coincidido
        raise ValueError(f"Tipo de archivo desconocido: {modo_cifrado}")
