from abc import ABC, abstractmethod
import wave
from PIL import Image
class OcultadorAudio(ABC) :
       
    def __init__(self,ruta_audio):
        if ruta_audio :
            self.audio = wave.open(ruta_audio, mode='rb')
            self.formato = ruta_audio.split(".")[-1]

    @abstractmethod
    def ocultar(datos) :
        pass
    @abstractmethod
    def desocultar() :
        pass