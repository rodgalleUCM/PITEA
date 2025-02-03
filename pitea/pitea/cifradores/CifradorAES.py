from pitea.cifradores.Cifrador import Cifrador
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from pitea.constantes import RUTA_DATOS_CIFRADOS_DESOCULTACION, SEMILLA


class CifradorAES(Cifrador):
    nombre = "aes"

    def trasformar_contrasenia_a_clave(self):
        contraseña_bytes = self.contraseña.encode()
        # Rellenar o truncar la contraseña a 16 bytes
        if len(contraseña_bytes) < 16:
            contraseña_bytes += b"\x00" * (
                16 - len(contraseña_bytes)
            )  # Rellenar con 0s
        else:
            contraseña_bytes = contraseña_bytes[:16]  # Tomar los primeros 16 bytes

        # Mezclar la contraseña con la semilla para crear la clave
        clave = bytes(
            a ^ b for a, b in zip(contraseña_bytes, SEMILLA)
        )  # XOR para mezclar

        return clave

    def cifrar(self, datos):
        tamano_bloque = AES.block_size

        clave = self.trasformar_contrasenia_a_clave()

        datos_padded = pad(
            datos, tamano_bloque
        )  # Asegurarse de que los datos tengan un tamaño múltiplo del tamaño del bloque
        iv = get_random_bytes(
            tamano_bloque
        )  # Generar un vector de inicialización aleatorio
        cifrador = AES.new(clave, AES.MODE_CBC, iv)  # Crear el cifrador
        datos_cifrados = cifrador.encrypt(datos_padded)  # Cifrar los datos

        return iv, datos_cifrados

    def descifrar(self,datos):
        tamano_bloque = AES.block_size

        iv =datos[:tamano_bloque]
        datos_cifrados = datos[tamano_bloque::]

        clave = self.trasformar_contrasenia_a_clave()

        # Crear el descifrador y descifrar los datos
        descifrador = AES.new(clave, AES.MODE_CBC, iv)
        datos_descifrados = unpad(descifrador.decrypt(datos_cifrados), tamano_bloque)


        return datos_descifrados
