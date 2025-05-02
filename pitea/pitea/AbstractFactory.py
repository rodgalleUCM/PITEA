from abc import ABC
class AbstractFactory(ABC):
    """
    Fábrica abstracta que delega la creación de objetos de ocultación o cifrado
    basándose en el modo especificado.

    Métodos estáticos:
        creacion(modo_cifrado: str) -> object:
            Retorna una instancia del constructor apropiado para el modo dado.
    """

    @staticmethod
    def creacion(modo_cifrado):
        """Devuelve el objeto correspondiente según el modo de cifrado.

        Args:
            modo_cifrado (str): Nombre del modo de cifrado o ocultacion, determinado por el parseo de argumentos en el script de ejecución.

        Returns:
            Object: Una instancia del objeto construido
        """
        pass
