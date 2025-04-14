from pitea.cifradores.CifradorAES import CifradorAES
from pitea.AbstractFactory import AbstractFactory
from pitea.cifradores.CifradorNone import CifradorNone


class CifradorFactory(AbstractFactory):
    """
    Fábrica para obtener el constructor de Cifrador adecuado basado en el tipo de archivo.

    Esta clase permite obtener el constructor correspondiente de un cifrador basado en el tipo de cifrado
    seleccionado (AES, None, etc.). A través de su método estático `creacion`, se puede obtener una instancia
    de la subclase de Cifrador adecuada.

    Atributos:
        lista_cifradores (list): Lista de clases de cifradores disponibles.
    """


    lista_cifradores = [CifradorAES, CifradorNone]

    @staticmethod
    def creacion(modo_cifrado, clave, ruta = None):
        """
        Devuelve el objeto de cifrador correspondiente según el modo de cifrado.

        Este método selecciona y devuelve una instancia de la subclase de Cifrador adecuada según el modo de cifrado
        que se pasa como parámetro. Si el modo de cifrado no es reconocido, se lanza una excepción `ValueError`.

        Args:
            modo_cifrado (str): Nombre del modo de cifrado, el cual está acotado por el parseo de argumentos de `script_ejecucion.py`.
            clave (str): Clave de cifrado que será utilizada por el cifrador.
            ruta (str): Ruta asociada al archivo o datos que se están cifrando o descifrando.

        Returns:
            Cifrador: Una instancia de la subclase de `Cifrador` correspondiente al `modo_cifrado`.

        Raises:
            ValueError: Si el `modo_cifrado` es desconocido o no está disponible en `lista_cifradores`.
        """
        # Iterar sobre los cifradores disponibles en la lista
        for cifrador in CifradorFactory.lista_cifradores:
            # Comparar el nombre del cifrador con el modo de cifrado proporcionado
            print(cifrador.nombre)
            if cifrador.nombre == modo_cifrado:
                return cifrador(clave, ruta)

        # Si no se encuentra un cifrador que coincida, lanzar una excepción
        else:
            raise ValueError(f"Tipo de cifrador desconocido: {modo_cifrado}")
