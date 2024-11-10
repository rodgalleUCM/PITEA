from pitea.cifradores.Cifrador_AES import Cifrador_AES
from pitea.AbstractFactory import AbstractFactory
class CifradorFactory(AbstractFactory) :
    """
    Fábrica para obtener el constructor de Cifrador adecuado basado en el tipo de archivo.

    Métodos
    -------
    get_builder(modo_cifrado,clave):
        Devuelve el constructor de Cifrador correspondiente según el tipo de archivo.
    """
    @staticmethod
    def get_builder(modo_cifrado,clave):
        """
        Devuelve el constructor de cifrador correspondiente según el modo de cifrado.

        Parameters
        ----------
        modo_cifrado :   str
                         nombre del modo de cifrado , el cual esta acotado por el parseo de argumentos de script_ejecucion.py

        Returns
        -------
        CifradorBuilder
            Una instancia de la subclase de CifradorBuilder correspondiente.

        Raises
        ------
        ValueError
            Si el modo de cifrado es desconocido.
        """
        if modo_cifrado == 'aes':
            return Cifrador_AES(clave)
       
        else:
            raise ValueError(f"Tipo de archivo desconocido: {modo_cifrado}")