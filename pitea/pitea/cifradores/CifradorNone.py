from pitea.cifradores.Cifrador import Cifrador


class CifradorNone(Cifrador):
    """
    Cifrador nulo que no modifica los datos.

    Mantiene la misma interfaz que otros cifradores para compatibilidad,
    pero `_cifrar` y `_descifrar` retornan los datos inalterados.

    Atributos:
        nombre (str): Identificador del cifrador, "none".
    """

    nombre = "none"

    def __init__(self, contraseña, ruta=None):
        """
        Inicializa el cifrador nulo con contraseña y ruta opcional.

        Args:
            contraseña (str): Contraseña (no utilizada en este cifrador).
            ruta (str, opcional): Ruta de salida para datos, si aplica.
        """
        super().__init__(contraseña,ruta)

    def _cifrar(self, datos):
        """
        Simula el cifrado sin modificar los datos.

        Args:
            datos (bytes): Datos originales.

        Returns:
            tuple(bytes, bytes): Tupla con IV vacío y datos originales.
        """
        return b"", datos

    def _descifrar(self, datos):
        """
        Simula el descifrado sin modificar los datos.

        Args:
            datos (bytes): Datos cifrados.

        Returns:
            bytes: Los mismos datos recibidos.
        """
        return datos
