from opciones_ocultadores import *

SCRIPT_PATH = "script_ejecucion.py"
SPINNING = False
RESET = "\033[0m"      # Restablecer color
CYAN = "\033[1;36m"    # Color Cian (títulos)
YELLOW = "\033[1;33m"  # Amarillo (etiquetas de entrada)
ROJO = "\033[1;31m"  # Rojo (errores)
VERDE = "\033[1;32m"  # Verde (éxito)
MORADO = "\033[1;35m"  # Morado (información)
TITULO = """
░▒▓███████▓▒░  ░▒▓█▓▒░ ░▒▓████████▓▒░ ░▒▓████████▓▒░  ░▒▓██████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░  ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓██████▓▒░   ░▒▓████████▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓████████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
        """

OPCIONES_CIFRADOS = ["aes", "none"]
OPCIONES_MODO_IMAGEN = OPCIONES_OCULTACION_IMAGEN
OPCIONES_MODO_AUDIO = OPCIONES_OCULTACION_AUDIO
OPCIONES_MODO_IMAGEN_DESOCULTACION = OPCIONES_DESOCULTACION_IMAGEN
OPCIONES_MODO_AUDIO_DESOCULTACION= OPCIONES_DESCOCULTACION_AUDIO
OPCIONES_VERBOSE = ["s", "n"]