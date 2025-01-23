from abc import ABC, abstractmethod
from pitea.constantes import RUTA_DATOS_CIFRADO, RUTA_DATOS_LIMPIOS_DESOCULTACION


class Cifrador(ABC):
    nombre = ""

    def __init__(self, contraseña, ruta=None):
        """
        Parameters
        ----------
        archivo : str
                  contraseña del cifrado.
        """
        self.contraseña = contraseña
        self.df = None
        self.ruta = ruta

    @abstractmethod
    def cifrar(secreto, datos):
        pass

    @abstractmethod
    def descifrar():
        pass

    def cifrar_guardar(self, secreto):
        with open(secreto, "rb") as f:
            datos = f.read()

        iv, datos_cifrados = self.cifrar(datos)

        with open(RUTA_DATOS_CIFRADO, "wb") as f:
            f.write(iv + datos_cifrados)  # Escribir el IV al inicio del archivo

        print(f"Archivo cifrado guardado en {RUTA_DATOS_CIFRADO}")

    def descifrar_guardar(self):
        datos_descifrados = self.descifrar()

        # Guardar los datos descifrados en el archivo de salida
        with open(RUTA_DATOS_LIMPIOS_DESOCULTACION, "wb") as f:
            f.write(datos_descifrados)

        print(f"Archivo descifrado guardado en {RUTA_DATOS_LIMPIOS_DESOCULTACION}")

        # Guardar los datos descifrados en el archivo de salida
        with open(self.ruta, "wb") as f:
            f.write(datos_descifrados)

        print(f"Archivo descifrado guardado en {self.ruta}")
