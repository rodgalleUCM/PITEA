from pitea.cifradores.CifradorAES import  CifradorAES
from pitea.AbstractFactory import AbstractFactory
from pitea.cifradores.CifradorNone import CifradorNone


class CifradorFactory(AbstractFactory):
    lista_cifradores = [CifradorAES,CifradorNone]
    """
    Fábrica para obtener el constructor de Cifrador adecuado basado en el tipo de archivo.

    Métodos
    -------
    get_builder(modo_cifrado,clave):
        Devuelve el constructor de Cifrador correspondiente según el tipo de archivo.
    """

    @staticmethod
    def get_builder(modo_cifrado, clave, ruta):
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
        for cifrador in CifradorFactory.lista_cifradores:
            if cifrador.nombre == modo_cifrado:
                return cifrador(clave, ruta)

        else:
            raise ValueError(f"Tipo de cifrador desconocido: {modo_cifrado}")
