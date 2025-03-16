import subprocess
import threading
import itertools
import os
import time
from interfaz.constantes import RESET, VERDE, ROJO, MORADO, SPINNING,YELLOW
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter


archivo_completer = PathCompleter(expanduser=True)


def comprobar_directorio(mensaje):
    """
    Solicita una ruta de directorio al usuario y verifica que exista.

    Esta función mantiene un ciclo de entrada hasta que el usuario ingrese una ruta válida de directorio
    que exista en el sistema.

    Args:
        mensaje (str): Mensaje que se muestra al usuario para pedir la ruta.

    Returns:
        str: La ruta del archivo ingresada por el usuario.

    Raises:
        ValueError: Si el directorio donde se guardara el archivo ha ingresar no existe.
    """
    while True:
        salida = prompt(mensaje, completer=archivo_completer).strip()
        salida = os.path.expanduser(salida)  # Expande '~' a '/home/usuario/'
        directorio = os.path.dirname(salida)  # Extraer solo el directorio de la ruta

        if directorio == "" or os.path.exists(directorio):  
            return salida
        print(ROJO + "❌ Error: La carpeta de salida no existe. Introduce una ruta válida." + RESET)


def comprobar_opcion(mensaje, opciones):
    """
    Solicita una opción al usuario y verifica que esté en las opciones válidas.

    Esta función mantiene un ciclo de entrada hasta que el usuario ingrese una opcion valida.

    Args:
        mensaje (str): Mensaje que se muestra al usuario para pedir la opción.
        opciones (list): Lista de opciones válidas.

    Returns:
        str: Opción seleccionada por el usuario.
    
    Raises:
        ValueError: Si la opción ingresada no es válida.
    """
    while True:
        opcion = input(YELLOW + mensaje + RESET).strip().lower()
        if opcion in opciones:
            return opcion
        print(ROJO + "❌ Error: Opción inválida." + RESET)


def comprobar_archivo(mensaje):
    """
    Solicita una ruta de archivo al usuario y verifica que exista.

    Esta función mantiene un ciclo de entrada hasta que el usuario ingrese una ruta válida de archivo
    que exista en el sistema.

    Args:
        mensaje (str): Mensaje que se muestra al usuario para pedir la ruta del archivo.

    Returns:
        str: La ruta del archivo ingresada por el usuario.

    Raises:
        ValueError: Si el archivo ingresado no existe.
    """
    while True:
        archivo = prompt( mensaje , completer=archivo_completer).strip()
        if os.path.exists(archivo):
            return archivo
        print(ROJO + "❌ Error: El archivo no existe. Introduce una ruta válida." + RESET)


def spinner():
    """
    Muestra un spinner en consola para indicar que un proceso está en ejecución.

    Este spinner se actualiza en un ciclo, mostrando caracteres de animación (|, /, -, \\) mientras el
    proceso esté en ejecución.

    El spinner se detiene cuando la variable global `SPINNING` es cambiada a False.
    """
    for cursor in itertools.cycle(['|', '/', '-', '\\']):
        if not SPINNING:
            break
        print(MORADO + f"\rProcesando... {cursor}" +RESET, end="", flush=True)
        time.sleep(0.1)


def ejecutar_comando(comando):
    """
    Ejecuta un comando en el sistema y muestra el resultado.

    Esta función ejecuta el comando proporcionado, muestra un spinner mientras el comando se ejecuta y,
    al finalizar, imprime el resultado en la consola. Si ocurre un error, se maneja la excepción y
    se muestra el error al usuario.

    Args:
        comando (list): Lista que representa el comando a ejecutar.

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: Si ocurre un error durante la ejecución del comando.
    """
    global SPINNING
    SPINNING = True

    # Iniciar el spinner en un hilo separado
    hilo_spinner = threading.Thread(target=spinner)
    hilo_spinner.start()

    try:
        result = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        SPINNING = False 
        hilo_spinner.join() 

        print(VERDE + "\r🟢 Proceso de " + comando[2] + " finalizado.\n" + RESET)
        print(MORADO + "Podra encontrar el archivo en la ruta especificada.\n"+ RESET)
        print(result.stdout)
        print(result.stderr)
        input(MORADO + "Presione enter para continuar..."+ RESET)
    except subprocess.CalledProcessError as error:
        SPINNING = False
        hilo_spinner.join()
        print(ROJO +"\r❌ Error en la ejecución:\n" + RESET, error.stderr)
        input(MORADO + "Presione enter para continuar..."+ RESET)