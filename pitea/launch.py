import os
from interfaz.Invoker import Invoker
from interfaz.OcultarArchivoCommand import OcultarArchivoCommand
from interfaz.DesocultarArchivoCommand import DesocultarArchivoCommand
from interfaz.MenuPrinter import MenuPrinter


def menu():
    menu_printer = MenuPrinter()
    Inv = Invoker()
    Inv.registrar_comando("1", OcultarArchivoCommand())
    Inv.registrar_comando("2", DesocultarArchivoCommand())

  
    while True:
        menu_printer.mostrar_encabezado()
        opcion = menu_printer.mostrar_menu()   
        if opcion == "3":
            menu_printer.mostrar_salida()
            break
        Inv.ejecutar_comando(opcion)
        

if __name__ == "__main__":
    menu()
