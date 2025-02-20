from abc import ABC, abstractmethod
import wave
from pitea.constantes import (
    FORMATO_AUDIO_OCULTACION,
    FORMATO_IMAGEN_DESOCULTACION,
    RUTA_IMAGEN_CONTENEDORA,
    RUTA_AUDIO_CONTENEDOR,
    RUTA_IMAGEN_DESOCULTACION,
)

class OcultadorAudio(ABC):
    nombre = ""


    def __init__(self, ruta_audio):
        if ruta_audio:
            self.audio = wave.open(ruta_audio, mode="rb")
            self.formato = ruta_audio.split(".")[-1]
            self.ruta_audio = ruta_audio

    def guardar(self,ruta,frames) :
        with (
            wave.open(
                ruta, "wb"
            ) as audio_modificado
        ):  # Guardar los frames modificados en un nuevo archivo de audio
            audio_modificado.setparams(
                self.audio.getparams()
            )  # Copiar los parámetros del archivo de audio original
            audio_modificado.writeframes(frames)  # Escribir los frames modificados

            print(
                    f"La imagen ha sido ocultada en el archivo de audio: {ruta}"
                )

    @abstractmethod
    def ocultar(self, datos):
        pass

    @abstractmethod
    def desocultar():
        pass

    def ocultar_guardar(self, formato_imagen, ruta_salida):
        with open(str(RUTA_IMAGEN_CONTENEDORA) % formato_imagen, "rb") as img_file:
            datos_imagen = img_file.read()

        frames = self.ocultar(datos_imagen)

        self.guardar(str(RUTA_AUDIO_CONTENEDOR) % FORMATO_AUDIO_OCULTACION,frames)

        if ruta_salida:
            self.guardar(ruta_salida,frames)
            
            

    def desocultar_guardar(self):
        datos_extraidos = self.desocultar()

        with open(
            str(RUTA_IMAGEN_DESOCULTACION) % FORMATO_IMAGEN_DESOCULTACION, "wb"
        ) as archivo_img:
            archivo_img.write(datos_extraidos)

        print(
            f"La imagen ha sido extraída y guardada en {str(RUTA_IMAGEN_DESOCULTACION) % FORMATO_IMAGEN_DESOCULTACION}"
        )
