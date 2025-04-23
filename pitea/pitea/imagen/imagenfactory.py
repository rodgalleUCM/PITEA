from pitea.AbstractFactory import AbstractFactory
from pitea.imagen.OcultadorImagenLSB import OcultadorImagenLSB
from pitea.imagen.OcultadorImagenText import OcultadorImagenText
from pitea.imagen.OcultadorImagenNone import OcultadorImagenNone


class OcultadorImagenFactory(AbstractFactory):
    """
    Fábrica concreta que devuelve instancias de ocultadores de imagen basados en el modo.

    Atributos:
        lista_ocultadores (list): Clases derivadas de ocultadores de imagen soportadas.
    """
    
    lista_ocultadores = [OcultadorImagenLSB,OcultadorImagenText,OcultadorImagenNone]

    @staticmethod
    def creacion(modo_ocultacion, ruta_imagen,modo_cifrador,input_text= None):
        """
        Crea y retorna una instancia del ocultador de imagen especificado.

        Args:
            modo_ocultacion (str): Identificador del modo de ocultación ('lsb', 'text', 'none').
            ruta_imagen (str, optional): Ruta al archivo de imagen contenedora.
            modo_cifrador (str, optional): Modo de cifrado aplicado antes de ocultar.
            input_text (str, optional): Texto a ocultar en la imagen para modos de texto.

        Returns:
            OcultadorImagen: Instancia de la subclase de ocultador adecuada.

        Raises:
            ValueError: Si `modo_ocultacion` no coincide con ningún ocultador registrado.
        """

        for ocultador in OcultadorImagenFactory.lista_ocultadores:
            if ocultador.nombre == modo_ocultacion:
                return ocultador(ruta_imagen,modo_cifrador,input_text)

        # Si llega aqui esque ninguno ha coincidido
        raise ValueError(f"Tipo de archivo desconocido: {modo_ocultacion}")
