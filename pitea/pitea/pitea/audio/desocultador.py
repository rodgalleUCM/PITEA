# Función para extraer la imagen del archivo de audio
def extraer_datos_de_audio(audio_entrada, archivo_salida, tamano_imagen):
    audio = wave.open(audio_entrada, mode="rb")
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()

    datos_binarios = ""
    for i in range(len(frames)):
        datos_binarios += str(frames[i] & 1)

    datos_extraidos = int(datos_binarios[: tamano_imagen * 8], 2).to_bytes(
        tamano_imagen, byteorder="big"
    )

    with open(archivo_salida, "wb") as archivo_img:
        archivo_img.write(datos_extraidos)

    print(f"La imagen ha sido extraída y guardada en {archivo_salida}")
