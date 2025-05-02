from pitea.cifradores.Cifrador import Cifrador
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib


class CifradorAES(Cifrador):
    """
    Cifrador AES en modo CBC.

    Utiliza SHA-256 para derivar una clave de 16 bytes desde la contraseña,
    y genera un vector de inicialización (IV) aleatorio para cada cifrado.

    Atributos:
        nombre (str): Identificador del cifrador, "aes".
    """
    nombre = "aes"
    
    def __init__(self, contraseña, ruta=None):
        """
        Inicializa el cifrador AES con contraseña y ruta de salida opcional.

        Args:
            contraseña (str): Contraseña para derivar la clave AES.
            ruta (str, opcional): Ruta de archivo para guardar datos descifrados. Default: None.
        """
        super().__init__(contraseña,ruta)
        


    def __trasformar_contrasenia_a_clave(self):
        """
        Deriva una clave de 16 bytes desde la contraseña usando SHA-256.

        Devuelve los primeros 16 bytes del digest SHA-256 de la contraseña.
        
        Returns:
            bytes: Clave AES de 16 bytes.
        """
        contraseña_bytes = self._contraseña.encode()

        # Crear un hash SHA-256 de la contraseña
        hash_digest = hashlib.sha256(contraseña_bytes).digest()

        # Tomar los primeros 16 bytes para usar como clave
        clave = hash_digest[:16]

        return clave

    def _cifrar(self, datos):
        """
        Cifra datos en modo CBC.

        Genera IV aleatorio, aplica PKCS7 padding y cifra con AES.

        Args:
            datos (bytes): Datos originales a cifrar.

        Returns:
            tuple(bytes, bytes): Tupla (IV, datos_cifrados).
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
        Descifra datos en modo CBC.

        Extrae IV del inicio, descifra y remueve padding.

        Args:
            datos (bytes): IV concatenado con ciphertext.

        Returns:
            bytes: Datos originales descifrados.
        """
        tamano_bloque = AES.block_size

        iv = datos[:tamano_bloque]
        datos_cifrados = datos[tamano_bloque::]

        clave = self.__trasformar_contrasenia_a_clave()

        # Crear el descifrador y descifrar los datos
        descifrador = AES.new(clave, AES.MODE_CBC, iv)
        datos_descifrados = unpad(descifrador.decrypt(datos_cifrados), tamano_bloque)

        return datos_descifrados
