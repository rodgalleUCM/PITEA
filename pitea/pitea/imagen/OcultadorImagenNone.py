import base64

from pitea.imagen.OcultadorImagen import OcultadorImagen

from constantes import constantes
from pitea.mensajes import print

class OcultadorImagenNone(OcultadorImagen):
    """
    Ocultador de imagen nulo que no inserta datos en la imagen.

    Utilizado exclusivamente para desocultar datos previamente guardados
    en un archivo de texto (`ruta_txt`).

    Atributos:
        nombre (str): Identificador del modo, "none".
    """

    nombre = "none"

    def __init__(self, ruta_imagen, modo_cifrador, ruta_txt=None):
        """
        Inicializa el ocultador nulo.

        Args:
            ruta_imagen (str, optional): Ignorada en este modo.
            modo_cifrador (str): Indica si los datos están cifrados.
            ruta_txt (str): Ruta al archivo de texto con datos ocultados.
        """
        super().__init__(ruta_imagen, modo_cifrador, ruta_txt)
        

    
    def _ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
        """
        No implementado para modo 'none'.

        Raises:
            NotImplementedError: Siempre, ya que no se oculta en este modo.
        """
        raise Exception("El modo Ocultador de imagen None no es valido para ocultacion, solo para desocultacion")

    def _desocultar(self):
        """
        Extrae datos desde archivo de texto.

        Si `self._cifrado` es True, decodifica base64;
        de lo contrario, retorna bytes sin cambios.

        Returns:
            bytes: Datos extraídos.

        Raises:
            FileNotFoundError: Si `self._ruta_txt` no apunta a un archivo existente.
        """
        with open(self._ruta_txt, 'rb') as f:
            datos = f.read()
        
        if self._cifrado:
            return base64.b64decode(datos)
        else:
            return datos

    def desocultar_guardar(self):
        """
        Gestiona la extracción y almacenamiento de los datos desocultados.

        1. Llama a `_desocultar`.
        2. Escribe los bytes resultantes en el archivo de cache de desocultación.
        3. Muestra un mensaje en verbose.
        """
        datos_extraidos = self._desocultar()

        with open(constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION, "wb") as f:
            f.write(datos_extraidos)

        print(f"Datos cifrados guardados en {constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION}")
