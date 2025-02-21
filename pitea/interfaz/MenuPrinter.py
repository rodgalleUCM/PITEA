import os
from interfaz.constantes import RESET, ROJO, CYAN, YELLOW,TITULO

class MenuPrinter:
    
    # Método para imprimir el menú en la terminal.
    def mostrar_menu(self, comandos):
        
        print(CYAN+ "╔══════════════════════════════════╗")
        print("║        ¿Qué desea hacer?         ║")
        print("╠══════════════════════════════════╣")            
        for key, command in comandos.items():
            print(f"║  {key}️⃣   {command.descripcion.ljust(26)}  ║")
        print("║  3️⃣   Salir                       ║")
        print("╚══════════════════════════════════╝"+ RESET)
        opcion = input(YELLOW +"Seleccione una opción:" + RESET)
        return opcion
    
    # Método para imprimir la cabecera de la opcion correspondiente
    def mostrar_opcion(self,opcion):
        print(CYAN + "╔══════════════════════════════╗")
        print(f"║      {opcion.ljust(24)}║")
        print("╚══════════════════════════════╝"+ RESET)

    # Método para mostrar el titulo de la aplicación
    def mostrar_titulo(self):
         os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla antes de mostrar el menú
         print(ROJO + TITULO + RESET)
    
    # Método para mostrar el mensaje de salida
    def mostrar_salida(self):
        print(ROJO + "Saliendo..." + RESET)