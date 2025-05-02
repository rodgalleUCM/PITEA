from abc import ABC, abstractmethod
import wave
from constantes import constantes
from pitea.mensajes import print

class OcultadorAudio(ABC):
    """
    Clase base para estrategias de ocultación/desocultación de datos en audio WAV.

    Debe ser extendida por implementaciones específicas (LSB, SSTV, None).

    Atributos:
        nombre (str): Identificador del modo de ocultación.
        _audio (wave.Wave_read): Recurso de audio abierto para leer parámetros y frames.
        _formato (str): Extensión del archivo de audio (p.ej., 'wav').
        _ruta_audio (str): Ruta al archivo de audio contenedor.
    """

    nombre= ""

    def __init__(self, ruta_audio):
        """
        Inicializa el ocultador con un archivo de audio WAV.

        Args:
            ruta_audio (str): Ruta al archivo WAV donde se ocultarán o extraerán datos.

        Raises:
            ValueError: Si el archivo no es válido o no se puede abrir.
        """
        
        self._audio = None
        self._formato = None
        self._ruta_audio = ruta_audio

        if ruta_audio:
            try:
                self._audio = wave.open(ruta_audio, mode="rb")
                self._formato = ruta_audio.split(".")[-1]
            except wave.Error as e:
                raise ValueError(f"Error al abrir el archivo de audio: {e}")



    def __guardar(self, ruta, frames):
        """
        Guarda frames de audio en un nuevo archivo WAV conservando parámetros.

        Args:
            ruta (str): Ruta de salida para el archivo WAV modificado.
            frames (bytes): Bytes de frames de audio a escribir.

        Raises:
            ValueError: Si no se cargó audio previamente.
        """
        if not self._audio:
            raise ValueError("El archivo de audio original no está cargado.")

        with wave.open(ruta, "wb") as audio_modificado:
            audio_modificado.setparams(self._audio.getparams())  # Copiar los parámetros del original
            audio_modificado.writeframes(frames)  # Escribir los frames modificados

        print(f"Archivo de audio guardado en: {ruta}")

    @abstractmethod
    def _ocultar(self, datos):
        """
        Inserta datos en los frames de audio.

        Debe ser implementado por subclases para modificar frames (p.ej., LSB en audio).

        Args:
            datos (bytes): Datos binarios (imagen, texto) a ocultar.

        Returns:
            bytes: Frames de audio modificados con datos embebidos.
        """
        pass

    @abstractmethod
    def _desocultar(self):
        """
        Extrae y devuelve datos embebidos de los frames de audio.

        Returns:
            bytes: Datos ocultados extraídos.
        """
        pass

    def ocultar_guardar(self, formato_imagen, ruta_salida=None):
        """
        Oculta una imagen en el archivo de audio y guarda los resultados.

        Lee la imagen contenedora generada por OcultadorImagen, extrae sus bytes,
        delega en `_ocultar` y guarda en rutas definidas y opcionales.

        Args:
            formato_imagen (str): Extensión del archivo de imagen a ocultar.
            ruta_salida (str, optional): Ruta personalizada para el audio modificado.
        """
        with open(str(constantes.RUTA_IMAGEN_CONTENEDORA) % formato_imagen, "rb") as img_file:
            datos_imagen = img_file.read()

        frames = self._ocultar(datos_imagen)

        # Guardar en la ruta por defecto
        self.__guardar(str(constantes.RUTA_AUDIO_CONTENEDOR) % constantes.FORMATO_AUDIO_OCULTACION, frames)

        # Guardar en la ruta personalizada si se especifica
        if ruta_salida:
            self.__guardar(ruta_salida, frames)

    def desocultar_guardar(self):
        """
        Extrae datos ocultos (imagen) desde el audio y guarda en archivo.

        Invoca `_desocultar`, escribe bytes de imagen y muestra log.
        """
        datos_extraidos = self._desocultar()

        ruta_salida = str(constantes.RUTA_IMAGEN_DESOCULTACION) % constantes.FORMATO_IMAGEN_DESOCULTACION
        with open(ruta_salida, "wb") as archivo_img:
            archivo_img.write(datos_extraidos)

        print(f"Imagen extraída y guardada en: {ruta_salida}")
