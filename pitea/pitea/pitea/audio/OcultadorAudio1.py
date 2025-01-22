import wave
from pitea.audio.OcultadorAudio import OcultadorAudio

from pitea.mensajes import print

class OcultadorAudio1(OcultadorAudio) :
       
    def ocultar(self,datos_imagen) :
        
    
        binarios_imagen = ''.join(format(byte, '08b') for byte in datos_imagen) # Convertir los datos de la imagen a binarios

        # Añadir una cabecera con el tamaño de los datos (32 bits)
        tamano_datos = format(len(binarios_imagen), '032b')
        binarios_imagen = tamano_datos + binarios_imagen  # Cabecera + Datos
        
        assert self.audio.getsampwidth() == 2, "El archivo de audio debe ser de 16 bits" # Asegurarse de que el archivo de audio sea de 16 bits
        
        frames = bytearray(list(self.audio.readframes(self.audio.getnframes()))) # Leer los frames del archivo de audio
        
        if len(binarios_imagen) > len(frames) * 8: # Asegurarse de que la imagen pueda ser ocultada en el archivo de audio
            raise ValueError("La imagen es demasiado grande para ser ocultada en este archivo de audio.")
        
        indice_datos = 0
        for i in range(len(frames)): # Iterar sobre los frames del archivo de audio
            if indice_datos < len(binarios_imagen): # Si todavía hay datos para ocultar
                frames[i] = (frames[i] & 254) | int(binarios_imagen[indice_datos]) # Ocultar el bit menos significativo
                indice_datos += 1

        self.audio.close()

        return frames
        
        print(f'La imagen ha sido ocultada en el archivo de audio: {str(RUTA_AUDIO_CONTENEDOR) % self.formato}')

    def desocultar(self) :
        frames = bytearray(list(self.audio.readframes(self.audio.getnframes())))
        tamano_imagen= 0
        self.audio.close()

        datos_binarios = ''
        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)
            if len(datos_binarios) >= 32:
                tamano_datos = int(datos_binarios[:32], 2)  # Leer el tamaño de los datos
                datos_binarios = datos_binarios[32:]  # Eliminar la cabecera
                break  # Una vez obtenida la cabecera, podemos detener la lectura
        
        # Verificar que la cabecera tenga el tamaño correcto
        if tamano_datos == 0:
            raise ValueError("No se pudo extraer el tamaño de los datos ocultos.")
        # Extraer los datos de acuerdo al tamaño especificado
    
        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)  # Extraer el bit menos significativo
            if len(datos_binarios) >= tamano_datos+32:
                break

        datos_binarios = datos_binarios[32:]
            
        datos_extraidos = int(datos_binarios, 2).to_bytes(tamano_datos// 8, byteorder='big')

        return datos_extraidos
        