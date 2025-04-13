from abc import ABC, abstractmethod
from PIL import Image
from constantes import constantes
import cv2
import numpy as np
from pitea.mensajes import print


class OcultadorImagen(ABC):
    """
    Clase abstracta para los ocultadores de imagen que proporcionan métodos para ocultar y desocultar datos en imágenes.

    Atributos:
        nombre (str): Nombre del tipo de ocultador de imagen, utilizado para distinguir entre ocultadores en la factoria.
        formato (str): Formato de la imagen cargada.
        imagen (PIL.Image): Objeto imagen cargado.
        cifrado (int): Indicador de si se aplica cifrado (1 si se aplica, 0 si no).
        ruta_txt (str, optional): Ruta al archivo de texto (si aplica).
    
    Métodos:
        __init__(self, ruta_imagen, modo_cifrador, ruta_txt=None):
            Inicializa el ocultador de imagen con la ruta de la imagen y el modo de cifrado.
        
        _ocultar(self, datos_imagen, altura_imagen=None, anchura_imagen=None):
            Método abstracto que debe implementarse en las subclases para ocultar los datos en la imagen.
        
        _desocultar(self):
            Método abstracto que debe implementarse en las subclases para extraer los datos ocultos en la imagen.

        ocultar_guardar(self, altura_imagen=None, anchura_imagen=None):
            Oculta los datos en la imagen y guarda la imagen transformada en el formato adecuado.

        desocultar_guardar(self):
            Extrae los datos ocultos de la imagen y guarda los datos extraídos en un archivo.

        _transformar_imagen(self, imagen):
            Aplica transformaciones a la imagen para ocultar los datos de manera no obvia.

        _transformar_imagen_inversa(self, imagen):
            Restaura la imagen transformada a su estado original para facilitar la desocultación.
    """
    
    
    def __init__(self, ruta_imagen, modo_cifrador, ruta_txt=None):
        """
        Inicializa el ocultador de imagen con la ruta de la imagen y el modo de cifrado.

        Args:
            ruta_imagen (str): Ruta del archivo de imagen que contiene los datos.
            modo_cifrador (str): Modo de cifrado para aplicar.
            ruta_txt (str, optional): Ruta a un archivo de texto si se utiliza para ocultar datos en la imagen. Por defecto es None.
        """
        self.__nombre = ""
        if ruta_imagen:
            self._formato = ruta_imagen.split(".")[-1]
            self._imagen = Image.open(ruta_imagen)
        else:
            self._ruta_txt = ruta_txt
        self._cifrado = 1 if modo_cifrador not in ["none"] else 0

    @property
    def nombre(self) :
        return self.__nombre

    @abstractmethod
    def _ocultar(self, datos_imagen, altura_imagen=None, anchura_imagen=None):
        """Método abstracto para ocultar los datos en la imagen.

        Args:
            datos_imagen (bytes): Datos que se desean ocultar en la imagen.
            altura_imagen (int, optional): Altura de la imagen modificada (si es necesario). Por defecto es None.
            anchura_imagen (int, optional): Anchura de la imagen modificada (si es necesario). Por defecto es None.

        Returns:
            PIL.Image: Imagen con los datos ocultos.
            str: Formato de la imagen.
        """
        pass

    @abstractmethod
    def _desocultar(self):
        """Método abstracto para extraer los datos ocultos de la imagen.

        Returns:
            bytes: Datos extraídos de la imagen.
        """
        pass

    def ocultar_guardar(self, altura_imagen=None, anchura_imagen=None):
        """Oculta los datos en la imagen y guarda la imagen transformada.

        Args:
            altura_imagen (int, optional): Altura de la imagen modificada. Por defecto es None.
            anchura_imagen (int, optional): Anchura de la imagen modificada. Por defecto es None.

        Returns:
            PIL.Image: Imagen con los datos ocultos.
            str: Formato de la imagen.
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
        """Extrae los datos ocultos de la imagen y guarda los datos extraídos.

        Returns:
            None
        """
        self._imagen = self._transformar_imagen_inversa(self._imagen)
        self._imagen.save(str(constantes.RUTA_IMAGEN_CONTENEDORA_DESOCULTACION_DESTRANSFORMADA) % self._formato)
        datos_extraidos = self._desocultar()

        with open(constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION, "wb") as f:
            f.write(datos_extraidos)

        print(f"Datos cifrados guardados en {constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION}")

    def _transformar_imagen(self, imagen):
        """Aplica transformaciones a la imagen para ocultar los datos de manera no obvia.

        Args:
            imagen (PIL.Image): Imagen que será transformada.

        Returns:
            PIL.Image: Imagen transformada con los datos ocultos.
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

    def __transformar_imagen_inversa(self, imagen):
        """Restaura la imagen transformada a su estado original para facilitar la desocultación.

        Args:
            imagen (PIL.Image): Imagen que será restaurada.

        Returns:
            PIL.Image: Imagen restaurada a su estado original.
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
