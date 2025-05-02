from abc import ABC, abstractmethod
from PIL import Image
from constantes import constantes
import cv2
import numpy as np
from pitea.mensajes import print


class OcultadorImagen(ABC):
    """
    Interfaz base para ocultadores de imagen en Pitea.

    Subclases deben implementar `_ocultar` y `_desocultar` para aplicar y extraer
    datos binarios en las imágenes.

    Atributos:
        nombre (str): Identificador del modo de ocultación ('lsb', 'text', 'none').
        _formato (str): Extensión/formato de la imagen (png, jpg, etc.).
        _imagen (PIL.Image.Image): Instancia de imagen cargada.
        _cifrado (int): Flag (1 o 0) indicando si se aplicó cifrado previo.
        _ruta_txt (str or None): Ruta a archivo de texto si se emplea ocultación por texto.
    """
    
    nombre = ""
    def __init__(self, ruta_imagen, modo_cifrador, ruta_txt=None):
        """
        Inicializa el ocultador de imagen.

        Args:
            ruta_imagen (str): Ruta al archivo de imagen contenedora.
            modo_cifrador (str): Identificador de cifrado aplicado antes de ocultar.
            ruta_txt (str, optional): Ruta a archivo de texto si aplica.
        """
        
        if ruta_imagen:
            self._formato = ruta_imagen.split(".")[-1]
            self._imagen = Image.open(ruta_imagen)
        else:
            self._ruta_txt = ruta_txt
        self._cifrado = 1 if modo_cifrador not in ["none"] else 0


    @abstractmethod
    def _ocultar(self, datos_imagen, altura_imagen=None, anchura_imagen=None):
        """
        Cifra o inserta datos binarios en la imagen.

        Args:
            datos_imagen (bytes): Bytes a ocultar (p.ej. cifrados).
            altura_imagen (int, optional): Nueva altura si requiere resize.
            anchura_imagen (int, optional): Nueva anchura si requiere resize.

        Returns:
            tuple: (imagen_contenedora, formato_str).
        """
        pass

    @abstractmethod
    def _desocultar(self):
        """
        Extrae y retorna datos ocultos de la imagen.

        Returns:
            bytes: Contenido binario ocultado.
        """
        pass

    def ocultar_guardar(self, altura_imagen=None, anchura_imagen=None):
        """
        Gestiona la lectura de datos cifrados, la ocultación y guarda la imagen resultante.

        1. Lee bytes cifrados desde cache.
        2. Invoca `_ocultar` para embed.
        3. Guarda imagen sin transformar.
        4. Aplica transformaciones inversibles (_transformar_imagen).
        5. Guarda imagen final.

        Args:
            altura_imagen (int, optional): Altura para ocultación SSTV.
            anchura_imagen (int, optional): Anchura para ocultación SSTV.

        Returns:
            tuple: (imagen_transformada, formato_str).
        """
        with open(constantes.RUTA_DATOS_CIFRADO, "rb") as f:
            datos = f.read()

        imagen, formato = self._ocultar(datos, altura_imagen, anchura_imagen)

        imagen.save(str(constantes.RUTA_IMAGEN_CONTENEDORA_SIN_TRANSFORMAR) % formato)

        # Ocultar el texto realizando transformaciones con inversa a la imagen
        imagen = self._transformar_imagen(imagen)

        imagen.save(str(constantes.RUTA_IMAGEN_CONTENEDORA) % formato)

        print(
            f"Imagen contenedora guardada en {str(constantes.RUTA_IMAGEN_CONTENEDORA) % formato}"
        )

        return imagen, formato

    def desocultar_guardar(self):
        """
        Gestiona la inversión de transformaciones y la extracción de datos.

        1. Invierte transformaciones (_transformar_imagen_inversa).
        2. Guarda imagen destransformada.
        3. Extrae bytes ocultos con `_desocultar`.
        4. Guarda bytes cifrados en cache.
        """
        self._imagen = self._transformar_imagen_inversa(self._imagen)
        self._imagen.save(str(constantes.RUTA_IMAGEN_CONTENEDORA_DESOCULTACION_DESTRANSFORMADA) % self._formato)
        datos_extraidos = self._desocultar()

        with open(constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION, "wb") as f:
            f.write(datos_extraidos)

        print(f"Datos cifrados guardados en {constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION}")

    def _transformar_imagen(self, imagen):
        """
        Aplica una transformación visual al cuadrante de la imagen para ocultación reforzada.

        - Divide la imagen en 4 subimágenes.
        - Invierte colores de cada cuadrante.
        - Reorganiza los cuadrantes de forma invertida.
        """

        imagen = imagen.convert("RGB")

        pixeles = imagen.load()
        ancho, alto = imagen.size

        if ancho % 2 == 1 or alto % 2 == 1:
            ancho_or = ancho
            alt_or= alto
            if ancho % 2 == 1:
                ancho += 1
            if alto % 2 == 1:
                alto += 1
            # Creamos una nueva imagen con anchura par
            imagen_auxiliar= Image.new("RGB", (ancho, alto), (0, 0, 0))
            pixeles_aux = imagen_auxiliar.load()

            # Copiamos los píxeles originales en la nueva imagen, como usamos en el ancho y alto de la imagen original , la liena nueva se mantiene
            for y in range(alt_or):
                for x in range(ancho_or):
                        pixeles_aux[x, y] = pixeles[x, y]
            
            # Actualizar la imagen original y volvemos a cargar los pixeles
            imagen = imagen_auxiliar
            pixeles = imagen.load()  

      
        imagen_np = np.array(imagen)
        h, w = imagen_np.shape[:2]
        h1, w1 = h // 2, w // 2  # Punto medio para dividir en 4 partes

        img1 = imagen_np[0:h1, 0:w1] # Arriba izquierda
        img2 = imagen_np[h1:h, 0:w1] # Abajo izquierda
        img3 = imagen_np[0:h1, w1:w] # Arriba derecha
        img4 = imagen_np[h1:h, w1:w] # Abajo derecha

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

        imagen_modificada_pil = Image.fromarray(imagen_modificada)

        return imagen_modificada_pil

    def _transformar_imagen_inversa(self, imagen):
        """
        Revierte la transformación aplicada en `_transformar_imagen`.

        - Divide según tamaño inversamente.
        - Invierte colores nuevamente.
        - Reubica cuadrantes a su disposición original.
        """
        imagen = imagen.convert("RGB")

        imagen_np = np.array(imagen)
       # Obtener las dimensiones de la imagen
        h, w = imagen_np.shape[:2]
        h1, w1 = h // 2, w // 2 # Punto medio para dividir en 4 partes

        img4 = imagen_np[0:h1, 0:w1] # Arriba izquierda (cambio de posición)
        img3 = imagen_np[0:h1, w1:w] # Arriba derecha (cambio de posición)
        img2 = imagen_np[h1:h, 0:w1] # Abajo izquierda (cambio de posición)
        img1 = imagen_np[h1:h, w1:w] # Abajo derecha (cambio de posición)

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

        imagen_recuperada_pil = Image.fromarray(imagen_recuperada)

        return imagen_recuperada_pil
