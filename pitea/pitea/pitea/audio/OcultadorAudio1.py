import wave
from pitea.audio.OcultadorAudio import OcultadorAudio
from pitea.constantes import RUTA_IMAGEN_CONTENEDORA,RUTA_AUDIO_CONTENEDOR,RUTA_IMAGEN_DESOCULTACION
from pitea.mensajes import print

class OcultadorAudio1(OcultadorAudio) :
       
    def ocultar(self,formato,ruta_salida) :
        with open(RUTA_IMAGEN_CONTENEDORA %formato, 'rb') as img_file:
            datos_imagen = img_file.read()
    
        binarios_imagen = ''.join(format(byte, '08b') for byte in datos_imagen) # Convertir los datos de la imagen a binarios
        
        assert self.audio.getsampwidth() == 2, "El archivo de audio debe ser de 16 bits" # Asegurarse de que el archivo de audio sea de 16 bits
        
        frames = bytearray(list(self.audio.readframes(self.audio.getnframes()))) # Leer los frames del archivo de audio
        
        if len(binarios_imagen) > len(frames) * 8: # Asegurarse de que la imagen pueda ser ocultada en el archivo de audio
            raise ValueError("La imagen es demasiado grande para ser ocultada en este archivo de audio.")
        
        indice_datos = 0
        for i in range(len(frames)): # Iterar sobre los frames del archivo de audio
            if indice_datos < len(binarios_imagen): # Si todavía hay datos para ocultar
                frames[i] = (frames[i] & 254) | int(binarios_imagen[indice_datos]) # Ocultar el bit menos significativo
                indice_datos += 1
        
        with wave.open(RUTA_AUDIO_CONTENEDOR, 'wb') as audio_modificado: # Guardar los frames modificados en un nuevo archivo de audio
            audio_modificado.setparams(self.audio.getparams())  # Copiar los parámetros del archivo de audio original
            audio_modificado.writeframes(frames) # Escribir los frames modificados

        if ruta_salida :
            with wave.open(ruta_salida, 'wb') as audio_modificado: # Guardar los frames modificados en un nuevo archivo de audio
                audio_modificado.setparams(self.audio.getparams())  # Copiar los parámetros del archivo de audio original
                audio_modificado.writeframes(frames) # Escribir los frames modificados
                print(f'La imagen ha sido ocultada en el archivo de audio: {ruta_salida }')
        
        self.audio.close()
        
        print(f'La imagen ha sido ocultada en el archivo de audio: {RUTA_AUDIO_CONTENEDOR % self.formato}')

    def desocultar(self) :
        frames = bytearray(list(self.audio.readframes(self.audio.getnframes())))
        tamano_imagen= 0
        self.audio.close()
        formato = "png"

        datos_binarios = ''
        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)
        
        datos_extraidos = int(datos_binarios[:tamano_imagen * 8], 2).to_bytes(tamano_imagen, byteorder='big')

        with open(RUTA_IMAGEN_DESOCULTACION % formato, 'wb') as archivo_img:
            archivo_img.write(datos_extraidos)
        
        print(f'La imagen ha sido extraída y guardada en {RUTA_IMAGEN_DESOCULTACION %formato}')
