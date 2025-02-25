import subprocess
from pitea.audio.OcultadorAudio import OcultadorAudio
from PIL import Image
from pitea.utils import cargar_configuracion
from pathlib import Path
from pitea.mensajes import print
import builtins
from pitea.constantes import (
    FORMATO_IMAGEN_DESOCULTACION,
    RUTA_IMAGEN_DESOCULTACION,
    ARCHIVO_CONFIG,
    FORMATO_AUDIO_OCULTACION,
    MODES_SSTV,
    RUTA_AUDIO_CONTENEDOR,
    RUTA_IMAGEN_CONTENEDORA,
    RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA
)


class OcultadorAudioSSTV(OcultadorAudio):
    """Clase que implementa la ocultación y desocultación de datos en audio usando SSTV.

    Attributes:
        nombre (str): Nombre del método de ocultación.

    Methods:
        guardar(ruta, sstv):
            Guarda el audio generado por SSTV en un archivo WAV.

        guardar_imagen_redimensionada(imagen, ruta):
            Guarda la imagen redimensionada en una ruta específica.

        ocultar(datos, modo="MartinM1", image=None, samples_per_sec=None, bits=None):
            Codifica la imagen en un archivo de audio usando el modo SSTV seleccionado.

        desocultar():
            Abre QSSTV para decodificar la imagen oculta en el archivo de audio.

        ocultar_guardar(formato_imagen, ruta_salida):
            Codifica una imagen en audio SSTV y la guarda en un archivo.

        desocultar_guardar():
            Ejecuta la desocultación de la imagen desde el archivo de audio SSTV y la guarda.
    """

    nombre = "sstv"

    def guardar(self, ruta, sstv):
        """Guarda el audio generado por SSTV en un archivo WAV.

        Args:
            ruta (str): Ruta donde se guardará el archivo de audio.
            sstv (PySSTV): Objeto de codificación SSTV que genera el audio.
        """
        sstv.write_wav(ruta)  # Usar el método directo de PySSTV
        print(f"La imagen ha sido ocultada en el archivo de audio: {ruta}")

    def guardar_imagen_redimensionada(self, imagen, ruta):
        """Guarda la imagen redimensionada en una ruta específica.

        Args:
            imagen (PIL.Image): Imagen redimensionada.
            ruta (str): Ruta donde se guardará la imagen.
        """
        imagen.save(ruta)
        print(f"Imagen contenedora redimensionada guardada en {ruta}")

    def ocultar(self, datos, modo="MartinM1", image=None, samples_per_sec=None, bits=None):
        """Codifica la imagen en un archivo de audio usando el modo SSTV seleccionado.

        Args:
            datos (bytes): Datos a ocultar (no utilizado en este método).
            modo (str, optional): Modo de codificación SSTV. Default es "MartinM1".
            image (PIL.Image, optional): Imagen a ocultar en el audio SSTV.
            samples_per_sec (int, optional): Frecuencia de muestreo del audio.
            bits (int, optional): Resolución de bits del audio.

        Returns:
            PySSTV: Objeto de codificación SSTV.
        """
        sstv = MODES_SSTV[modo][0](image, samples_per_sec, bits)
        return sstv

    def desocultar(self):
        """Abre QSSTV para decodificar la imagen oculta en el archivo de audio.

        Raises:
            Exception: Si no se encuentra ninguna imagen decodificada después de ejecutar QSSTV.
        """
        RUTA_AUDIO = Path(f"{self.ruta_audio}").resolve()
        RUTA_IMAGEN_DESOCULTACION_absoluta = (Path.cwd() / Path(RUTA_IMAGEN_DESOCULTACION)).resolve()

        while True:
            builtins.print(f"Una vez abierto QSSTV, elija el audio con ruta \033[1;33m{RUTA_AUDIO}\033[0m")
            builtins.print(f"Elija el modo \033[1;33m {cargar_configuracion(ARCHIVO_CONFIG)['Ajustes_sstv']['modo_sstv']} \033[0m")
            builtins.print(f"Asegúrese de guardar la imagen como \033[1;33m{str(RUTA_IMAGEN_DESOCULTACION_absoluta) % FORMATO_IMAGEN_DESOCULTACION}\033[0m")
            subprocess.run(["qsstv"])

            # Verificar si hay al menos un archivo PNG en la ruta
            ruta_padre = Path(RUTA_IMAGEN_DESOCULTACION).parent
            archivos_png = list(ruta_padre.glob("*.png"))

            if len(archivos_png) >= 1:
                break
            else:
                raise Exception(f"No hay ningún archivo 'png' en el directorio especificado: {ruta_padre}")

    def ocultar_guardar(self, formato_imagen, ruta_salida):
        """Codifica una imagen en audio SSTV y la guarda en un archivo.

        Args:
            formato_imagen (str): Formato de la imagen a ocultar.
            ruta_salida (str): Ruta donde se guardará el audio generado.
        """
        # Cargar configuración de SSTV desde archivo
        conf = cargar_configuracion(ARCHIVO_CONFIG)
        modo = conf['Ajustes_sstv']["modo_sstv"]
        samples_per_sec = conf['Ajustes_sstv']["samples_per_sec"]
        bits = conf['Ajustes_sstv']["bits"]

        # Leer y redimensionar la imagen con Pillow
        image = Image.open(str(RUTA_IMAGEN_CONTENEDORA) % formato_imagen).resize(
            MODES_SSTV[modo][1], Image.Resampling.LANCZOS
        )

        self.guardar_imagen_redimensionada(image, str(RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA) % formato_imagen)

        # Codificar imagen en audio SSTV
        sstv = self.ocultar(None, modo, image, samples_per_sec, bits)

        # Guardar el archivo de audio
        self.guardar(str(RUTA_AUDIO_CONTENEDOR) % FORMATO_AUDIO_OCULTACION, sstv)
        self.guardar(ruta_salida, sstv)

    def desocultar_guardar(self):
        """Ejecuta la desocultación de la imagen desde el archivo de audio SSTV y la guarda."""
        self.desocultar()
        return None
