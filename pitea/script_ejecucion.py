import click
from pitea.main import flujo_de_trabajo_ocultar, flujo_de_trabajo_desocultar
import pitea.constantes as constantes
from pitea.mensajes import SEPARADOR
from pitea.utils import comprobar_existencia_archivo
from opciones_ocultadores import OPCIONES_CIFRADO, OPCIONES_DESOCULTACION_IMAGEN, OPCIONES_DESCOCULTACION_AUDIO,OPCIONES_OCULTACION_IMAGEN,OPCIONES_OCULTACION_AUDIO


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def main():
    """PITEA"""
    pass


@main.command()
@click.option(
    "--modo-cifrado",
    type=click.Choice(
        OPCIONES_CIFRADO
    ),  
    default="aes",
    help=f"Modo de cifrado a utilizar ({'/'.join(OPCIONES_CIFRADO)}): ",
)
@click.option(
    "--modo-cifrado-imagen",
    type=click.Choice(
        OPCIONES_OCULTACION_IMAGEN
    ), 
    default="lsb",
    help=f"Modo de ocultacion a usar en la imagen ({'/'.join(OPCIONES_OCULTACION_IMAGEN)}): ",
)
@click.option(
    "--modo-cifrado-audio",
    type=click.Choice(
        OPCIONES_OCULTACION_AUDIO
    ),  
    default="lsb",
    help=f"Modo de ocultacion específico para audio ({'/'.join(OPCIONES_OCULTACION_AUDIO)}): ",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Modo verbose , muestra mensajes del flujo.",
)
@click.option(
    "-i",
    "--input",
    required=True,
    type=click.Path(exists=True),
    help="Archivo de datos a ocultar",
)
@click.option(
    "--input_imagen",
    type=click.Path(exists=True),
    help="Archivo de imagen requerido para ciertos modo de ocultacion de imagen ",
)
@click.option(
    "--input_audio",
    type=click.Path(exists=True),
    help="Archivo de audio requerido para ciertos modo de ocultacion de audio ",
)
@click.option(
    "-o",
    "--output",
    default="audio_salida",
    type=click.Path(),
    help="Nombre del archivo de salida", 
)
@click.option(
    "--contraseña", 
    required=True, 
    help="Contraseña para cifrado o descifrado."
)
def ocultar(
    modo_cifrado,
    modo_cifrado_imagen,
    modo_cifrado_audio,
    input,
    input_imagen,
    input_audio,
    output,
    contraseña,
    verbose,
):
    """
    Ejecuta la acción de ocultación usando los archivos especificados.
    """

    # activo el modo verbose o no
    if verbose:
        constantes.VERBOSE = True

   
    comprobar_existencia_archivo(input)

    if input_imagen is None and modo_cifrado_imagen in OPCIONES_OCULTACION_IMAGEN:
        raise click.BadParameter(f"En el modo {modo_cifrado_imagen} es necesario añadir la opcion --input_imagen ARCHIVO ")
    elif input_imagen is not None:
        comprobar_existencia_archivo(input_imagen)

    if input_audio is None and modo_cifrado_audio in OPCIONES_OCULTACION_AUDIO:
        raise click.BadParameter(f"En el modo {modo_cifrado_audio} es necesario añadir la opcion --input_audio ARCHIVO ")
    elif input_audio is not None :
        comprobar_existencia_archivo(input_audio)


    # Mostramos parámetros para depuración
    if constantes.VERBOSE:
        click.echo(f"Modo de cifrado: {modo_cifrado}")
        click.echo(f"Modo de cifrado de imagen: {modo_cifrado_imagen}")
        click.echo(f"Modo de cifrado de audio: {modo_cifrado_audio}")
        click.echo(f"Contraseña: {contraseña}")

        click.echo(f"Archivo de entrada de texto: {input}")
        if input_imagen:
            click.echo(f"Archivo de entrada de imagen: {input_imagen}")
        if input_audio:
            click.echo(f"Archivo de entrada de audio: {input_audio}")

        click.echo(f"Archivo de salida de audio: {output}")

        print(SEPARADOR)

    flujo_de_trabajo_ocultar(
        modo_cifrado,
        modo_cifrado_imagen,
        modo_cifrado_audio,
        input,
        input_imagen,
        input_audio,
        output,
        contraseña,
    )


@main.command()
@click.option(
    "--modo-cifrado",
    type=click.Choice(
        OPCIONES_CIFRADO
    ),  
    default="aes",
    help=f"Modo de cifrado a utilizar ({'/'.join(OPCIONES_CIFRADO)}): ",
)
@click.option(
    "--modo-cifrado-imagen",
    type=click.Choice(
        OPCIONES_DESOCULTACION_IMAGEN
    ),  
    default="lsb",
    help=f"Modo de ocultacion usado en la imagen ({'/'.join(OPCIONES_OCULTACION_IMAGEN)}): ",
)
@click.option(
    "--modo-cifrado-audio",
    type=click.Choice(
        OPCIONES_DESCOCULTACION_AUDIO
    ),  
    default="lsb",
    help=f"Modo de ocultacion usado en el audio ({'/'.join(OPCIONES_OCULTACION_AUDIO)}): ",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Modo verbose , muestra mensajes del flujoy.",
)
@click.option(
    "--input_audio",
    type=click.Path(exists=True),
    help="Archivos de audio de entrada ",
)
@click.option(
    "--input_imagen",
    type=click.Path(exists=True),
    help="Archivos de imagen de entrada ",
)
@click.option(
    "-i",
    "--input_text",
    type=click.Path(exists=True),
    help="Archivos de texto de entrada ",
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
    input_audio,
    input_imagen,
    input_text,
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

    #Se puede pasar o el de audio o el de imagen, los dos no y uno obligatorio
    if not input_audio  and not input_imagen and not input_text :
        click.BadOptionUsage("No se ha introducido nigún input")
    elif input_audio and input_imagen :
        click.BadOptionUsage("Solo se puede introducir input_imagen si no introduce input_audio")
    elif input_text and input_imagen :
        click.BadOptionUsage("Solo se puede introducir input_text si no introduce input_imagen")
    elif input_text and input_audio :
        click.BadOptionUsage("Solo se puede introducir input_text si no introduce input_audio")

    # Mostramos parámetros para depuración
    if constantes.VERBOSE:
        click.echo(f"Modo de cifrado: {modo_cifrado}")
        click.echo(f"Modo de cifrado de imagen: {modo_cifrado_imagen}")
        click.echo(f"Modo de cifrado de audio: {modo_cifrado_audio}")
        click.echo(f"Contraseña: {contraseña}")

        if input_audio :
            click.echo(f"Archivo de entrada de audio: {input_audio}")
        if input_imagen:
            click.echo(f"Archivo de entrada de imagen: {input_imagen}")

        click.echo(f"Archivo de salida de audio: {output}")

        print(SEPARADOR)

        flujo_de_trabajo_desocultar(
            modo_cifrado,
            modo_cifrado_imagen,
            modo_cifrado_audio,
            input_audio,
            input_imagen,
            input_text,
            output,
            contraseña,
        )


if __name__ == "__main__":
    main()
