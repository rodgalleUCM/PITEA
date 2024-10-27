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