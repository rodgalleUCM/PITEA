import pysstv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from pydub import AudioSegment
from pydub.playback import play

from PIL import Image
import wave
import os

# Función para cifrar un archivo de texto usando AES
def cifrar_archivo(archivo_entrada, archivo_salida, clave):

    # Tamaño del bloque para el cifrado AES
    tamano_bloque = AES.block_size

    # Leer el archivo de entrada
    with open(archivo_entrada, 'rb') as f:
        datos = f.read()
    
    datos_padded = pad(datos, tamano_bloque) # Asegurarse de que los datos tengan un tamaño múltiplo del tamaño del bloque
    iv = get_random_bytes(tamano_bloque) # Generar un vector de inicialización aleatorio
    cifrador = AES.new(clave, AES.MODE_CBC, iv) # Crear el cifrador
    datos_cifrados = cifrador.encrypt(datos_padded) # Cifrar los datos
    
    with open(archivo_salida, 'wb') as f: # Guardar el IV y los datos cifrados en el archivo de salida
        f.write(iv + datos_cifrados) # Escribir el IV al inicio del archivo
    
    print(f'Archivo cifrado guardado en {archivo_salida}')

# Función para descifrar un archivo cifrado con AES
def descifrar_archivo(archivo_cifrado, archivo_salida, clave):
    tamano_bloque = AES.block_size
    
    # Leer el archivo cifrado
    with open(archivo_cifrado, 'rb') as f:
        iv = f.read(tamano_bloque)  # Leer el IV al inicio
        datos_cifrados = f.read() # Leer los datos cifrados
    
    # Crear el descifrador y descifrar los datos
    descifrador = AES.new(clave, AES.MODE_CBC, iv) 
    datos_descifrados = unpad(descifrador.decrypt(datos_cifrados), tamano_bloque)
    
    # Guardar los datos descifrados en el archivo de salida
    with open(archivo_salida, 'wb') as f:
        f.write(datos_descifrados)
    
    print(f'Archivo descifrado guardado en {archivo_salida}')


# Función para ocultar el archivo cifrado en una imagen PNG
def ocultar_datos_en_imagen(imagen_entrada, archivo_datos, imagen_salida):
    with open(archivo_datos, 'rb') as f:
        datos = f.read()

    datos_binarios = ''.join(format(byte, '08b') for byte in datos) # Convertir los datos a binarios del archivo cifrado
    imagen = Image.open(imagen_entrada)
    pixeles = imagen.load()
    ancho, alto = imagen.size

    indice_datos = 0
    total_datos = len(datos_binarios)

    for y in range(alto): # Iterar sobre los píxeles de la imagen
        for x in range(ancho):
            pixel = list(pixeles[x, y]) # Obtener el valor de los píxeles
            for canal in range(3): # Iterar sobre los canales de color (RGB) 
                if indice_datos < total_datos: # Si todavía hay datos para ocultar
                    pixel[canal] = (pixel[canal] & ~1) | int(datos_binarios[indice_datos]) # Ocultar el bit menos significativo
                    indice_datos += 1
            pixeles[x, y] = tuple(pixel) # Actualizar el valor de los píxeles
            if indice_datos >= total_datos: # Si ya se han ocultado todos los datos
                break
        if indice_datos >= total_datos: 
            break

    imagen.save(imagen_salida)
    print(f'Datos ocultos en la imagen: {imagen_salida}')


# Función para convertir imagen a audio SSTV
def imagen_a_sstv(imagen_entrada, archivo_salida):
    # Crear un objeto SSTV
    sstv = pysstv.SSTV()

    # Cargar la imagen
    sstv.load_image(imagen_entrada)

    # Codificar la imagen en audio
    audio_data = sstv.encode()

    # Guardar el archivo de audio
    with open(archivo_salida, 'wb') as f:
        f.write(audio_data)

    print(f'Archivo de audio SSTV guardado en {archivo_salida}')

# Función para reproducir el audio
def reproducir_audio(archivo_audio):
    audio_segment = AudioSegment.from_file(archivo_audio)
    play(audio_segment)

def sstv_a_imagen(archivo_audio, imagen_salida):
    # Crear un objeto SSTV
    sstv = pysstv.SSTV()

    # Leer el archivo de audio
    with open(archivo_audio, 'rb') as f:
        audio_data = f.read()

    # Decodificar el audio en una imagen
    sstv.decode(audio_data)
    sstv.save_image(imagen_salida)

    print(f'Imagen SSTV guardada en {imagen_salida}')



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

# Función para extraer la imagen del archivo de audio
def extraer_datos_de_audio(audio_entrada, archivo_salida, tamano_imagen):
    audio = wave.open(audio_entrada, mode='rb')
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()

    datos_binarios = ''
    for i in range(len(frames)):
        datos_binarios += str(frames[i] & 1)
    
    datos_extraidos = int(datos_binarios[:tamano_imagen * 8], 2).to_bytes(tamano_imagen, byteorder='big')

    with open(archivo_salida, 'wb') as archivo_img:
        archivo_img.write(datos_extraidos)
    
    print(f'La imagen ha sido extraída y guardada en {archivo_salida}')

# Función para extraer los datos de la imagen
def extraer_datos_de_imagen(imagen_entrada, archivo_salida, tamano_datos):
    imagen = Image.open(imagen_entrada)
    pixeles = imagen.load()
    ancho, alto = imagen.size

    datos_binarios = ''
    indice_datos = 0

    for y in range(alto):
        for x in range(ancho):
            pixel = list(pixeles[x, y])
            for canal in range(3):
                if indice_datos < tamano_datos * 8:
                    datos_binarios += str(pixel[canal] & 1)
                    indice_datos += 1
            if indice_datos >= tamano_datos * 8:
                break
        if indice_datos >= tamano_datos * 8:
            break

    datos = int(datos_binarios, 2).to_bytes(tamano_datos, byteorder='big')

    with open(archivo_salida, 'wb') as f:
        f.write(datos)
    
    print(f'Datos extraídos y guardados en {archivo_salida}')

# Ejecución del flujo completo
def flujo_completo():
    archivo_texto = 'archivo.txt'  # El archivo de texto que queremos cifrar
    archivo_cifrado = 'archivo_cifrado.txt'  # Archivo cifrado
    imagen_entrada = 'imagen.png'  # La imagen donde ocultaremos el archivo cifrado
    imagen_con_datos = 'imagen_con_datos.png'  # Imagen con el archivo cifrado oculto
    audio_entrada = 'audio.wav'  # El archivo de audio donde ocultaremos la imagen
    audio_con_imagen = 'audio_con_imagen.wav'  # El archivo de audio con la imagen oculta

    # Cifrar el archivo de texto
    clave = get_random_bytes(16)  # Clave de cifrado de 128 bits
    cifrar_archivo(archivo_texto, archivo_cifrado, clave)

    # Ocultar el archivo cifrado dentro de la imagen PNG
    ocultar_datos_en_imagen(imagen_entrada, archivo_cifrado, imagen_con_datos)

    # Ocultar la imagen con el archivo cifrado dentro de un archivo de audio WAV
    ocultar_datos_en_audio(audio_entrada, imagen_con_datos, audio_con_imagen)

    # # Ejemplo de uso con SSTV
    # imagen_a_sstv('imagen.png', 'sstv_audio.wav')
    # reproducir_audio('sstv_audio.wav')
    # sstv_a_imagen('sstv_audio.wav', 'sstv_imagen.png')

    tamano_imagen = os.path.getsize(imagen_con_datos)   
    # Extraer la imagen de un archivo de audio
    extraer_datos_de_audio(audio_con_imagen, 'imagen_extraida.png', tamano_imagen)

    # Extraer los datos de la imagen
    # La longitud de datos que se extraen debe ser exactamente la misma que la longitud del archivo cifrado
    tamano_datos = os.path.getsize('archivo_cifrado.txt')
    extraer_datos_de_imagen('imagen_extraida.png', 'archivo_extraido.txt', tamano_datos)

    # Descifrar el archivo extraído
    descifrar_archivo('archivo_extraido.txt', 'archivo_descifrado.txt', clave)

    print('El archivo original y el archivo descifrado son iguales:', 
          open(archivo_texto, 'rb').read() == open('archivo_descifrado.txt', 'rb').read())

    print('[+] Proceso completado con éxito!')

# Llamar al flujo completo
flujo_completo()
