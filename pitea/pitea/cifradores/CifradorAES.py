from pitea.cifradores.Cifrador import Cifrador
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib


class CifradorAES(Cifrador):
    """
    Cifrador AES que utiliza el algoritmo de cifrado simétrico AES en modo CBC.
    
    Esta clase cifra y descifra datos utilizando una contraseña que se transforma en una clave
    de 16 bytes, y un vector de inicialización (IV) aleatorio para garantizar la seguridad.
    
    Atributos:
        nombre (str): El nombre del cifrador, en este caso "aes".
    """
    nombre = "aes"
    
    def __init__(self, contraseña, ruta=None):
        """
        Inicializa el cifrador con la contraseña y una ruta opcional.

        Args:
            contraseña (str): Contraseña del cifrado.
            ruta (str, opcional): Ruta del archivo donde se guardan los datos. (default es None)
        """
        super().__init__(contraseña,ruta)
        


    def __trasformar_contrasenia_a_clave(self):
        """
        Transforma la contraseña en una clave de 16 bytes utilizando sha256.


        Returns:
            bytes: La clave de 16 bytes resultante después de pasar por sha256 y ser truncada.
        """
        contraseña_bytes = self._contraseña.encode()

        # Crear un hash SHA-256 de la contraseña
        hash_digest = hashlib.sha256(contraseña_bytes).digest()

        # Tomar los primeros 16 bytes para usar como clave
        clave = hash_digest[:16]

        return clave

    def _cifrar(self, datos):
        """
        Cifra los datos utilizando el algoritmo AES en modo CBC.

        Este método utiliza una clave generada a partir de la contraseña, un vector de inicialización
        aleatorio y relleno de datos para garantizar que los datos sean múltiplos del tamaño de bloque.

        Args:
            datos (bytes): Los datos a cifrar.

        Returns:
            tuple: Un tuple que contiene el IV y los datos cifrados.
        """
        tamano_bloque = AES.block_size

        clave = self.__trasformar_contrasenia_a_clave()

        datos_padded = pad(datos, tamano_bloque)  # Asegurarse de que los datos tengan un tamaño múltiplo del tamaño del bloque
        iv = get_random_bytes(tamano_bloque)  # Generar un vector de inicialización aleatorio
        cifrador = AES.new(clave, AES.MODE_CBC, iv)  # Crear el cifrador
        datos_cifrados = cifrador.encrypt(datos_padded)  # Cifrar los datos

        return iv, datos_cifrados

    def _descifrar(self, datos):
        """
        Descifra los datos utilizando el algoritmo AES en modo CBC.

        Este método toma los datos cifrados y un IV (vector de inicialización) del principio del bloque de datos,
        luego los descifra utilizando la misma clave generada a partir de la contraseña.

        Args:
            datos (bytes): Los datos cifrados, incluyendo el IV al principio.

        Returns:
            bytes: Los datos descifrados y despaddeados.
        """
        tamano_bloque = AES.block_size

        iv = datos[:tamano_bloque]
        datos_cifrados = datos[tamano_bloque::]

        clave = self.__trasformar_contrasenia_a_clave()

        # Crear el descifrador y descifrar los datos
        descifrador = AES.new(clave, AES.MODE_CBC, iv)
        datos_descifrados = unpad(descifrador.decrypt(datos_cifrados), tamano_bloque)

        return datos_descifrados
