from pitea.cifradores.CifradorAES import CifradorAES
from pitea.AbstractFactory import AbstractFactory
from pitea.cifradores.CifradorNone import CifradorNone


class CifradorFactory(AbstractFactory):
    """
    Fábrica concreta que devuelve instancias de `Cifrador` según el modo.

    Atributos:
        lista_cifradores (list): Clases derivadas de `Cifrador` disponibles.
    """

    lista_cifradores = [CifradorAES, CifradorNone]

    @staticmethod
    def creacion(modo_cifrado, clave, ruta = None):
        """
        Crea y retorna una instancia del cifrador especificado.

        Args:
            modo_cifrado (str): Identificador del cifrador ('aes', 'none', etc.).
            clave (str): Contraseña o clave para el cifrador.
            ruta (str, opcional): Ruta de salida para datos cifrados o descifrados.

        Returns:
            Cifrador: Instancia de la subclase de `Cifrador` correspondiente.

        Raises:
            ValueError: Si `modo_cifrado` no coincide con ninguna clase en `lista_cifradores`.
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
