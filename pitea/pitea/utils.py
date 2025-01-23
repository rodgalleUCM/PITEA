

import tomllib
import click
import tomli_w
import pitea.constantes as constantes
from pathlib import Path


def crear_cache(lista) :
    conf = cargar_configuracion(constantes.ARCHIVO_CONFIG)

    retorno = conf["contador_cache"]

    conf["contador_cache"] = int(conf["contador_cache"]) + 1

    actualizar_conf(conf,constantes.ARCHIVO_CONFIG)

    for dir in lista :
        dir.mkdir(exist_ok=True, parents=True)

    return retorno 


def cargar_configuracion(archivo_conf):
    """Cargar la configuración desde un archivo TOML.

    Args:
        archivo_conf (str): Nombre del archivo de configuración.

    Returns:
        dict: Contenido del archivo de configuración.
              En caso de error, devuelve None.
    """
    try:
        with open(archivo_conf, "rb") as f:
            conf = tomllib.load(f)
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
        return None
    except PermissionError:
        print("No tienes permisos para acceder a este archivo.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

    return conf

def actualizar_conf(conf,archivo_conf):
    """Actualizar el archivo de configuración.

    Args:
        conf (dict): Diccionario con el contenido en formato TOML.
        archivo_conf (str): Nombre del archivo de configuración.

    Returns:
        None
    """
    with open(archivo_conf, "wb") as f:
        tomli_w.dump(conf, f)

def comprobar_existencia_archivo(nombre) :
    ruta = Path(nombre)
    if not ruta.exists():
        raise click.UsageError(f"El archivo '{nombre}' no existe.")
    if not ruta.is_file():
        raise click.UsageError(f"'{nombre}' no es un archivo válido.")
