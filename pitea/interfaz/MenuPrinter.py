import os
from interfaz.constantes import RESET, ROJO, CYAN, YELLOW,TITULO,MENU

class MenuPrinter:
    def __init__(self):
        self.menu = MENU
    
    # Método para imprimir el menú en la terminal.
    def mostrar_menu(self):
      
        print(CYAN + self.menu + RESET)
        opcion = input(YELLOW +"Seleccione una opción:" + RESET)
        return opcion

    # Método para imprimir el encabezado o título decorado
    def mostrar_encabezado(self):
         os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla antes de mostrar el menú
         print(ROJO + TITULO + RESET)
    
    # Método para mostrar el mensaje de salida
    def mostrar_salida(self):
        print(ROJO + "Saliendo..." + RESET)