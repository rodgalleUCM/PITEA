from pitea.AbstractFactory import AbstractFactory
from pitea.audio.OcultadorAudioLSB import OcultadorAudioLSB
from pitea.audio.OcultadorAudioSSTV import OcultadorAudioSSTV
from pitea.audio.OcultadorAudioNone import OcultadorAudioNone


class OcultadorAudioFactory(AbstractFactory):
    """
    Fábrica concreta para obtener instancias de ocultadores de audio.

    Atributos:
        lista_ocultadores (list): Clases derivadas de ocultadores de audio soportadas.
    """

    lista_ocultadores = [OcultadorAudioLSB, OcultadorAudioSSTV, OcultadorAudioNone]

    @staticmethod
    def creacion(modo_ocultacion, ruta_audio):
        """
        Crea y retorna el ocultador de audio correspondiente al modo.

        Args:
            modo_ocultacion (str): Identificador del método de ocultación ('lsb', 'sstv', 'none').
            ruta_audio (str): Ruta al archivo de audio contenedor.

        Returns:
            OcultadorAudio: Instancia de la clase de ocultación seleccionada.

        Raises:
            ValueError: Si `modo_ocultacion` no coincide con ninguna clase registrada.
        """
        for ocultador in OcultadorAudioFactory.lista_ocultadores:
            if ocultador.nombre == modo_ocultacion:
                return ocultador(ruta_audio)

        # Si ningún ocultador coincide con el nombre dado, se lanza un error
        raise ValueError(f"Tipo de ocultador de audio desconocido: {modo_ocultacion}")
