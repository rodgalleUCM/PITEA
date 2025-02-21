
from interfaz.comandos.command import Command
from interfaz.constantes import OPCIONES_MODO_IMAGEN_DESOCULTACION,OPCIONES_CIFRADOS,OPCIONES_MODO_AUDIO_DESOCULTACION,YELLOW,RESET,SCRIPT_PATH,OPCIONES_VERBOSE
from interfaz.utils import ejecutar_comando,comprobar_opcion,comprobar_archivo,comprobar_directorio
from interfaz.MenuPrinter import MenuPrinter


class DesocultarArchivoCommand(Command):

    def __init__(self):
        super().__init__("Desocultar  archivo")

    def ejecutar(self):
        menu = MenuPrinter()
        menu. mostrar_opcion(self.descripcion)

        #Se recogen los datos si son necesarios
        input_audio = ""
        input_imagen = ""
        input_text = ""
        
        modo_imagen = comprobar_opcion(f"🖼️  Modo de ocultacion usado en la imagen ({'/'.join(OPCIONES_MODO_IMAGEN_DESOCULTACION)}): ", OPCIONES_MODO_IMAGEN_DESOCULTACION)
        modo_cifrado = comprobar_opcion(f"🔒 Modo de cifrado usado en el texto ({'/'.join(OPCIONES_CIFRADOS)}): ", OPCIONES_CIFRADOS)
        modo_audio =  comprobar_opcion(f"🎵 Modo de ocultacion usado en el audio ({'/'.join(OPCIONES_MODO_AUDIO_DESOCULTACION)}): ", OPCIONES_MODO_AUDIO_DESOCULTACION)
        contraseña = input(YELLOW + "🔑 Contraseña: " + RESET).strip()

        if modo_audio == "none" and modo_imagen == "none":
            input_text = comprobar_archivo("📄 Ruta del archivo de texto: ") 
        else:
            if modo_audio == "sstv":
                #Usar o un audio o una imagen
                while True:
                    opcion = input(YELLOW + "🔊 ¿Desea usar un audio o una imagen? (audio/imagen): " + RESET).strip().lower()
                    if opcion == "audio":
                        input_audio = comprobar_archivo("🎵 Ruta del audio: ")
                        break
                    elif opcion == "imagen":
                        input_imagen = comprobar_archivo("🖼️ Ruta de la imagen: ")
                        break
                    else:
                        print("Opción inválida.")
            else:
                input_audio = comprobar_archivo("🎵 Ruta del audio: ")

    

        salida = comprobar_directorio("💾 Ruta del archivo de salida: ")
        verbose = comprobar_opcion(f"📢 Modo verbose ({'/'.join(OPCIONES_VERBOSE)}): ", OPCIONES_VERBOSE)

        comando = [
            "python3", SCRIPT_PATH, "desocultar",
            "--modo-cifrado", modo_cifrado,
            "--modo-cifrado-imagen", modo_imagen,
            "--modo-cifrado-audio", modo_audio,
            "--contraseña", contraseña,
            "-o", salida
        ]

        if input_text:
            comando.extend(["--input_text", input_text])
        if input_audio:
            comando.extend(["--input_audio", input_audio])
        if input_imagen:
            comando.extend(["--input_imagen", input_imagen])
        if verbose == "s":
            comando.extend(["-v"])
        
        
        ejecutar_comando(comando)