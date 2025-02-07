import os
from interfaz.Invoker import Invoker
from interfaz.OcultarArchivoCommand import OcultarArchivoCommand
from interfaz.DesocultarArchivoCommand import DesocultarArchivoCommand
from interfaz.constantes import RESET, ROJO, CYAN, YELLOW

def mostrar_menu():
    
    menu = """╔══════════════════════════════════╗
║      🕵️‍♂️ ¿Qué desea hacer?        ║
╠══════════════════════════════════╣
║  1️⃣   Ocultar archivo             ║
║  2️⃣   Desocultar archivo          ║
║  3️⃣  🚪 Salir                     ║
╚══════════════════════════════════╝
"""
    print(CYAN + menu + RESET)
    opcion = input(YELLOW +"Seleccione una opción:" + RESET)
    return opcion

def menu():
    Inv = Invoker()
    Inv.registrar_comando("1", OcultarArchivoCommand())
    Inv.registrar_comando("2", DesocultarArchivoCommand())

    os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla antes de mostrar el menú
    print(ROJO +"""
░▒▓███████▓▒░  ░▒▓█▓▒░ ░▒▓████████▓▒░ ░▒▓████████▓▒░  ░▒▓██████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░  ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓██████▓▒░   ░▒▓████████▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓████████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
        """+ RESET)
    while True:
        opcion = mostrar_menu()   
        if opcion == "3":
            print("Saliendo...")
            break
        Inv.ejecutar_comando(opcion)
        

if __name__ == "__main__":
    menu()
