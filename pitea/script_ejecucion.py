import click
from pitea.main import flujo_de_trabajo_ocultar, flujo_de_trabajo_desocultar
from pitea.mensajes import *
import pitea.constantes as constantes
from pitea.utils import comprobar_existencia_archivo
from pathlib import Path


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def main():
    """CLI para realizar análisis de grafos."""
    pass


@main.command()
@click.option(
    "--modo-cifrado",
    type=click.Choice(
        ["aes", "2"]
    ),  #! el 2 es solo para dejar indicado que hay que añadir mas opciones
    default="aes",
    help="Modo de cifrado a utilizar (ej. aes, rsa).",
)
@click.option(
    "--modo-cifrado-imagen",
    type=click.Choice(
        ["lsb", "2"]
    ),  #! el 2 es solo para dejar indicado que hay que añadir mas opciones
    default="lsb",
    help="Modo de ocultacion a usar en la imagen , no todos son compatibles con todos los formatos de imagen.",
)
@click.option(
    "--modo-cifrado-audio",
    type=click.Choice(
        ["lsb", "2", "sstv"]
    ),  #! hay un issue donde hay que cambiar el nombre de 1
    default="1",
    help="Modo de cifrado específico para audio (ej. sstv).",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Modo verbose , muestra mensajes del flujoy.",
)
@click.option(
    "-i",
    "--input",
    required=True,
    type=str,
    help="Archivos de entrada separados por espacio: "
    'para modo ocultación de audio "1" o "2", se requieren 3 archivos en orden [datos, imagen, audio]; '
    'para modo "sstv", se requieren 2 archivos en orden [datos, imagen] han de ser escritos entre comillas para que lo identifique python como un unico argumento',
)
@click.option(
    "-o",
    "--output",
    default="audio_salida",
    type=str,
    help="Archivos de salida separados por espacio: se requiere 1 o 2 archivos en orden [audio_salida, imagen_salida (opcional)].\nHan de ser escritos entre comillas para que lo identifique python como un unico argumento",
)
@click.option(
    "--contraseña", 
    required=True, 
    help="Contraseña para cifrado o descifrado."
)
@click.option(
    "--formato-salida",
    required=True,
    type=click.Choice(["wav", "mp4"]),
    default="wav",
    help="Formato de salida del audio (ej. wav, mp4).",
)
def ocultar(
    modo_cifrado,
    modo_cifrado_imagen,
    modo_cifrado_audio,
    input,
    output,
    contraseña,
    formato_salida,
    verbose,
):
    """
    Ejecuta la acción de ocultación usando los archivos especificados.
    """

    # activo el modo verbose o no
    if verbose:
        constantes.VERBOSE = True

    # Divido los distintos rutas de entrada y salida ya que lo recibo como una única cadena
    archivos_entrada = input.split()
    archivos_salida = output.split()

    # Compruebo que la cantidad de rutas es la adecuada
    num_entradas_esperadas = (
        3
        if modo_cifrado_audio in ["lsb", "2"]
        else 2  # En sstv el audio se genera solo por lo que no es necesario pasarle uno
    )

    if len(archivos_entrada) != num_entradas_esperadas:
        raise click.BadParameter(
            f"Se requieren {num_entradas_esperadas} archivos de entrada para el modo-cifrado-audio '{modo_cifrado_audio}', has introducido {len(archivos_entrada)}, {archivos_entrada}."
        )

    # Compruebo el número de archivos de salida
    if len(archivos_salida) < 1 or len(archivos_salida) > 2:
        raise click.BadParameter(
            "Se requiere 1 o 2 archivos de salida en el orden [audio_salida, imagen_salida (opcional)]."
        )

    # Renombramiento de variables para hacer mas leible el paso a los flujos y comprobacio  de existencia de archivos
    archivo_entrada_texto = Path(archivos_entrada[0])
    comprobar_existencia_archivo(archivo_entrada_texto)

    archivo_entrada_imagen = Path(archivos_entrada[1])
    comprobar_existencia_archivo(archivo_entrada_imagen)

    #si se le ha pasado el archivo se procesa si no, no
    if len(archivos_entrada) == 3:
        archivo_entrada_audio = Path(archivos_entrada[2])
        comprobar_existencia_archivo(archivo_entrada_audio)
    else:
        archivo_entrada_audio = None

    archivo_salida_audio = archivos_salida[0]

    # Mostramos parámetros para depuración
    if constantes.VERBOSE:
        click.echo(f"Modo de cifrado: {modo_cifrado}")
        click.echo(f"Modo de cifrado de imagen: {modo_cifrado_imagen}")
        click.echo(f"Modo de cifrado de audio: {modo_cifrado_audio}")
        click.echo(f"Contraseña: {contraseña}")
        click.echo(f"Formato de salida: {formato_salida}")

        click.echo(f"Archivo de entrada de texto: {archivo_entrada_texto}")
        click.echo(f"Archivo de entrada de imagen: {archivo_entrada_imagen}")
        if archivo_entrada_audio:
            click.echo(f"Archivo de entrada de audio: {archivo_entrada_audio}")

        click.echo(f"Archivo de salida de audio: {archivo_salida_audio}")

        print(SEPARADOR)

    flujo_de_trabajo_ocultar(
        modo_cifrado,
        modo_cifrado_imagen,
        modo_cifrado_audio,
        archivos_entrada,
        archivos_salida,
        contraseña,
        formato_salida,
    )


@main.command()
@click.option(
    "--modo-cifrado",
    type=click.Choice(
        ["aes", "2"]
    ),  #! el 2 es solo para dejar indicado que hay que añadir mas opciones
    default="aes",
    help="Modo de cifrado a utilizar (ej. aes, rsa).",
)
@click.option(
    "--modo-cifrado-imagen",
    type=click.Choice(
        ["lsb", "2"]
    ),  #! el 2 es solo para dejar indicado que hay que añadir mas opciones
    default="lsb",
    help="Modo de ocultacion a usar en la imagen , no todos son compatibles con todos los formatos de imagen.",
)
@click.option(
    "--modo-cifrado-audio",
    type=click.Choice(
        ["lsb", "2", "sstv"]
    ),  #! hay un issue donde hay que cambiar el nombre de 1
    default="1",
    help="Modo de cifrado específico para audio (ej. sstv).",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Modo verbose , muestra mensajes del flujoy.",
)
@click.option(
    "-i",
    "--input",
    default="audio_salida.wav",
    type=click.Path(exists=True),
    help="Archivos de audio de entrada ",
)
@click.option(
    "-o",
    "--output",
    default="datos_desocultos.txt",
    type=click.Path(),
    help="Archivos txt de salida",
)
@click.option("--contraseña", required=True, help="Contraseña para descifrado.")
def desocultar(
    modo_cifrado,
    modo_cifrado_imagen,
    modo_cifrado_audio,
    input,
    output,
    contraseña,
    verbose,
):
    """
    Ejecuta la acción de desocultación usando los archivos especificados.
    """

    # activo el modo verbose o no
    if verbose:
        constantes.VERBOSE = True

    comprobar_existencia_archivo(input)

    # Mostramos parámetros para depuración
    if constantes.VERBOSE:
        click.echo(f"Modo de cifrado: {modo_cifrado}")
        click.echo(f"Modo de cifrado de imagen: {modo_cifrado_imagen}")
        click.echo(f"Modo de cifrado de audio: {modo_cifrado_audio}")
        click.echo(f"Contraseña: {contraseña}")

        click.echo(f"Archivo de entrada de audio: {input}")
        click.echo(f"Archivo de salida de audio: {output}")

        print(SEPARADOR)

        flujo_de_trabajo_desocultar(
            modo_cifrado,
            modo_cifrado_imagen,
            modo_cifrado_audio,
            input,
            output,
            contraseña,
        )


if __name__ == "__main__":
    main()
