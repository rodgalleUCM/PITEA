import subprocess
import threading
import itertools
import os
import time
from interfaz.constantes import RESET, VERDE, ROJO, MORADO, SPINNING,YELLOW
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.styles import Style

# Autocompletador de rutas
archivo_completer = PathCompleter(expanduser=True)

def comprobar_directorio(mensaje):
    while True:
        salida = prompt(mensaje, completer=archivo_completer).strip()
        directorio = os.path.dirname(salida)  # Extraer solo el directorio de la ruta

        if directorio == "" or os.path.exists(directorio):  
            return salida
        print(ROJO + "❌ Error: La carpeta de salida no existe. Introduce una ruta válida." + RESET)

def comprobar_opcion(mensaje, opciones):
    while True:
        opcion = input(YELLOW + mensaje + RESET).strip().lower()
        if opcion in opciones:
            return opcion
        print(ROJO + "❌ Error: Opción inválida." + RESET)

def comprobar_archivo(mensaje):
    while True:
        archivo = prompt( mensaje , completer=archivo_completer).strip()
        if os.path.exists(archivo):
            return archivo
        print(ROJO + "❌ Error: El archivo no existe. Introduce una ruta válida." + RESET)

def spinner():
    for cursor in itertools.cycle(['|', '/', '-', '\\']):
        if not SPINNING:
            break
        print(MORADO + f"\rProcesando... {cursor}" +RESET, end="", flush=True)
        time.sleep(0.1)

def ejecutar_comando(comando):
    global SPINNING
    SPINNING = True

    # Iniciar el spinner en un hilo separado
    hilo_spinner = threading.Thread(target=spinner)
    hilo_spinner.start()

    try:
        result = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        SPINNING = False  # Detener el spinner
        hilo_spinner.join()  # Esperar a que termine el hilo

        print(VERDE + "\r🟢 Proceso de " + comando[2] + " finalizado.\n" + RESET)
        print(MORADO + "Podra encontrar el archivo en la ruta especificada.\n"+ RESET)
        print(result.stdout)
        input(MORADO + "Presione enter para continuar..."+ RESET)
    except subprocess.CalledProcessError as error:
        SPINNING = False
        hilo_spinner.join()
        print(ROJO +"\r❌ Error en la ejecución:\n" + RESET, error.stderr)
        input(MORADO + "Presione enter para continuar..."+ RESET)