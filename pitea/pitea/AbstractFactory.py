from abc import ABC
class AbstractFactory(ABC):
    """
    Fábrica abstracta para obtener el constructor adecuado de ocultadores de datos basado en el modo de cifrado.

    Methods:
        creacion(modo_cifrado):
            Devuelve el objeto correspondiente según el modo de cifrado.
    """

    @staticmethod
    def creacion(modo_cifrado):
        """Devuelve el objeto correspondiente según el modo de cifrado.

        Args:
            modo_cifrado (str): Nombre del modo de cifrado o ocultacion, determinado por el parseo de argumentos en el script de ejecución.

        Returns:
            Object: Una instancia del objeto construido

        Raises:
            ValueError: Si el modo de cifrado es desconocido.
        """
        pass
