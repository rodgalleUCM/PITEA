from abc import ABC, abstractmethod
import wave
from PIL import Image
from pitea.constantes import FORMATO_IMAGEN_DESOCULTACION, RUTA_IMAGEN_CONTENEDORA,RUTA_AUDIO_CONTENEDOR,RUTA_IMAGEN_DESOCULTACION
class OcultadorAudio(ABC) :
    
    def __init__(self):
        pass
       
    def __init__(self,ruta_audio):
            self.audio = wave.open(ruta_audio, mode='rb')
            self.formato = ruta_audio.split(".")[-1]

    @abstractmethod
    def ocultar(self,datos) :
        pass
    @abstractmethod
    def desocultar() :
        pass


    def ocultar_guardar(self,formato,ruta_salida) :
        with open(str(RUTA_IMAGEN_CONTENEDORA) %formato, 'rb') as img_file:
            datos_imagen = img_file.read()

        frames = self.ocultar(datos_imagen)

        with wave.open(str(RUTA_AUDIO_CONTENEDOR) % formato, 'wb') as audio_modificado: # Guardar los frames modificados en un nuevo archivo de audio
            audio_modificado.setparams(self.audio.getparams())  # Copiar los parámetros del archivo de audio original
            audio_modificado.writeframes(frames) # Escribir los frames modificados

        if ruta_salida :
            with wave.open(ruta_salida, 'wb') as audio_modificado: # Guardar los frames modificados en un nuevo archivo de audio
                audio_modificado.setparams(self.audio.getparams())  # Copiar los parámetros del archivo de audio original
                audio_modificado.writeframes(frames) # Escribir los frames modificados
                print(f'La imagen ha sido ocultada en el archivo de audio: {ruta_salida }')

        
  
    def desocultar_guardar(self) :
        datos_extraidos = self.desocultar()

        with open(str(RUTA_IMAGEN_DESOCULTACION) % FORMATO_IMAGEN_DESOCULTACION, 'wb') as archivo_img:
            archivo_img.write(datos_extraidos)
        
        print(f'La imagen ha sido extraída y guardada en {str(RUTA_IMAGEN_DESOCULTACION) % FORMATO_IMAGEN_DESOCULTACION}')

