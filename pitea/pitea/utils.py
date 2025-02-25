import tomllib
import click
import tomli_w
from pathlib import Path


def crear_cache(lista):
    """
    Crea los directorios de caché especificados en la lista.

    Args:
        lista (list of Path): Lista de objetos `Path` que representan los directorios a crear.

    Notes:
        - Si el directorio ya existe, no se genera un error.
        - Se crean todos los directorios padres si no existen.

    """

    for dir in lista:
        dir.mkdir(exist_ok=True, parents=True)


def cargar_configuracion(archivo_conf):
    """
    Carga la configuración desde un archivo TOML.

    Args:
        archivo_conf (str): Ruta del archivo de configuración en formato TOML.

    Returns:
        dict or None: Un diccionario con el contenido del archivo de configuración si se carga correctamente.
                    Retorna None en caso de error.
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


def actualizar_conf(conf, archivo_conf):
    """
    Actualiza el archivo de configuración con los valores de 'conf'.

    Args:
        conf (dict): Diccionario que contiene la configuración en formato TOML.
        archivo_conf (str): Ruta del archivo de configuración a actualizar.

    Returns:
        None

    """

    with open(archivo_conf, "wb") as f:
        tomli_w.dump(conf, f)


def comprobar_existencia_archivo(nombre):
    """
    Verifica la existencia y validez de un archivo.

    Args:
        nombre (str): Ruta del archivo a comprobar.

    Raises:
        click.UsageError: Si el archivo no existe o no es un archivo válido.
    """
    ruta = Path(nombre)
    if not ruta.exists():
        raise click.UsageError(f"El archivo '{nombre}' no existe.")
    if not ruta.is_file():
        raise click.UsageError(f"'{nombre}' no es un archivo válido.")
