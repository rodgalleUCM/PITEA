from pitea.constantes import VERBOSE

MENSAJE_INICIO_FLUJO = "Iniciando flujo de %s ..."
SEPARADOR = "---------------------------------------------------------------------"


def print(str) :
    if VERBOSE :
        print(str)