
from abc import ABC, abstractmethod

class Command(ABC):
    """
    Clase abstracta que define la estructura básica de un comando.

    Esta clase sirve como base para todos los comandos concretos. Cada comando debe
    definir una descripción y la implementación del método `ejecutar`, que es abstracto
    y debe ser implementado por las subclases.

    Atributos:
        descripcion (str): Descripción breve del comando.

    Métodos:
        ejecutar():
            Método abstracto que debe ser implementado en las subclases para definir la acción
            que ejecutará el comando.
    """
    def __init__(self,descripcion):
        """
        Inicializa un comando con su descripción.

        Args:
            descripcion (str): Descripción del comando que será utilizada para mostrar
                                información sobre lo que hace el comando.
        """
        self.descripcion = descripcion

    @abstractmethod
    def ejecutar(self):
        """
        Método abstracto que debe ser implementado por las subclases.

        Este método define la acción a ejecutar cuando el comando es invocado.

        Raises:
            NotImplementedError: Si no se implementa en una subclase concreta.
        """
        pass

    
