from pitea.imagen.OcultadorImagen import OcultadorImagen
from pitea.constantes import RUTA_IMAGEN_CONTENEDORA , RUTA_DATOS_CIFRADOS_DESOCULTACION,RUTA_DATOS_CIFRADO
from pitea.mensajes import print

class OcultadorImagenLSB(OcultadorImagen) :
    def ocultar(self) :
        with open(RUTA_DATOS_CIFRADO, 'rb') as f:
            datos = f.read()

        datos_binarios = ''.join(format(byte, '08b') for byte in datos) # Convertir los datos a binarios del archivo cifrado
        indice_datos = 0
        total_datos = len(datos)
        for y in range(self.alto):  # Iterar sobre los píxeles de la imagen
            for x in range(self.ancho):
                pixel = list(self.pixeles[x, y])  # Obtener el valor de los píxeles
                for canal in range(3):  # Iterar sobre los canales de color (RGB)
                    if indice_datos < total_datos:  # Si todavía hay datos para ocultar
                        pixel[canal] = (pixel[canal] & ~1) | int(
                            datos[indice_datos]
                        )  # Ocultar el bit menos significativo
                        indice_datos += 1
                self.pixeles[x, y] = tuple(pixel)  # Actualizar el valor de los píxeles
                if indice_datos >= total_datos:  # Si ya se han ocultado todos los datos
                    break
            if indice_datos >= total_datos:
                break

        self.imagen.save(RUTA_IMAGEN_CONTENEDORA % self.formato)

        print(f'Imagen contenedora guardada en {RUTA_IMAGEN_CONTENEDORA % self.formato}')

        return self.imagen , self.formato
    def desocultar(self) :
        datos_binarios = ""
        indice_datos = 0
        tamano_datos = 0 

        for y in range(self.alto):
            for x in range(self.ancho):
                pixel = list(self.pixeles[x, y])
                for canal in range(3):
                    if indice_datos < tamano_datos * 8:
                        datos_binarios += str(pixel[canal] & 1)
                        indice_datos += 1
                if indice_datos >= tamano_datos * 8:
                    break
            if indice_datos >= tamano_datos * 8:
                break


        with open(RUTA_DATOS_CIFRADOS_DESOCULTACION, "wb") as f:
            f.write(datos_binarios)

        print(f'Datos cifrados guardados en {RUTA_DATOS_CIFRADOS_DESOCULTACION}')


        return datos_binarios

       
        

