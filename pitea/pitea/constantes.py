from pathlib import Path
from pitea.utils import cargar_configuracion
from datetime import datetime
from pitea.utils import actualizar_conf
from pysstv.color import MartinM1, Robot36, ScottieS1


RUTA_PROGRAMA = Path("pitea")

ARCHIVO_CONFIG = RUTA_PROGRAMA / "configuracion.toml"

RUTA_CACHE_GENERAL = RUTA_PROGRAMA / "cache"

conf = cargar_configuracion(ARCHIVO_CONFIG)

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now()

# Formatear la fecha y hora como "DD:MM:YYYY_HH:Minutos"
formato = fecha_hora_actual.strftime("%d-%m-%Y_%H:%M")

if formato != conf["ult_fecha"]:
    RUTA_CACHE_ESPECIFICA = RUTA_CACHE_GENERAL / f"cache_{formato}"
    conf["ult_fecha"] = formato
    conf["contador_cache"] = 0
else:
    RUTA_CACHE_ESPECIFICA = (
        RUTA_CACHE_GENERAL / f"cache_{formato}_{conf['contador_cache']}"
    )
    conf["contador_cache"] += 1

actualizar_conf(conf, ARCHIVO_CONFIG)


RUTA_OCULTACION = RUTA_CACHE_ESPECIFICA / "ocultacion"
RUTA_OCULTACION_DATOS = RUTA_OCULTACION / "datos"
RUTA_OCULTACION_IMAGEN = RUTA_OCULTACION / "imagen"
RUTA_OCULTACION_AUDIO = RUTA_OCULTACION / "audio"

RUTA_DATOS_CIFRADO = RUTA_OCULTACION_DATOS / "datos_originales_cifrados.txt"
RUTA_IMAGEN_CONTENEDORA = RUTA_OCULTACION_IMAGEN / "imagen_contenedora.%s"
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


LISTA_DIR_CACHE_OCULTACION = [
    RUTA_OCULTACION_DATOS,
    RUTA_OCULTACION_IMAGEN,
    RUTA_OCULTACION_AUDIO,
]

LISTA_DIR_CACHE_DESOCULTACION = [RUTA_DESOCULTACION_DATOS, RUTA_DESOCULTACION_IMAGEN]


SEMILLA = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"

VERBOSE = False

FORMATO_IMAGEN_DESOCULTACION = "png"
FORMATO_AUDIO_OCULTACION = "wav"

# Diccionario de modos disponibles en sstv, !no he comprobado que funcione con todos , es solo ejemplo
MODES = {
    "MartinM1": (MartinM1,(320, 256)),
    "Robot36": (Robot36,(320,240)),
    "ScottieS1": (ScottieS1,(320,256)),
}
