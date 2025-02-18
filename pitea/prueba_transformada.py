from PIL import Image
from pitea.imagen.OcultadorImagenLSB import OcultadorImagenLSB


# Test de transformaciones sin ocultar datos
ruta_imagen_prueba = "archivos_prueba/imagen_salida_sstv.png"
imagen_original = Image.open(ruta_imagen_prueba)

# Crear instancia de OcultadorImagen
ocultador = OcultadorImagenLSB(ruta_imagen_prueba, modo_cifrador="none")

# Función para obtener los primeros 32 LSB (bits de la cabecera) de la imagen
def obtener_primeros_32_bits(imagen, ancho, alto):
    pixeles = imagen.load()
    bits = ""
    for y in range(alto):
        for x in range(ancho):
            pixel = pixeles[x, y]
            for canal in range(3):  # RGB
                bits += str(pixel[canal] & 1)  # Extraer LSB
                if len(bits) >= 32:
                    return bits
    return bits

# Extraer los 32 bits originales
bits_originales = obtener_primeros_32_bits(imagen_original, imagen_original.width, imagen_original.height)
print("Bits originales:", bits_originales)

# Transformar la imagen
imagen_transformada = ocultador.transformar_imagen(imagen_original)

# Extraer los 32 bits después de la transformación
bits_transformados = obtener_primeros_32_bits(imagen_transformada, imagen_transformada.width, imagen_transformada.height)
print("Bits transformados:", bits_transformados)

# Invertir la transformación
imagen_revertida = ocultador.transformar_imagen_inversa(imagen_transformada)

# Extraer los 32 bits después de revertir la transformación
bits_revertidos = obtener_primeros_32_bits(imagen_revertida, imagen_revertida.width, imagen_revertida.height)
print("Bits revertidos:", bits_revertidos)

# Comparar píxeles para verificar reversibilidad completa
if list(imagen_original.getdata()) == list(imagen_revertida.getdata()):
    print("Transformaciones completamente reversibles.")
else:
    print("Error: Las transformaciones no son reversibles.")

# Comparar los bits
if bits_originales == bits_revertidos:
    print("La cabecera permanece intacta después de las transformaciones.")
else:
    print("Error: La cabecera fue alterada durante las transformaciones.")
