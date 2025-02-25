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

    def trasformar_contrasenia_a_clave(self):
        """
        Transforma la contraseña en una clave de 16 bytes utilizando una semilla y el operador XOR.

        La contraseña proporcionada se convierte en una clave de 16 bytes. Si la contraseña es más corta,
        se rellena con ceros. Si es más larga, se trunca a 16 bytes.

        Luego, la clave se mezcla con una semilla definida (SEMILLA) mediante el operador XOR para
        generar la clave final.

        Returns:
            bytes: La clave de 16 bytes resultante después de mezclar la contraseña con la semilla.
        """
        contraseña_bytes = self.contraseña.encode()

        # Crear un hash SHA-256 de la contraseña
        hash_object = hashlib.sha256(contraseña_bytes)
        hash_digest = hash_object.digest()

        # Tomar los primeros 16 bytes para usar como clave
        clave = hash_digest[:16]

        return clave

    def cifrar(self, datos):
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

        clave = self.trasformar_contrasenia_a_clave()

        datos_padded = pad(datos, tamano_bloque)  # Asegurarse de que los datos tengan un tamaño múltiplo del tamaño del bloque
        iv = get_random_bytes(tamano_bloque)  # Generar un vector de inicialización aleatorio
        cifrador = AES.new(clave, AES.MODE_CBC, iv)  # Crear el cifrador
        datos_cifrados = cifrador.encrypt(datos_padded)  # Cifrar los datos

        return iv, datos_cifrados

    def descifrar(self, datos):
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

        clave = self.trasformar_contrasenia_a_clave()

        # Crear el descifrador y descifrar los datos
        descifrador = AES.new(clave, AES.MODE_CBC, iv)
        datos_descifrados = unpad(descifrador.decrypt(datos_cifrados), tamano_bloque)

        return datos_descifrados
