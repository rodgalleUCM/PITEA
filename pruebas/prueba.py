import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image
import wave
import struct

# Función para obtener el tamaño del archivo
def obtener_tamano_archivo(archivo):
    return os.path.getsize(archivo)

# Función para cifrar un archivo de texto usando AES
def cifrar_archivo(archivo_entrada, archivo_salida, clave):
    tamano_bloque = AES.block_size
    with open(archivo_entrada, 'rb') as f:
        datos = f.read()

    datos_padded = pad(datos, tamano_bloque)
    iv = get_random_bytes(tamano_bloque)
    cifrador = AES.new(clave, AES.MODE_CBC, iv)
    datos_cifrados = cifrador.encrypt(datos_padded)

    with open(archivo_salida, 'wb') as f:
        f.write(iv + datos_cifrados)

    print(f'Archivo cifrado guardado en {archivo_salida}')

# Función para descifrar un archivo cifrado con AES
def descifrar_archivo(archivo_cifrado, archivo_salida, clave):
    tamano_bloque = AES.block_size
    with open(archivo_cifrado, 'rb') as f:
        iv = f.read(tamano_bloque)
        datos_cifrados = f.read()

    descifrador = AES.new(clave, AES.MODE_CBC, iv)
    datos_descifrados = unpad(descifrador.decrypt(datos_cifrados), tamano_bloque)

    with open(archivo_salida, 'wb') as f:
        f.write(datos_descifrados)

    print(f'Archivo descifrado guardado en {archivo_salida}')

# Función para ocultar datos cifrados en una imagen
def ocultar_datos_en_imagen(imagen_entrada, archivo_datos, imagen_salida):
    with open(archivo_datos, 'rb') as f:
        datos = f.read()

    # Convertir los datos a binario
    datos_binarios = ''.join(format(byte, '08b') for byte in datos)


    # Añadir una cabecera con el tamaño de los datos (32 bits)
    tamano_datos = format(len(datos_binarios), '032b')


    datos_binarios = tamano_datos + datos_binarios  # Cabecera + Datos

    imagen = Image.open(imagen_entrada)
    pixeles = imagen.load()
    ancho, alto = imagen.size

    indice_datos = 0
    total_datos = len(datos_binarios)

    # Comprobar si la imagen tiene suficiente espacio para almacenar los datos
    if total_datos > ancho * alto * 3:
        raise ValueError("La imagen no tiene suficiente espacio para almacenar todos los datos.")

    for y in range(alto):
        for x in range(ancho):
            pixel = list(pixeles[x, y])
            for canal in range(3):
                if indice_datos < total_datos:
                    pixel[canal] = (pixel[canal] & ~1) | int(datos_binarios[indice_datos])  # Limpiar el bit menos significativo y añadir el bit de los datos
                    indice_datos += 1
            pixeles[x, y] = tuple(pixel)
            if indice_datos >= total_datos:
                break
        if indice_datos >= total_datos:
            break

    imagen.save(imagen_salida, format="PNG", compress_level=5) 
    print(f'Datos ocultos en la imagen: {imagen_salida}')

# Función para extraer datos ocultos de una imagen
def extraer_datos_de_imagen(imagen_entrada, archivo_salida):
    imagen = Image.open(imagen_entrada)
    pixeles = imagen.load()
    ancho, alto = imagen.size

    datos_binarios = ''
    tamano_datos = 0  # Inicializamos la variable de tamaño de datos

    # Leer los primeros 32 bits que contienen el tamaño de los datos ocultos
    for y in range(alto):
        for x in range(ancho):
            pixel = list(pixeles[x, y])
            for canal in range(3):
                datos_binarios += str(pixel[canal] & 1)  # Extraer el bit menos significativo
                if len(datos_binarios) >= 32:
                    tamano_datos = int(datos_binarios[:32], 2)  # Leer el tamaño de los datos
                    datos_binarios = datos_binarios[32:]  # Eliminar la cabecera

                    # Si el tamaño de los datos es mayor que 0, seguimos extrayendo los datos
                    if tamano_datos > 0:
                        break
            if tamano_datos > 0:
                break
        if tamano_datos > 0:
            break

    if tamano_datos == 0:
        raise ValueError("No se pudo extraer el tamaño de los datos ocultos.")

    # Ahora extraemos los datos ocultos según el tamaño indicado
    while len(datos_binarios) < tamano_datos+32:
        for y in range(alto):
            for x in range(ancho):
                pixel = list(pixeles[x, y])
                for canal in range(3):
                    datos_binarios += str(pixel[canal] & 1)
                    if len(datos_binarios) >= tamano_datos+32:
                        break
                if len(datos_binarios) >= tamano_datos+32:
                    break
            if len(datos_binarios) >= tamano_datos+32:
                break
    # Convertir los datos binarios en bytes
    datos_binarios = datos_binarios[32:] 
    datos_extraidos = int(datos_binarios, 2).to_bytes(tamano_datos// 8, byteorder='big')
    
    # Guardar los datos extraídos en un archivo
    with open(archivo_salida, 'wb') as archivo_img:
        archivo_img.write(datos_extraidos)

    print(f'Los datos ocultos han sido extraídos y guardados en {archivo_salida}')

# Función para ocultar datos en un archivo de audio
def ocultar_datos_en_audio(audio_entrada, imagen_entrada, audio_salida):
    # Leer los datos de la imagen
    with open(imagen_entrada, 'rb') as img_file:
        datos_imagen = img_file.read()
    
    # Convertir los datos de la imagen a una representación binaria
    binarios_imagen = ''.join(format(byte, '08b') for byte in datos_imagen)

    # Añadir una cabecera con el tamaño de los datos (32 bits)
    tamano_datos = format(len(binarios_imagen), '032b')
    binarios_imagen = tamano_datos + binarios_imagen  # Cabecera + Datos
 
    # Abrir el archivo de audio
    audio = wave.open(audio_entrada, mode='rb')

    # Verificar que el audio sea de 16 bits
    assert audio.getsampwidth() == 2, "El archivo de audio debe ser de 16 bits"

    # Leer los frames del archivo de audio
    frames = bytearray(list(audio.readframes(audio.getnframes())))

    # Verificar si el archivo de audio tiene capacidad suficiente para ocultar los datos
    if len(binarios_imagen) > len(frames) * 8: 
        raise ValueError("La imagen (con la cabecera) es demasiado grande para ser ocultada en este archivo de audio.")

    # Ocultar los datos binarios en los bits menos significativos de los frames
    indice_datos = 0
    for i in range(len(frames)):
        if indice_datos < len(binarios_imagen):
            frames[i] = (frames[i] & 254) | int(binarios_imagen[indice_datos]) # Limpiar el bit menos significativo y añadir el bit de los datos
            indice_datos += 1

    # Guardar los frames modificados en un nuevo archivo de audio
    with wave.open(audio_salida, 'wb') as audio_modificado:
        audio_modificado.setparams(audio.getparams())  # Copiar los parámetros del archivo original
        audio_modificado.writeframes(frames)

    # Cerrar el archivo de audio original
    audio.close()
    print(f'La imagen ha sido ocultada en el archivo de audio: {audio_salida}')


# Función para extraer los datos ocultos de un archivo de audio
def extraer_datos_de_audio(audio_entrada, archivo_salida):
    # Abrir el archivo de audio
    audio = wave.open(audio_entrada, mode='rb')
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()

    # Extraer los bits menos significativos
    datos_binarios = ''

   
    # Leer los primeros 32 bits que contienen el tamaño de los datos ocultos
    for i in range(len(frames)):
        datos_binarios += str(frames[i] & 1)  # Extraer el bit menos significativo
        if len(datos_binarios) >= 32:
            tamano_datos = int(datos_binarios[:32], 2)  # Leer el tamaño de los datos
            datos_binarios = datos_binarios[32:]  # Eliminar la cabecera
            break  # Una vez obtenida la cabecera, podemos detener la lectura
    
    # Verificar que la cabecera tenga el tamaño correcto
    if tamano_datos == 0:
        raise ValueError("No se pudo extraer el tamaño de los datos ocultos.")

    # Extraer los datos de acuerdo al tamaño especificado
    
    for i in range(len(frames)):
        datos_binarios += str(frames[i] & 1)  # Extraer el bit menos significativo
        if len(datos_binarios) >= tamano_datos+32:
            break

    datos_binarios = datos_binarios[32:]
    datos_extraidos = int(datos_binarios, 2).to_bytes(tamano_datos// 8, byteorder='big')
    # Guardar los datos extraídos en un archivo
    with open(archivo_salida, 'wb') as archivo_img:
        archivo_img.write(datos_extraidos)

    print(f'Los datos ocultos han sido extraídos y guardados en {archivo_salida}')


# Flujo principal
def flujo_completo():
    archivo_texto = 'archivo.txt'  # El archivo de texto que queremos cifrar
    archivo_cifrado = 'archivo_cifrado.txt'  # Archivo cifrado
    imagen_entrada = 'imagen.png'  # La imagen donde ocultaremos el archivo cifrado
    imagen_con_datos = 'imagen_con_datos.png'  # Imagen con el archivo cifrado oculto
    audio_entrada = 'audio.wav'  # El archivo de audio donde ocultaremos la imagen
    audio_con_imagen = 'audio_con_imagen.wav'  # El archivo de audio con la imagen oculta

    clave = get_random_bytes(16)
    print(f"Tamaño del archivo de texto original: {obtener_tamano_archivo(archivo_texto)} bytes\n")

    cifrar_archivo(archivo_texto, archivo_cifrado, clave)
    print(f"Tamaño del archivo de texto cifrado: {obtener_tamano_archivo(archivo_cifrado)} bytes\n")

    ocultar_datos_en_imagen(imagen_entrada, archivo_cifrado, imagen_con_datos)
    print(f"Tamaño de la imagen: {obtener_tamano_archivo(imagen_entrada)} bytes")
    print(f"Tamaño de la imagen con datos : {obtener_tamano_archivo(imagen_con_datos)} bytes\n")


    ocultar_datos_en_audio(audio_entrada, imagen_con_datos, audio_con_imagen)
    print(f"Tamaño del archivo de audio: {obtener_tamano_archivo(audio_entrada)} bytes")
    print(f"Tamaño del archivo de audio con imagen: {obtener_tamano_archivo(audio_con_imagen)} bytes\n")

    extraer_datos_de_audio(audio_con_imagen, 'imagen_extraida.png')
    print(f"Tamaño de la imagen extraída: {obtener_tamano_archivo('imagen_extraida.png')} bytes\n")
    
    print (f'La imagen extraida es igual a la imagen original: {open(imagen_entrada, "rb").read() == open("imagen_extraida.png", "rb").read()}')

    extraer_datos_de_imagen(imagen_con_datos, 'archivo_extraido.txt')
    print(f"Tamaño del archivo extraído: {obtener_tamano_archivo('archivo_extraido.txt')} bytes\n")

    descifrar_archivo('archivo_extraido.txt', 'archivo_descifrado.txt', clave)
    print(f"Tamaño del archivo descifrado: {obtener_tamano_archivo('archivo_descifrado.txt')} bytes\n")

    original = open(archivo_texto, 'rb').read()
    descifrado = open('archivo_descifrado.txt', 'rb').read()
    print('El archivo original y el archivo descifrado son iguales:', original == descifrado)
    print('[+] Proceso completado con éxito!')

if __name__ == "__main__":
    flujo_completo()
