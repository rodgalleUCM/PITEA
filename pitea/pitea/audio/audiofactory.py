from pitea.AbstractFactory import AbstractFactory
from pitea.audio.OcultadorAudio1 import OcultadorAudio1

class OcultadorAudioFactory(AbstractFactory) :

    @staticmethod
    def get_builder(modo_cifrado,ruta_audio):

        if modo_cifrado == '1':
            return OcultadorAudio1(ruta_audio) 
        else:
            raise ValueError(f"Tipo de archivo desconocido: {modo_cifrado}")