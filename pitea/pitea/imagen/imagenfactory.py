from pitea.AbstractFactory import AbstractFactory
from pitea.imagen.OcultadorImagenLSB import OcultadorImagenLSB
from pitea.imagen.OcultadorImagenText import OcultadorImagenText
from pitea.imagen.OcultadorImagenNone import OcultadorImagenNone


class OcultadorImagenFactory(AbstractFactory):
    """
    Fábrica para obtener el constructor adecuado de ocultadores de imagen basado en el modo de ocultaci´on

    Atributos:
        lista_ocultadores (list): Lista de clases de ocultadores de imagen disponibles.

    Métodos:
        get_builder(modo_ocultacion, ruta_imagen, modo_cifrador, input_text=None):
            Devuelve el constructor adecuado de OcultadorImagen según el modo de cifrado.
    """

    lista_ocultadores = [OcultadorImagenLSB,OcultadorImagenText,OcultadorImagenNone]

    @staticmethod
    def get_builder(modo_ocultacion, ruta_imagen,modo_cifrador,input_text= None):
        """Devuelve el constructor de OcultadorImagen correspondiente según el modo de cifrado.

        Args:
            modo_ocultacion (str): Nombre del modo de cifrado, determinado por el parseo de argumentos en el script de ejecución.
            ruta_imagen (str , None): Ruta del archivo de imagen contenedora.
            modo_cifrador (str): Modo de cifrado que se desea utilizar.
            input_text (str, optional): Texto a ocultar en la imagen, utilizado en OcultadorImagenNone (por defecto es None).

        Returns:
            OcultadorImagen: Una instancia del ocultador de imagen correspondiente al modo de cifrado.

        Raises:
            ValueError: Si el modo de cifrado es desconocido.
        """

        for ocultador in OcultadorImagenFactory.lista_ocultadores:
            if ocultador.nombre == modo_ocultacion:
                return ocultador(ruta_imagen,modo_cifrador,input_text)

        # Si llega aqui esque ninguno ha coincidido
        raise ValueError(f"Tipo de archivo desconocido: {modo_ocultacion}")
