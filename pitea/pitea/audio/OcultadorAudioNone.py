from pitea.audio.OcultadorAudio import OcultadorAudio



class OcultadorAudioNone(OcultadorAudio):
    nombre = "none"

    def ocultar(self, datos_imagen):
        raise Exception("El ocultador de audio none es solo para desocultar")
       

    def desocultar(self):
        return None
