
from interfaz.comandos.command import Command
from interfaz.constantes import OPCIONES_MODO_IMAGEN_DESOCULTACION,OPCIONES_CIFRADOS,OPCIONES_MODO_AUDIO_DESOCULTACION,YELLOW,RESET,SCRIPT_PATH,OPCIONES_VERBOSE
from interfaz.utils import ejecutar_comando,comprobar_opcion,comprobar_archivo,comprobar_directorio
from interfaz.MenuPrinter import MenuPrinter


class DesocultarArchivoCommand(Command):
    """
    Comando para desocultar un archivo de texto, imagen o audio oculto en otro archivo.

    Este comando solicita al usuario información sobre los métodos utilizados para ocultar
    los datos (modo de ocultación de imagen y audio, y modo de cifrado), y las rutas de los
    archivos que se van a desocultar, así como la contraseña para desencriptar el contenido.

    Atributos:
        descripcion (str): Descripción del comando. En este caso, "Desocultar archivo".
    
    Métodos:
        ejecutar():
            Ejecuta el comando, recopilando los datos del usuario y ejecutando el proceso
            de desocultación del archivo.
    """
    def __init__(self):
        """
        Inicializa el comando con una descripción de "Desocultar archivo".
        Llama al constructor de la clase base `Command` con la descripción.
        """
        super().__init__("Desocultar  archivo")

    def ejecutar(self):
        """
        Ejecuta el comando de desocultación, solicitando al usuario la información necesaria
        para el proceso (modo de ocultación, modo de cifrado, rutas de archivos y contraseña).
        Después construye y ejecuta el comando correspondiente utilizando la función `ejecutar_comando`.

        El proceso incluye:
            - Solicitar al usuario el modo de ocultación utilizado en la imagen y audio.
            - Solicitar al usuario la contraseña para descifrar los datos.
            - Verificar si se necesita un archivo de texto, imagen o audio para la desocultación.
            - Construir el comando para ejecutar el proceso de desocultación.
            - Ejecutar el comando utilizando `ejecutar_comando`.
        """
        menu = MenuPrinter()
        menu. mostrar_opcion(self.descripcion)

        #Se recogen los datos si son necesarios
        input_audio = ""
        input_imagen = ""
        input_text = ""
        
         # Solicitar modos de ocultación y cifrado
        modo_imagen = comprobar_opcion(f"🖼️  Modo de ocultacion usado en la imagen ({'/'.join(OPCIONES_MODO_IMAGEN_DESOCULTACION)}): ", OPCIONES_MODO_IMAGEN_DESOCULTACION)
        modo_cifrado = comprobar_opcion(f"🔒 Modo de cifrado usado en el texto ({'/'.join(OPCIONES_CIFRADOS)}): ", OPCIONES_CIFRADOS)
        modo_audio =  comprobar_opcion(f"🎵 Modo de ocultacion usado en el audio ({'/'.join(OPCIONES_MODO_AUDIO_DESOCULTACION)}): ", OPCIONES_MODO_AUDIO_DESOCULTACION)
        contraseña = input(YELLOW + "🔑 Contraseña: " + RESET).strip()

    
        # Validar si es necesario usar texto, imagen o audio para la desocultación
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

    
        # Solicitar la ruta de salida y el modo verbose
        salida = comprobar_directorio("💾 Ruta del archivo de salida: ")
        verbose = comprobar_opcion(f"📢 Modo verbose ({'/'.join(OPCIONES_VERBOSE)}): ", OPCIONES_VERBOSE)

        # Construir el comando
        comando = [
            "python3", SCRIPT_PATH, "desocultar",
            "--modo-cifrado", modo_cifrado,
            "--modo-cifrado-imagen", modo_imagen,
            "--modo-cifrado-audio", modo_audio,
            "--contraseña", contraseña,
            "-o", salida
        ]

        # Añadir los parámetros de entrada según lo que se haya seleccionado
        if input_text:
            comando.extend(["--input_text", input_text])
        if input_audio:
            comando.extend(["--input_audio", input_audio])
        if input_imagen:
            comando.extend(["--input_imagen", input_imagen])
        if verbose == "s":
            comando.extend(["-v"])
        
        # Ejecutar el comando
        ejecutar_comando(comando)