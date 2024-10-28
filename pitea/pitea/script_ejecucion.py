import click


@click.command()
@click.argument(
    "accion", type=click.Choice(["ocultar", "desocultar"], case_sensitive=False)
)
@click.option(
    "--modo-cifrado",
    type=click.Choice(["1", "2"]),
    required=True,
    help="Modo de cifrado a utilizar (ej. aes, rsa).",
)
@click.option(
    "--modo-cifrado-audio",
    type=click.Choice(["1", "2", "sstv"]),
    required=True,
    help="Modo de cifrado específico para audio (ej. sstv).",
)
@click.option(
    "-i",
    "--input",
    required=True,
    type=str,
    help="Archivos de entrada separados por espacio: "
    'para modo ocultación de audio "1" o "2", se requieren 3 archivos en orden [datos, imagen, audio]; '
    'para modo "sstv", se requieren 2 archivos en orden [datos, imagen].',
)
@click.option(
    "-o",
    "--output",
    required=True,
    type=str,
    help="Archivos de salida separados por espacio: se requiere 1 o 2 archivos en orden [audio_salida, imagen_salida (opcional)].\n Si se añade imagen_salida, se devolverá la imagen contendida; en caso contrario no.",
)
@click.option(
    "--contraseña", required=True, help="Contraseña para cifrado o descifrado."
)
@click.option(
    "--formato-salida",
    required=True,
    type=click.Choice(["wav", "mp4"]),
    default="str",
    help="Formato de salida del audio (ej. wav, mp4).",
)
def main(
    accion, modo_cifrado, modo_cifrado_audio, input, output, contraseña, formato_salida
):
    """
    Ejecuta la acción de ocultación o desocultación usando los archivos especificados.
    """

    # Divido los distintos rutas de entrada y salida ya que lo recibo como una única cadena
    archivos_entrada = input.split()
    archivos_salida = output.split()

    # Compruebo que la cantidad de rutas es la adecuada
    num_entradas_esperadas = (
        3
        if modo_cifrado_audio in ["1", "2"]
        else 2  # En sstv el audio se genera solo por lo que no es necesario pasarle uno
    )

    if len(archivos_entrada) != num_entradas_esperadas:
        raise click.BadParameter(
            f"Se requieren {num_entradas_esperadas} archivos de entrada para el modo-cifrado-audio '{modo_cifrado_audio}'."
        )

    # Compruebo el número de archivos de salida
    if len(archivos_salida) < 1 or len(archivos_salida) > 2:
        raise click.BadParameter(
            "Se requiere 1 o 2 archivos de salida en el orden [audio_salida, imagen_salida (opcional)]."
        )

    # Renombramiento de variables
    archivo_entrada_texto = archivos_entrada[0]
    archivo_entrada_imagen = archivos_entrada[1]
    archivo_entrada_audio = archivos_entrada[2] if len(archivos_entrada) == 3 else None

    archivo_salida_audio = archivos_salida[0]
    archivo_salida_imagen = archivos_salida[1] if len(archivos_salida) == 2 else None

    if accion == "ocultar":
        click.echo("Ocultando archivos...")
    elif accion == "desocultar":
        click.echo("Desocultando archivos...")

    # Mostramos parámetros para depuración
    click.echo(f"Modo de cifrado: {modo_cifrado}")
    click.echo(f"Modo de cifrado de audio: {modo_cifrado_audio}")
    click.echo(f"Contraseña: {contraseña}")
    click.echo(f"Formato de salida: {formato_salida}")

    click.echo(f"Archivo de entrada de texto: {archivo_entrada_texto}")
    click.echo(f"Archivo de entrada de imagen: {archivo_entrada_imagen}")
    if archivo_entrada_audio:
        click.echo(f"Archivo de entrada de audio: {archivo_entrada_audio}")

    click.echo(f"Archivo de salida de audio: {archivo_salida_audio}")
    if archivo_salida_imagen:
        click.echo(f"Archivo de salida de imagen: {archivo_salida_imagen}")


if __name__ == "__main__":
    main()
