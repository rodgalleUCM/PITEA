import os
import subprocess
import threading
import itertools
import time

SCRIPT_PATH = "script_ejecucion.py"
SPINNING = False
RESET = "\033[0m"      # Restablecer color
CYAN = "\033[1;36m"    # Color Cian (títulos)
YELLOW = "\033[1;33m"  # Amarillo (etiquetas de entrada)
ROJO = "\033[1;31m"  # Rojo (errores)
VERDE = "\033[1;32m"  # Verde (éxito)
MORADO = "\033[1;35m"  # Morado (información)

import os

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


def spinner():
    for cursor in itertools.cycle(['|', '/', '-', '\\']):
        if not SPINNING:
            break
        print(MORADO + "\rProcesando... {cursor}" +RESET, end="", flush=True)
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

def ocultar():
    print(CYAN + "\n╔══════════════════════════════╗")
    print("║      🔒 Ocultar Archivo      ║")
    print("╚══════════════════════════════╝" + RESET)

    while True:
        modo_cifrado = input(YELLOW + "🔹 Modo de cifrado (aes): " + RESET).strip().lower() or "aes"
        if modo_cifrado in ["aes"]:
            break
        print(ROJO + "❌ Error: Modo de cifrado no válido. Debe ser 'aes'." + RESET)


    while True:
        modo_imagen = input(YELLOW + "🖼️  Modo de cifrado en imagen (lsb/text): " + RESET).strip().lower() or "lsb"
        if modo_imagen in ["lsb", "text"]:
            break
        print(ROJO + "❌ Error: Opción inválida. Debe ser 'lsb' o 'text'." + RESET)

    while True:
        modo_audio = input(YELLOW + "🎵 Modo de cifrado en audio (lsb/sstv): " + RESET).strip().lower() or "lsb"
        if modo_audio in ["lsb", "sstv"]:
            break
        print(ROJO + "❌ Error: Opción inválida. Debe ser 'lsb' o 'sstv'." + RESET)

    contraseña = input(YELLOW + "🔑 Contraseña: " + RESET).strip()

    while True:
        archivo = input(YELLOW + "📂 Ruta del archivo a ocultar: " + RESET).strip()
        if os.path.exists(archivo):
            break
        print(ROJO + "❌ Error: El archivo no existe. Introduce una ruta válida." + RESET)

    if modo_imagen == "lsb":
        while True:
            imagen = input(YELLOW + "🖼️  Ruta de la imagen: " + RESET).strip()
            if os.path.exists(imagen):
                break
            print(ROJO + "❌ Error: La imagen no existe. Introduce una ruta válida." + RESET)
        
        while True:
            audio = input(YELLOW + "🎵 Ruta del audio: " + RESET).strip()
            if os.path.exists(audio):
                break
            print(ROJO + "❌ Error: El archivo de audio no existe. Introduce una ruta válida." + RESET)
    else:
        imagen = ""
        audio = ""

    while True:
        salida = input(YELLOW + "💾 Ruta del archivo de salida: " + RESET).strip()
        directorio = os.path.dirname(salida)  # Extraer solo el directorio de la ruta

        if directorio == "" or os.path.exists(directorio):  
            break
        print(ROJO + "❌ Error: La carpeta de salida no existe. Introduce una ruta válida." + RESET)

    while True:
        verbose = input(YELLOW + "📢 Modo verbose (s/n): " + RESET).strip().lower() or "n"
        if verbose in ["s", "n"]:
            break
        print(ROJO + "❌ Error: Opción inválida. Debe ser 's' o 'n'." + RESET)
    
   
    comando = [
        "python3", SCRIPT_PATH, "ocultar",
        "--modo-cifrado", modo_cifrado,
        "--modo-cifrado-imagen", modo_imagen,
        "--modo-cifrado-audio", modo_audio,
        "--contraseña", contraseña,
        "-i", archivo,
        "-o", salida
    ]

    if imagen: # Si se especifica la imagen, se añade al comando
        comando.extend(["--input_imagen", imagen])
    if audio:  # Si se especifica el audio, se añade al comando
        comando.extend(["--input_audio", audio])
    if verbose == "s":
        comando.extend(["-v"])
    
    ejecutar_comando(comando)

def desocultar():
    print(CYAN + "\n╔══════════════════════════════╗")
    print("║     🔓 Desocultar Archivo    ║")
    print("╚══════════════════════════════╝" + RESET)

    while True:
        modo_cifrado = input(YELLOW + "🔹 Modo de cifrado (aes): " + RESET).strip().lower() or "aes"
        if modo_cifrado in ["aes"]:
            break
        print(ROJO + "❌ Error: Modo de cifrado no válido. Debe ser 'aes'." + RESET)

   
    while True:
        modo_imagen = input(YELLOW + "🖼️  Modo de cifrado en imagen (lsb/text/sstv): " + RESET).strip().lower() or "lsb"
        if modo_imagen in ["lsb", "text", "sstv"]:
            break
        print(ROJO + "❌ Error: Opción inválida. Debe ser 'lsb', 'text' o 'sstv'." + RESET)

    
    while True:
        modo_audio = input(YELLOW + "🎵 Modo de cifrado en audio (lsb/sstv): " + RESET).strip().lower() or "lsb"
        if modo_audio in ["lsb", "sstv"]:
            break
        print(ROJO + "❌ Error: Opción inválida. Debe ser 'lsb' o 'sstv'." + RESET)

    
    contraseña = input(YELLOW + "🔑 Contraseña: " + RESET).strip()

    
    if modo_audio == "sstv":
        input_audio = ""
        while True:
            input_imagen = input(YELLOW + "🖼️  Ruta de la imagen de entrada: " + RESET).strip()
            if os.path.exists(input_imagen):
                break
            print(ROJO + "❌ Error: La imagen no existe. Introduce una ruta válida." + RESET)
    else:
        input_imagen = ""
        while True:
            input_audio = input(YELLOW + "🎵 Ruta del audio de entrada: " + RESET).strip()
            if os.path.exists(input_audio):
                break
            print(ROJO + "❌ Error: El archivo de audio no existe. Introduce una ruta válida." + RESET)


    while True:
        salida = input(YELLOW + "💾 Ruta del archivo de salida: " + RESET).strip()
        directorio = os.path.dirname(salida)  # Extraer solo el directorio de la ruta

        if directorio == "" or os.path.exists(directorio):  
            break
        print(ROJO + "❌ Error: La carpeta de salida no existe. Introduce una ruta válida." + RESET)

    
    while True:
        verbose = input(YELLOW + "📢 Modo verbose (s/n): " + RESET).strip().lower() or "n"
        if verbose in ["s", "n"]:
            break
        print(ROJO + "❌ Error: Opción inválida. Debe ser 's' o 'n'." + RESET)


    comando = [
        "python3", SCRIPT_PATH, "desocultar",
        "--modo-cifrado", modo_cifrado,
        "--modo-cifrado-imagen", modo_imagen,
        "--modo-cifrado-audio", modo_audio,
        "--contraseña", contraseña,
        "-o", salida
    ]

    if input_audio:
        comando.extend(["--input_audio", input_audio])
    if input_imagen:
        comando.extend(["--input_imagen", input_imagen])
    if verbose == "s":
        comando.extend(["-v"])
    
    ejecutar_comando(comando)

def menu():
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
        
        if opcion == "1":
            ocultar()
        elif opcion == "2":
            desocultar()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print(ROJO + "Opción no válida. Intente de nuevo." + RESET)

if __name__ == "__main__":
    menu()
