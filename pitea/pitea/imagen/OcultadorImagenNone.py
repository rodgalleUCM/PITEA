import base64

import numpy as np
from pitea.imagen.OcultadorImagen import OcultadorImagen
from PIL import Image, ImageDraw, ImageFont

from pitea.constantes import ARCHIVO_CONFIG, FORMATO_IMAGEN_OCULTACION ,RUTA_DATOS_OCULTADOR_IMAGEN_TEXT,RUTA_DATOS_CIFRADOS_DESOCULTACION
from pitea.utils import cargar_configuracion
from PIL import Image, ImageFilter
import easyocr
from PIL import ImageEnhance
import pytesseract
class OcultadorImagenNone(OcultadorImagen):
    nombre = "none"
    
    def ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
        raise Exception("El modo Ocultador de imagen None no es valido para ocultacion , solo para desocultacion")

    def desocultar(self):
        with open(self.ruta_txt,'r') as f :
            datos = f.read()
        
        if self.cifrado :
            return base64.b64decode(datos)
        else :
            return datos

    def desocultar_guardar(self):
        datos_extraidos = self.desocultar()

        with open(RUTA_DATOS_CIFRADOS_DESOCULTACION, "wb") as f:
            f.write(datos_extraidos)

        print(f"Datos cifrados guardados en {RUTA_DATOS_CIFRADOS_DESOCULTACION}")
