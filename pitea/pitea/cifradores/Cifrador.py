from abc import ABC, abstractmethod
from constantes import constantes
from pitea.mensajes import print


class Cifrador(ABC):
    """
    Clase abstracta que define la interfaz para cifrado y descifrado de datos.

    Subclases deben implementar los métodos `_cifrar` y `_descifrar` usando algoritmos específicos.

    Atributos:
        nombre (str): Identificador legible del tipo de cifrador.
        _contraseña (str): Contraseña usada para el proceso de cifrado/descifrado.
        _ruta (str or None): Ruta de archivo de salida para datos resultantes.
    """

    nombre = ""

    def __init__(self, contraseña, ruta=None):
        """
        Inicializa el cifrador con credenciales y ruta de destino.

        Args:
            contraseña (str): Contraseña para cifrado/descifrado.
            ruta (str, opcional): Ruta al archivo donde escribir datos finales.
        """
        
        self._contraseña = contraseña
        self._ruta = ruta


    @abstractmethod
    def _cifrar(self, datos):
        """
        Cifra bytes de entrada y retorna IV y ciphertext.

        Args:
            datos (bytes): Datos sin cifrar.

        Returns:
            tuple(bytes, bytes): IV (vector de inicialización) y datos cifrados.
        """
        pass

    @abstractmethod
    def _descifrar(self, datos):
        """
        Descifra bytes de entrada y retorna datos originales.

        Args:
            datos (bytes): Datos cifrados (incluyendo IV si aplica).

        Returns:
            bytes: Datos ya descifrados.
        """
        pass

    def cifrar_guardar(self, secreto):
        """
        Lee un archivo, cifra su contenido y guarda el resultado en caché.

        Args:
            secreto (str): Ruta al archivo con datos a cifrar.
        """
        with open(secreto, "rb") as f:
            datos = f.read()

        iv, datos_cifrados = self._cifrar(datos)

        with open(constantes.RUTA_DATOS_CIFRADO, "wb") as f:
            f.write(iv + datos_cifrados)  # Escribir el IV al inicio del archivo

        print(f"Archivo cifrado guardado en {constantes.RUTA_DATOS_CIFRADO}")

    def descifrar_guardar(self):
        """
        Lee datos cifrados de cache, descifra y guarda resultados.

        Lee de `constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION`, descifra
        y escribe en dos ubicaciones: la cache limpia y la ruta final.

        Raises:
            ValueError: Si la operación de descifrado falla.
        """
        with open(constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION, "rb") as f:
            datos = f.read()

        datos_descifrados = self._descifrar(datos)

        # Guardar los datos descifrados en el archivo de salida
        with open(constantes.RUTA_DATOS_LIMPIOS_DESOCULTACION, "wb") as f:
            f.write(datos_descifrados)

        print(f"Archivo descifrado guardado en {constantes.RUTA_DATOS_LIMPIOS_DESOCULTACION}")

        # Guardar los datos descifrados en el archivo de salida
        with open(self._ruta, "wb") as f:
            f.write(datos_descifrados)

        print(f"Archivo descifrado guardado en {self._ruta}")
