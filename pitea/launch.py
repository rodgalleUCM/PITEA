import os
from interfaz.Invoker import Invoker
from interfaz.comandos.OcultarArchivoCommand import OcultarArchivoCommand
from interfaz.comandos.DesocultarArchivoCommand import DesocultarArchivoCommand
from interfaz.MenuPrinter import MenuPrinter


def menu():
    menu_printer = MenuPrinter()
    inv = Invoker()

    # Registro automático de comandos
    comandos = [OcultarArchivoCommand(), DesocultarArchivoCommand()]
    for idx, comando in enumerate(comandos, start=1):
        inv.registrar_comando(str(idx), comando)

  
    while True:
        menu_printer.mostrar_encabezado()
        opcion = menu_printer.mostrar_menu(inv.obtener_comandos())   
        if opcion == str(idx+1) :
            menu_printer.mostrar_salida()
            break
        inv.ejecutar_comando(opcion)
        

if __name__ == "__main__":
    menu()
