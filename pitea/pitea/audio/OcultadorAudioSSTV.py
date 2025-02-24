import subprocess
from pitea.audio.OcultadorAudio import OcultadorAudio
from PIL import Image
from pitea.utils import cargar_configuracion
from pathlib import Path

from pitea.mensajes import print
import builtins
from pitea.constantes import FORMATO_IMAGEN_DESOCULTACION, RUTA_IMAGEN_DESOCULTACION, ARCHIVO_CONFIG, FORMATO_AUDIO_OCULTACION, MODES_SSTV, RUTA_AUDIO_CONTENEDOR, RUTA_IMAGEN_CONTENEDORA,RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA


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

        # Conviertos rutas relativas a absolutas para que los mensajes sean solo copiar y pegar y poder funcionar todo
        RUTA_AUDIO = Path(f"{self.ruta_audio}").resolve()  
        RUTA_IMAGEN_DESOCULTACION_absoluta = ( Path.cwd() / Path(RUTA_IMAGEN_DESOCULTACION)).resolve()

        while True:
            builtins.print(f"Una vez abierto QSSTV elija el audio con ruta \033[1;33m{RUTA_AUDIO}\033[0m")
            builtins.print(f"Asegúrese de guardar la imagen como \033[1;33m{str(RUTA_IMAGEN_DESOCULTACION_absoluta) % FORMATO_IMAGEN_DESOCULTACION}\033[0m")
            subprocess.run(["qsstv"])

            # Verificar si hay exactamente un archivo PNG en la ruta
            ruta_padre=Path(RUTA_IMAGEN_DESOCULTACION).parent
            archivos_png = list(ruta_padre.glob("*.png"))  # Busca archivos con extensión .png

            if len(archivos_png) >= 1:  # Solo se rompe el bucle si hay exactamente un archivo PNG
                break
            else :
                raise Exception(f"No hay nigun archivo 'png' en el directorio pedido: {ruta_padre}")






        
        
    def ocultar_guardar(self, formato_imagen, ruta_saida):

        #Cargamos el modo de sstv del archivo de configuracion
        conf = cargar_configuracion(ARCHIVO_CONFIG)
        modo = conf['Ajustes_sstv']["modo_sstv"]
        samples_per_sec=conf['Ajustes_sstv']["samples_per_sec"]
        bits=conf['Ajustes_sstv']["bits"]
        
        #Leemos la imagen con Pillow, Image.Resampling.LANCZOS suaviza la foto al redimensionarla
        image = Image.open(str(RUTA_IMAGEN_CONTENEDORA) % formato_imagen).resize(MODES_SSTV[modo][1], Image.Resampling.LANCZOS)

        self.guardar_imagen_redimensionada(image,str(RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA) % formato_imagen) 

        sstv = self.ocultar(None,modo,image,samples_per_sec,bits)
        
        
        self.guardar(str(RUTA_AUDIO_CONTENEDOR) % FORMATO_AUDIO_OCULTACION,sstv)
        self.guardar(ruta_saida,sstv)
        


    def desocultar_guardar(self):
        self.desocultar()

        return None
