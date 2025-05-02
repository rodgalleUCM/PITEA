from pitea.audio.OcultadorAudio import OcultadorAudio


class OcultadorAudioNone(OcultadorAudio):
    """
    Ocultador de audio nulo que no inserta datos.

    Útil para desocultar datos de audio sin alteración.

    Atributos:
        nombre (str): Identificador del modo, "none".
    """

    nombre= "none"

    def __init__(self, ruta_audio):
        """
        Inicializa el ocultador nulo con ruta al archivo de audio.

        Args:
            ruta_audio (str): Ruta al archivo WAV para desocultación.

        Raises:
            ValueError: Si no se puede abrir el archivo de audio.
        """
        super().__init_(ruta_audio)
        
       

    def _ocultar(self, datos_imagen):
        """
        No implementado para modo 'none'.

        Raises:
            NotImplementedError: Siempre, ya que no se oculta en este modo.
        """
        raise Exception("El ocultador de audio none es solo para desocultar")

    def _desocultar(self):
        """
        Devuelve None, pues no hay lógica de extracción de datos en modo nulo.

        Returns:
            None
        """
        return None
