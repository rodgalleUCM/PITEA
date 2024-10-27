# Función para ocultar la imagen en un archivo de audio WAV
def ocultar_datos_en_audio(audio_entrada, imagen_entrada, audio_salida):
    with open(imagen_entrada, 'rb') as img_file:
        datos_imagen = img_file.read()
    
    binarios_imagen = ''.join(format(byte, '08b') for byte in datos_imagen) # Convertir los datos de la imagen a binarios
    audio = wave.open(audio_entrada, mode='rb') 
    
    assert audio.getsampwidth() == 2, "El archivo de audio debe ser de 16 bits" # Asegurarse de que el archivo de audio sea de 16 bits
    
    frames = bytearray(list(audio.readframes(audio.getnframes()))) # Leer los frames del archivo de audio
    
    if len(binarios_imagen) > len(frames) * 8: # Asegurarse de que la imagen pueda ser ocultada en el archivo de audio
        raise ValueError("La imagen es demasiado grande para ser ocultada en este archivo de audio.")
    
    indice_datos = 0
    for i in range(len(frames)): # Iterar sobre los frames del archivo de audio
        if indice_datos < len(binarios_imagen): # Si todavía hay datos para ocultar
            frames[i] = (frames[i] & 254) | int(binarios_imagen[indice_datos]) # Ocultar el bit menos significativo
            indice_datos += 1
    
    with wave.open(audio_salida, 'wb') as audio_modificado: # Guardar los frames modificados en un nuevo archivo de audio
        audio_modificado.setparams(audio.getparams())  # Copiar los parámetros del archivo de audio original
        audio_modificado.writeframes(frames) # Escribir los frames modificados
    
    audio.close()
    print(f'La imagen ha sido ocultada en el archivo de audio: {audio_salida}')
