from pitea.cifradores.Cifrador import Cifrador
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from pitea.constantes import RUTA_DATOS_CIFRADOS_DESOCULTACION, SEMILLA


class CifradorNone(Cifrador):
    nombre = "none"


    def cifrar(self, datos):

        return b"",datos

    def descifrar(self,datos):
    
        return datos
