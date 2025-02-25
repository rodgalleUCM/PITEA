import os
from interfaz.constantes import RESET, ROJO, CYAN, YELLOW,TITULO

class MenuPrinter:
    """
    Clase encargada de imprimir el menú y las opciones de la aplicación en la terminal.

    Métodos:
        mostrar_menu(comandos):
            Muestra el menú con las opciones disponibles.
        
        mostrar_opcion(opcion):
            Muestra la cabecera de la opción seleccionada.

        mostrar_titulo():
            Muestra el título de la aplicación, limpiando la pantalla antes.

        mostrar_salida():
            Muestra el mensaje de salida al cerrar la aplicación.
    """
    
   
    def mostrar_menu(self, comandos):
        """
        Muestra el menú con las opciones disponibles.

        Args:
            comandos (dict): Diccionario con las opciones del menú, donde la clave es el número y el valor es el comando con su descripción.

        Returns:
            str: Opción seleccionada por el usuario.
        """
        print(CYAN+ "╔══════════════════════════════════╗")
        print("║        ¿Qué desea hacer?         ║")
        print("╠══════════════════════════════════╣")            
        for key, command in comandos.items():
            print(f"║  {key}️⃣   {command.descripcion.ljust(26)}  ║")
        print(f"║  {int(key) + 1}️⃣   Salir                       ║")
        print("╚══════════════════════════════════╝"+ RESET)
        opcion = input(YELLOW +"Seleccione una opción:" + RESET)
        return opcion
    
  
    def mostrar_opcion(self,opcion):
        """
        Muestra la cabecera de la opción seleccionada.

        Args:
            opcion (str): Nombre de la opción seleccionada.
        """
        print(CYAN + "╔══════════════════════════════╗")
        print(f"║      {opcion.ljust(24)}║")
        print("╚══════════════════════════════╝"+ RESET)

    
    def mostrar_titulo(self):
        """
        Muestra el título de la aplicación, limpiando la pantalla antes.
        """
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla antes de mostrar el menú
        print(ROJO + TITULO + RESET)
    
    
    def mostrar_salida(self):
        """
        Muestra el mensaje de salida al cerrar la aplicación.
        """
        print(ROJO + "Saliendo..." + RESET)