import pitea.constantes as constantes
import builtins

MENSAJE_INICIO_FLUJO = "Iniciando flujo de %s ..."
SEPARADOR = "---------------------------------------------------------------------"


def print(
    str,
):
    
    if constantes.VERBOSE:
        builtins.print(str)
