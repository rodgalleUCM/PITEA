import subprocess
from pitea.audio.OcultadorAudio import OcultadorAudio
from PIL import Image
from pitea.utils import cargar_configuracion

from pitea.mensajes import print
from pitea.constantes import ARCHIVO_CONFIG, FORMATO_AUDIO_OCULTACION, MODES_SSTV, RUTA_AUDIO_CONTENEDOR, RUTA_IMAGEN_CONTENEDORA,RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA


class OcultadorAudioSSTV(OcultadorAudio):
    nombre = "sstv"


    def guardar(self, ruta,sstv):
        
        sstv.write_wav(ruta)  # Usar el método directo de PySSTV
        print(
                f"La imagen ha sido ocultada en el archivo de audio: {ruta}"
            )
        
    def guardar_imagen_redimensionada(self,imagen,ruta) :
        imagen.save(ruta)

        print(
                f"Imagen contenedora redimensionada guardada en {ruta}"
            )


    def ocultar(self, datos,modo="MartinM1",image=None,samples_per_sec= None,bits= None):
        
        # Instanciamos el modo SSTV
        sstv = MODES_SSTV[modo][0](image,samples_per_sec,bits)
        
        # Generar los frames del audio codificado en SSTV
        return sstv



    def desocultar(self):
        subprocess.run(["qsstv"])
        
    def ocultar_guardar(self, formato_imagen, ruta_saida):

        #Cargamos el modo de sstv del archivo de configuracion
        conf = cargar_configuracion(ARCHIVO_CONFIG)
        modo = conf["modo_sstv"]
        samples_per_sec=conf["samples_per_sec"]
        bits=conf["bits"]
        
        #Leemos la imagen con Pillow, Image.Resampling.LANCZOS suaviza la foto al redimensionarla
        image = Image.open(str(RUTA_IMAGEN_CONTENEDORA) % formato_imagen).resize(MODES_SSTV[modo][1], Image.Resampling.LANCZOS)

        self.guardar_imagen_redimensionada(image,str(RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA) % formato_imagen) 

        sstv = self.ocultar(None,modo,image,samples_per_sec,bits)
        
        
        self.guardar(str(RUTA_AUDIO_CONTENEDOR) % FORMATO_AUDIO_OCULTACION,sstv)
        self.guardar(ruta_saida,sstv)
        


    def desocultar_guardar(self):
        self.desocultar()

        return None
