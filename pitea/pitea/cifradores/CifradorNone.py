from pitea.cifradores.Cifrador import Cifrador


class CifradorNone(Cifrador):
    nombre = "none"


    def cifrar(self, datos):

        return b"",datos

    def descifrar(self,datos):
    
        return datos
