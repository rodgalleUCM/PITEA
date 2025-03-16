
from interfaz.comandos.command import Command
from interfaz.constantes import OPCIONES_CIFRADOS,OPCIONES_MODO_IMAGEN,OPCIONES_MODO_AUDIO,OPCIONES_VERBOSE,SCRIPT_PATH,RESET,YELLOW,ROJO
from interfaz.utils import ejecutar_comando,comprobar_opcion,comprobar_archivo,comprobar_directorio
from interfaz.MenuPrinter import MenuPrinter
from getpass import getpass

class OcultarArchivoCommand(Command):
    """
    Comando para ocultar un archivo en otros archivos (imagen o audio).

    Este comando solicita al usuario información sobre los métodos ha utilizar para ocultar
    los datos (modo de ocultación de imagen y audio, y modo de cifrado), las rutas de los
    archivos a ocultar y la contraseña para cifrar el contenido.

    Atributos:
        descripcion (str): Descripción del comando. En este caso, "Ocultar archivo".
    
    Métodos:
        ejecutar():
            Ejecuta el comando, recopilando los datos del usuario y ejecutando el proceso
            de ocultación del archivo.
    """
    def __init__(self):
        """
        Inicializa el comando con una descripción de "Ocultar archivo".
        Llama al constructor de la clase base `Command` con la descripción.
        """
        super().__init__("Ocultar  archivo")

    def ejecutar(self):
        """
        Ejecuta el comando de ocultación, solicitando al usuario la información necesaria
        para el proceso (modo de ocultación, modo de cifrado, rutas de archivos y contraseña).
        Después construye y ejecuta el comando correspondiente utilizando la función `ejecutar_comando`.

        El proceso incluye:
            - Solicitar al usuario el modo de cifrado y los modos de ocultación en imagen y audio.
            - Solicitar al usuario la contraseña para cifrar los datos.
            - Verificar si se necesitan imágenes o audios para la ocultación de datos.
            - Construir el comando para ejecutar el proceso de ocultación.
            - Ejecutar el comando utilizando `ejecutar_comando`.
        """
        menu = MenuPrinter()
        menu. mostrar_opcion(self.descripcion)

        imagen = ""
        audio = ""

        # Solicitar modos de cifrado y ocultación
        modo_cifrado =  comprobar_opcion(f"🔒 Modo de cifrado del texto ({'/'.join(OPCIONES_CIFRADOS)}): ", OPCIONES_CIFRADOS)
        modo_imagen = comprobar_opcion(f"🖼️  Modo de ocultacion en imagen ({'/'.join(OPCIONES_MODO_IMAGEN)}): ", OPCIONES_MODO_IMAGEN)
        modo_audio =  comprobar_opcion(f"🎵 Modo de ocultacion en audio ({'/'.join(OPCIONES_MODO_AUDIO)}): ", OPCIONES_MODO_AUDIO)
        while True :
            contraseña = getpass(YELLOW + "🔑 Contraseña: " + RESET).strip()
            contraseña_conf = getpass(YELLOW + "🔑 Introduzca de nuevo al contraseña: " + RESET).strip()
            if contraseña == contraseña_conf : break
            else : print(ROJO +"Las contraseñas introducidad no coinciden"+RESET)

        archivo =   comprobar_archivo("📂 Ruta del archivo a ocultar: ")
       
         # Si el modo de imagen es 'lsb', se solicita una imagen
        if modo_imagen == "lsb":
            imagen = comprobar_archivo("🖼️  Ruta de la imagen: ") 

        # Si el modo de audio es 'lsb', se solicita un archivo de audi
        if modo_audio == "lsb":
            audio = comprobar_archivo("🎵 Ruta del audio: ")
           
        # Solicitar la ruta de salida y el modo verbose
        salida = comprobar_directorio("💾 Ruta del audio de salida: ")
        verbose = comprobar_opcion(f"📢 Modo verbose ({'/'.join(OPCIONES_VERBOSE)}): ", OPCIONES_VERBOSE)
        
        # Construir el comando
        comando = [
            "python3", SCRIPT_PATH, "ocultar",
            "--modo-cifrado", modo_cifrado,
            "--modo-cifrado-imagen", modo_imagen,
            "--modo-cifrado-audio", modo_audio,
            "--contraseña", contraseña,
            "-i", archivo,
            "-o", salida
        ]

        # Añadir parámetros de imagen, audio y verbose según lo seleccionado
        if imagen: 
            comando.extend(["--input_imagen", imagen])
        if audio:  
            comando.extend(["--input_audio", audio])
        if verbose == "s":
            comando.extend(["-v"])
        
        # Ejecutar el comando
        ejecutar_comando(comando)