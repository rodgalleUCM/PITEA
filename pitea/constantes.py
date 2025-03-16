from pathlib import Path
from pitea.utils import cargar_configuracion
from datetime import datetime
from pitea.utils import actualizar_conf
from pysstv.color import MartinM1, Robot36, ScottieS1
from opciones_ocultadores import OPCIONES_OCULTACION_IMAGEN,OPCIONES_OCULTACION_AUDIO,OPCIONES_DESOCULTACION_IMAGEN,OPCIONES_DESCOCULTACION_AUDIO,OPCIONES_CIFRADO,OPCIONES_VERBOSE


RUTA_PROGRAMA = Path("pitea")

ARCHIVO_CONFIG = RUTA_PROGRAMA / "configuracion.toml"

RUTA_CACHE_GENERAL = RUTA_PROGRAMA.parent / "cache"
RUTA_CACHE_GENERAL = RUTA_CACHE_GENERAL.resolve()

conf = cargar_configuracion(ARCHIVO_CONFIG)

fecha_hora_actual = datetime.now()

formato = fecha_hora_actual.strftime("%d-%m-%Y_%H:%M")

if formato != conf['persistente']["ult_fecha"]:
    RUTA_CACHE_ESPECIFICA = RUTA_CACHE_GENERAL / f"cache_{formato}"
    conf['persistente']["ult_fecha"] = formato
    conf['persistente']["contador_cache"] = 0
else:
    RUTA_CACHE_ESPECIFICA = (
        RUTA_CACHE_GENERAL / f"cache_{formato}_{conf['persistente']['contador_cache']}"
    )
    conf['persistente']["contador_cache"] += 1


actualizar_conf(conf, ARCHIVO_CONFIG)


RUTA_OCULTACION =RUTA_CACHE_ESPECIFICA / "ocultacion"
RUTA_OCULTACION_DATOS = RUTA_OCULTACION / "datos"
RUTA_OCULTACION_IMAGEN = RUTA_OCULTACION / "imagen"
RUTA_OCULTACION_AUDIO = RUTA_OCULTACION / "audio"

RUTA_DATOS_CIFRADO = RUTA_OCULTACION_DATOS / "datos_originales_cifrados.txt"
RUTA_DATOS_OCULTADOR_IMAGEN_TEXT = RUTA_OCULTACION_DATOS / "datos_ocultador_imagen_text.txt"
RUTA_IMAGEN_CONTENEDORA = RUTA_OCULTACION_IMAGEN / "imagen_contenedora.%s"
RUTA_IMAGEN_CONTENEDORA_SIN_TRANSFORMAR= RUTA_OCULTACION_IMAGEN / "imagen_contenedora_sin_transformar.%s"

RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA = RUTA_OCULTACION_IMAGEN / "imagen_contenedora_redimensionada.%s"
RUTA_AUDIO_CONTENEDOR = RUTA_OCULTACION_AUDIO / "audio_contenedor.%s"

RUTA_DESOCULTACION =  RUTA_CACHE_ESPECIFICA / "desocultacion"
RUTA_DESOCULTACION_DATOS = RUTA_DESOCULTACION / "datos"
RUTA_DESOCULTACION_IMAGEN = RUTA_DESOCULTACION / "imagen"


RUTA_DATOS_CIFRADOS_DESOCULTACION = (
    RUTA_DESOCULTACION_DATOS / "datos_desocultos_originales_cifrados.txt"
)
RUTA_DATOS_LIMPIOS_DESOCULTACION = (
    RUTA_DESOCULTACION_DATOS / "datos_desocultos_originales_limpios.txt"
)
RUTA_IMAGEN_DESOCULTACION = (
    RUTA_DESOCULTACION_IMAGEN / "imagen_contenedora_desocultacion.%s"
)
RUTA_IMAGEN_CONTENEDORA_DESOCULTACION_DESTRANSFORMADA = (
    RUTA_DESOCULTACION_IMAGEN / "imagen_contenedora_desocultacion_destransformada.%s"
)


LISTA_DIR_CACHE_OCULTACION = [
    RUTA_OCULTACION_DATOS,
    RUTA_OCULTACION_IMAGEN,
    RUTA_OCULTACION_AUDIO,
]

LISTA_DIR_CACHE_DESOCULTACION = [RUTA_DESOCULTACION_DATOS, RUTA_DESOCULTACION_IMAGEN]


VERBOSE = False

STREAMING = False

FORMATO_IMAGEN_DESOCULTACION = "png"
FORMATO_IMAGEN_OCULTACION = "png"
FORMATO_AUDIO_OCULTACION = "wav"

# Diccionario de modos disponibles en sstv
MODES_SSTV = {
    "MartinM1": (MartinM1,(320, 256)),
    "Robot36": (Robot36,(320,240)),
    "ScottieS1": (ScottieS1,(320,256)),
}




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

OPCIONES_CIFRADOS = OPCIONES_CIFRADO
OPCIONES_MODO_IMAGEN = OPCIONES_OCULTACION_IMAGEN
OPCIONES_MODO_AUDIO = OPCIONES_OCULTACION_AUDIO
OPCIONES_MODO_IMAGEN_DESOCULTACION = OPCIONES_DESOCULTACION_IMAGEN
OPCIONES_MODO_AUDIO_DESOCULTACION= OPCIONES_DESCOCULTACION_AUDIO
OPCIONES_VERBOSE = OPCIONES_VERBOSE

def actualizar_cache():
    global RUTA_CACHE_ESPECIFICA, RUTA_OCULTACION, RUTA_OCULTACION_DATOS, RUTA_OCULTACION_IMAGEN, RUTA_OCULTACION_AUDIO
    global RUTA_DATOS_CIFRADO, RUTA_DATOS_OCULTADOR_IMAGEN_TEXT, RUTA_IMAGEN_CONTENEDORA, RUTA_IMAGEN_CONTENEDORA_SIN_TRANSFORMAR
    global RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA, RUTA_AUDIO_CONTENEDOR, RUTA_DESOCULTACION, RUTA_DESOCULTACION_DATOS
    global RUTA_DESOCULTACION_IMAGEN, RUTA_DATOS_CIFRADOS_DESOCULTACION, RUTA_DATOS_LIMPIOS_DESOCULTACION, RUTA_IMAGEN_DESOCULTACION
    global RUTA_IMAGEN_CONTENEDORA_DESOCULTACION_DESTRANSFORMADA, LISTA_DIR_CACHE_OCULTACION, LISTA_DIR_CACHE_DESOCULTACION

    # Cargar configuración
    conf = cargar_configuracion(ARCHIVO_CONFIG)

    # Obtener fecha y hora actual
    fecha_hora_actual = datetime.now()
    formato = fecha_hora_actual.strftime("%d-%m-%Y_%H:%M")

    # Verificar si la fecha actual es diferente a la última almacenada
    if formato != conf['persistente']["ult_fecha"]:
        RUTA_CACHE_ESPECIFICA = RUTA_CACHE_GENERAL / f"cache_{formato}"
        conf['persistente']["ult_fecha"] = formato
        conf['persistente']["contador_cache"] = 0
    else:
        RUTA_CACHE_ESPECIFICA = (
            RUTA_CACHE_GENERAL / f"cache_{formato}_{conf['persistente']['contador_cache']}"
        )
        conf['persistente']["contador_cache"] += 1

    # Actualizar configuración en archivo
    actualizar_conf(conf, ARCHIVO_CONFIG)

    # Actualizar las rutas de ocultación y desocultación
    RUTA_OCULTACION = RUTA_CACHE_ESPECIFICA / "ocultacion"
    RUTA_OCULTACION_DATOS = RUTA_OCULTACION / "datos"
    RUTA_OCULTACION_IMAGEN = RUTA_OCULTACION / "imagen"
    RUTA_OCULTACION_AUDIO = RUTA_OCULTACION / "audio"

    RUTA_DATOS_CIFRADO = RUTA_OCULTACION_DATOS / "datos_originales_cifrados.txt"
    RUTA_DATOS_OCULTADOR_IMAGEN_TEXT = RUTA_OCULTACION_DATOS / "datos_ocultador_imagen_text.txt"
    RUTA_IMAGEN_CONTENEDORA = RUTA_OCULTACION_IMAGEN / "imagen_contenedora.%s"
    RUTA_IMAGEN_CONTENEDORA_SIN_TRANSFORMAR = RUTA_OCULTACION_IMAGEN / "imagen_contenedora_sin_transformar.%s"
    RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA = RUTA_OCULTACION_IMAGEN / "imagen_contenedora_redimensionada.%s"
    RUTA_AUDIO_CONTENEDOR = RUTA_OCULTACION_AUDIO / "audio_contenedor.%s"

    RUTA_DESOCULTACION = RUTA_CACHE_ESPECIFICA / "desocultacion"
    RUTA_DESOCULTACION_DATOS = RUTA_DESOCULTACION / "datos"
    RUTA_DESOCULTACION_IMAGEN = RUTA_DESOCULTACION / "imagen"

    RUTA_DATOS_CIFRADOS_DESOCULTACION = (
        RUTA_DESOCULTACION_DATOS / "datos_desocultos_originales_cifrados.txt"
    )
    RUTA_DATOS_LIMPIOS_DESOCULTACION = (
        RUTA_DESOCULTACION_DATOS / "datos_desocultos_originales_limpios.txt"
    )
    RUTA_IMAGEN_DESOCULTACION = (
        RUTA_DESOCULTACION_IMAGEN / "imagen_contenedora_desocultacion.%s"
    )
    RUTA_IMAGEN_CONTENEDORA_DESOCULTACION_DESTRANSFORMADA = (
        RUTA_DESOCULTACION_IMAGEN / "imagen_contenedora_desocultacion_destransformada.%s"
    )

    LISTA_DIR_CACHE_OCULTACION = [
        RUTA_OCULTACION_DATOS,
        RUTA_OCULTACION_IMAGEN,
        RUTA_OCULTACION_AUDIO,
    ]

    LISTA_DIR_CACHE_DESOCULTACION = [RUTA_DESOCULTACION_DATOS, RUTA_DESOCULTACION_IMAGEN]


