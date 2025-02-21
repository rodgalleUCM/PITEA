
from interfaz.comandos.command import Command
from interfaz.constantes import OPCIONES_CIFRADOS,OPCIONES_MODO_IMAGEN,OPCIONES_MODO_AUDIO,OPCIONES_VERBOSE,SCRIPT_PATH,RESET,YELLOW
from interfaz.utils import ejecutar_comando,comprobar_opcion,comprobar_archivo,comprobar_directorio
from interfaz.MenuPrinter import MenuPrinter

class OcultarArchivoCommand(Command):
    def __init__(self):
        super().__init__("Ocultar  archivo")

    def ejecutar(self):
        menu = MenuPrinter()
        menu. mostrar_opcion(self.descripcion)

        imagen = ""
        audio = ""

        modo_cifrado =  comprobar_opcion(f"🔒 Modo de cifrado del texto ({'/'.join(OPCIONES_CIFRADOS)}): ", OPCIONES_CIFRADOS)
        modo_imagen = comprobar_opcion(f"🖼️  Modo de ocultacion en imagen ({'/'.join(OPCIONES_MODO_IMAGEN)}): ", OPCIONES_MODO_IMAGEN)
        modo_audio =  comprobar_opcion(f"🎵 Modo de ocultacion en audio ({'/'.join(OPCIONES_MODO_AUDIO)}): ", OPCIONES_MODO_AUDIO)
        contraseña = input(YELLOW + "🔑 Contraseña: " + RESET).strip()
        archivo =   comprobar_archivo("📂 Ruta del archivo a ocultar: ")
       

        if modo_imagen == "lsb":
            imagen = comprobar_archivo("🖼️  Ruta de la imagen: ") 

        if modo_audio == "lsb":
            audio = comprobar_archivo("🎵 Ruta del audio: ")
           

        salida = comprobar_directorio("💾 Ruta del audio de salida: ")
        verbose = comprobar_opcion(f"📢 Modo verbose ({'/'.join(OPCIONES_VERBOSE)}): ", OPCIONES_VERBOSE)
        
    
        comando = [
            "python3", SCRIPT_PATH, "ocultar",
            "--modo-cifrado", modo_cifrado,
            "--modo-cifrado-imagen", modo_imagen,
            "--modo-cifrado-audio", modo_audio,
            "--contraseña", contraseña,
            "-i", archivo,
            "-o", salida
        ]

        if imagen: 
            comando.extend(["--input_imagen", imagen])
        if audio:  
            comando.extend(["--input_audio", audio])
        if verbose == "s":
            comando.extend(["-v"])
        
        ejecutar_comando(comando)