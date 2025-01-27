from io import BytesIO
import wave
from pitea.audio.OcultadorAudio import OcultadorAudio
from PIL import Image
from pitea.utils import cargar_configuracion

from pitea.mensajes import print
from pitea.constantes import ARCHIVO_CONFIG, FORMATO_AUDIO_OCULTACION, MODES, RUTA_AUDIO_CONTENEDOR, RUTA_IMAGEN_CONTENEDORA


class OcultadorAudioSSTV(OcultadorAudio):
    nombre = "sstv"


    def guardar(self, ruta,sstv):
        
        sstv.write_wav(ruta)  # Usar el método directo de PySSTV
        print(
                f"La imagen ha sido ocultada en el archivo de audio: {ruta}"
            )



    def ocultar(self, datos,modo="MartinM1",image=None,samples_per_sec= None,bits= None):
        
        # Instanciamos el modo SSTV
        sstv = MODES[modo](image,samples_per_sec,bits)
        
        # Generar los frames del audio codificado en SSTV
        return sstv



    def desocultar():
        pass

    def ocultar_guardar(self, formato_imagen, ruta_saida):

        #Cargamos el modo de sstv del archivo de configuracion
        conf = cargar_configuracion(ARCHIVO_CONFIG)
        modo = conf["modo_sstv"]
        samples_per_sec=conf["samples_per_sec"]
        bits=conf["bits"]
        
        #Leemos la imagen con Pillow
        image = Image.open(str(RUTA_IMAGEN_CONTENEDORA) % formato_imagen)

        sstv = self.ocultar(None,modo,image,samples_per_sec,bits)
        
        
        self.guardar(str(RUTA_AUDIO_CONTENEDOR) % FORMATO_AUDIO_OCULTACION,sstv)
        self.guardar(ruta_saida,sstv)
        


    def desocultar_guardar(self):
        frames = bytearray(list(self.audio.readframes(self.audio.getnframes())))
        tamano_imagen = 0
        self.audio.close()

        datos_binarios = ""
        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)
            if len(datos_binarios) >= 32:
                tamano_datos = int(
                    datos_binarios[:32], 2
                )  # Leer el tamaño de los datos
                datos_binarios = datos_binarios[32:]  # Eliminar la cabecera
                break  # Una vez obtenida la cabecera, podemos detener la lectura

        # Verificar que la cabecera tenga el tamaño correcto
        if tamano_datos == 0:
            raise ValueError("No se pudo extraer el tamaño de los datos ocultos.")
        # Extraer los datos de acuerdo al tamaño especificado

        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)  # Extraer el bit menos significativo
            if len(datos_binarios) >= tamano_datos + 32:
                break

        datos_binarios = datos_binarios[32:]

        datos_extraidos = int(datos_binarios, 2).to_bytes(
            tamano_datos // 8, byteorder="big"
        )

        return datos_extraidos
