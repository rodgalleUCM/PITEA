from abc import ABC, abstractmethod
from PIL import Image
from pitea.constantes import (
    RUTA_IMAGEN_CONTENEDORA,
    RUTA_DATOS_CIFRADOS_DESOCULTACION,
    RUTA_DATOS_CIFRADO,
)
import cv2
import numpy as np


class OcultadorImagen(ABC):
    nombre = ""

    def __init__(self, ruta_imagen):
        if ruta_imagen:
            self.formato = ruta_imagen.split(".")[-1]
            self.imagen = Image.open(ruta_imagen)
            self.pixeles = self.imagen.load()
            self.ancho, self.alto = self.imagen.size

    @abstractmethod
    def ocultar(self, datos_imagen,altura_imagen = None,anchura_imagen=None):
        pass

    @abstractmethod
    def desocultar(self):
        pass

    def ocultar_guardar(self,altura_imagen= None,anchura_imagen=None):
        with open(RUTA_DATOS_CIFRADO, "rb") as f:
            datos = f.read()

        imagen, formato = self.ocultar(datos,altura_imagen,anchura_imagen)

        imagen.save(str(RUTA_IMAGEN_CONTENEDORA) % formato)

        print(
            f"Imagen contenedora guardada en {str(RUTA_IMAGEN_CONTENEDORA) % formato}"
        )

        return imagen, formato

    def desocultar_guardar(self):
        datos_extraidos = self.desocultar()

        with open(RUTA_DATOS_CIFRADOS_DESOCULTACION, "wb") as f:
            f.write(datos_extraidos)

        print(f"Datos cifrados guardados en {RUTA_DATOS_CIFRADOS_DESOCULTACION}")

    def transformar_imagen (self,imagen):
        
        #formato RGB
        imagen = imagen.convert("RGB")
        
        # Convertir la imagen PIL a un array de NumPy (para poder usar la indexación)
        imagen_np = np.array(imagen)

        # Obtener las dimensiones de la imagen
        h, w = imagen_np.shape[:2]  # Altura y ancho de la imagen
        h1, w1 = h // 2, w // 2  # Punto medio para dividir en 4 partes

        # Cortar en 4 partes
        img1 = imagen_np[0:h1, 0:w1]  # Arriba izquierda
        img2 = imagen_np[h1:h, 0:w1]  # Abajo izquierda
        img3 = imagen_np[0:h1, w1:w]  # Arriba derecha
        img4 = imagen_np[h1:h, w1:w]  # Abajo derecha

        # Modificar colores
        img1 = cv2.bitwise_not(img1)
        img2 = cv2.bitwise_not(img2)
        img3 = cv2.bitwise_not(img3)
        img4 = cv2.bitwise_not(img4)

        # Reorganizar la imagen
        imagen_modificada = cv2.vconcat([
            cv2.hconcat([img4, img3]),
            cv2.hconcat([img2, img1])
        ])

        # Convertir el array de NumPy de vuelta a PIL
        imagen_modificada_pil = Image.fromarray(imagen_modificada)

        return imagen_modificada_pil 
    
    def transformar_imagen_inversa (self,imagen):
        
        imagen = imagen.convert("RGB")
        
        # Convertir la imagen PIL a un array de NumPy (para poder usar la indexación)
        imagen_np = np.array(imagen)

        # Obtener las dimensiones de la imagen
        h, w = imagen_np.shape[:2]  # Altura y ancho de la imagen
        h1, w1 = h // 2, w // 2  # Punto medio para dividir en 4 partes

        # Cortar en 4 partes (con la disposición invertida)
        img4 = imagen_np[0:h1, 0:w1]  # Arriba izquierda (cambio de posición)
        img3 = imagen_np[0:h1, w1:w]  # Arriba derecha (cambio de posición)
        img2 = imagen_np[h1:h, 0:w1]  # Abajo izquierda (cambio de posición)
        img1 = imagen_np[h1:h, w1:w]  # Abajo derecha (cambio de posición)

        # Restaurar colores (invertir colores nuevamente)
        img1 = cv2.bitwise_not(img1)
        img2 = cv2.bitwise_not(img2)
        img3 = cv2.bitwise_not(img3)
        img4 = cv2.bitwise_not(img4)

        # Reorganizar la imagen a su disposición original
        imagen_recuperada = cv2.vconcat([
            cv2.hconcat([img1, img3]),
            cv2.hconcat([img2, img4])
        ])

        # Convertir el array de NumPy de vuelta a PIL
        imagen_recuperada_pil = Image.fromarray(imagen_recuperada)

        return imagen_recuperada_pil 


