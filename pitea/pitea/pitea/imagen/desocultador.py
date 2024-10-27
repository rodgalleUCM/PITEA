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
