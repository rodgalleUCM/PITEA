from pitea.AbstractFactory import AbstractFactory
from pitea.audio.OcultadorAudioLSB import OcultadorAudioLSB
from pitea.audio.OcultadorAudioSSTV import OcultadorAudioSSTV
from pitea.audio.OcultadorAudioNone import OcultadorAudioNone


class OcultadorAudioFactory(AbstractFactory):
    """
    Fábrica para obtener el constructor adecuado de ocultador de audio según el modo seleccionado.

    Esta fábrica permite crear instancias de diferentes estrategias de ocultación de audio
    según el método especificado.

    Atributos:
        lista_ocultadores (list): Lista de clases de ocultadores de audio disponibles.

    Métodos:
        get_builder(modo_ocultacion, ruta_audio):
            Devuelve una instancia del ocultador de audio correspondiente.
    """

    lista_ocultadores = [OcultadorAudioLSB, OcultadorAudioSSTV, OcultadorAudioNone]

    @staticmethod
    def get_builder(modo_ocultacion, ruta_audio):
        """
        Devuelve el constructor de ocultador de audio correspondiente según el modo seleccionado.

        Args:
            modo_ocultacion (str): Nombre del modo de ocultación de audio.
            ruta_audio (str): Ruta del archivo de audio sobre el cual se aplicará la ocultación.

        Returns:
            OcultadorAudio: Instancia de la subclase de `OcultadorAudio` correspondiente.

        Raises:
            ValueError: Si el modo de ocultación especificado no es válido.
        """
        for ocultador in OcultadorAudioFactory.lista_ocultadores:
            if ocultador.nombre == modo_ocultacion:
                return ocultador(ruta_audio)

        # Si ningún ocultador coincide con el nombre dado, se lanza un error
        raise ValueError(f"Tipo de ocultador de audio desconocido: {modo_ocultacion}")
