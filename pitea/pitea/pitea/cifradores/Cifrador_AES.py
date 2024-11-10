from pitea.cifradores.Cifrador import Cifrador
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from pitea.constantes import RUTA_DATOS_CIFRADO, SEMILLA
from pitea.mensajes import print

class Cifrador_AES(Cifrador):

    def trasformar_contrasenia_a_clave(self) :
        contraseña_bytes = self.contraseña.encode()
        # Rellenar o truncar la contraseña a 16 bytes
        if len(contraseña_bytes) < 16:
            contraseña_bytes += b'\x00' * (16 - len(contraseña_bytes))  # Rellenar con 0s
        else:
            contraseña_bytes = contraseña_bytes[:16]  # Tomar los primeros 16 bytes

        # Mezclar la contraseña con la semilla para crear la clave
        clave = bytes(a ^ b for a, b in zip(contraseña_bytes, SEMILLA))  # XOR para mezclar

        return clave


    def cifrar(self, secreto):
        tamano_bloque = AES.block_size

        with open(secreto, 'rb') as f:
            datos = f.read()

        clave = self.trasformar_contrasenia_a_clave()

        datos_padded = pad(datos, tamano_bloque)  # Asegurarse de que los datos tengan un tamaño múltiplo del tamaño del bloque
        iv = get_random_bytes(tamano_bloque)  # Generar un vector de inicialización aleatorio
        cifrador = AES.new(clave, AES.MODE_CBC, iv)  # Crear el cifrador
        datos_cifrados = cifrador.encrypt(datos_padded)  # Cifrar los datos
        
        # Guardar el IV y los datos cifrados en el archivo de salida
        with open(RUTA_DATOS_CIFRADO, 'wb') as f:  
            f.write(iv + datos_cifrados)  # Escribir el IV al inicio del archivo
        
        print(f'Archivo cifrado guardado en {RUTA_DATOS_CIFRADO}')
        return iv + datos_cifrados

    def descifrar(self):
        # TODO: Implementar la función de descifrado
        pass

    