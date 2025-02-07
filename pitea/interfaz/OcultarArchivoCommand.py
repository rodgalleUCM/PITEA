
import os
from interfaz.command import Command
from interfaz.constantes import RESET, ROJO, CYAN, YELLOW, SCRIPT_PATH
from interfaz.utils import ejecutar_comando

class OcultarArchivoCommand(Command):
    def ejecutar(self):
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