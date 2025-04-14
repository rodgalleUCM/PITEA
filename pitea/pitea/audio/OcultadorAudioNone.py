from pitea.audio.OcultadorAudio import OcultadorAudio


class OcultadorAudioNone(OcultadorAudio):
    """Clase de ocultación de audio que no implementa la ocultación de datos.

    Se usa únicamente para la desocultación de datos, sin realizar modificaciones en el audio.

    Attributes:
        nombre (str): Nombre del método de ocultación.
    """

    nombre= "none"

    def __init__(self, ruta_audio):
        """
        Inicializa el objeto con un archivo de audio.

        Args:
            ruta_audio (str): Ruta del archivo de audio en el que se ocultarán/extrarán datos.
        """
        super().__init_(ruta_audio)
        
       

    def _ocultar(self, datos_imagen):
        """Lanza una excepción, ya que este método no soporta la ocultación de datos.

        Args:
            datos_imagen (bytes): Datos de la imagen a ocultar.

        Raises:
            Exception: Indica que este ocultador solo sirve para desocultar.
        """
        raise Exception("El ocultador de audio none es solo para desocultar")

    def _desocultar(self):
        """Devuelve `None` ya que no se realiza ninguna operación de desocultación.

        Returns:
            None: No se extraen datos ya que este ocultador no implementa funcionalidad.
        """
        return None
