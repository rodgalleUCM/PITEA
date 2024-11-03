from abc import ABC, abstractmethod
class Cifrador(ABC) :
       
    def __init__(self,contraseña):
        """
        Parameters
        ----------
        archivo : str
                  contraseña del cifrado.
        """
        self.contraseña = contraseña
        self.df = None

    @abstractmethod
    def cifrar(secreto) :
        pass
    @abstractmethod
    def descifrar() :
        pass