import base64
from pitea.imagen.OcultadorImagen import OcultadorImagen
from PIL import Image, ImageDraw, ImageFont

from pitea.constantes import ARCHIVO_CONFIG, FORMATO_IMAGEN_OCULTACION
from pitea.utils import cargar_configuracion
from PIL import Image, ImageFilter
import pytesseract

class OcultadorImagenText(OcultadorImagen):
    nombre = "text"
    
    def ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
        #Codificamos los datos en base64 ya que al estar cifrados hay caracteres no operbales o representables como str
        datos = base64.b64encode(datos).decode('utf-8')
        print(datos)
       
        conf = cargar_configuracion(ARCHIVO_CONFIG)
        tamaño_fuente = conf["tamanio_fuente"]
        fuente = ImageFont.truetype("DejaVuSans.ttf", tamaño_fuente)
        anchura_maxima = conf["anchura_maxima"]

        # Definir anchura máxima si no se ha proporcionado
        if anchura_imagen is None:
            anchura_imagen = anchura_maxima
        else:
            anchura_maxima = anchura_imagen

        ancho_maximo_linea = anchura_imagen - 20  # Margen lateral de 10 píxeles a cada lado

        # Lista que contiene las lineas a dibujar
        lineas_ajustadas = []

        if datos:
            # Comprobar si la palabra es demasiado larga para caber en una línea
            ancho_datos = fuente.getlength(datos)
            if ancho_datos > ancho_maximo_linea:
                # Dividir la datos en fragmentos que quepan en la línea
                fragmento = ""
                for caracter in datos:
                    fragmento_prueba = fragmento + caracter
                    ancho_fragmento = fuente.getlength(fragmento_prueba)
                    if ancho_fragmento > ancho_maximo_linea:
                        lineas_ajustadas.append(fragmento)
                        fragmento = caracter
                    else:
                        fragmento = fragmento_prueba
                if fragmento:
                    lineas_ajustadas.append(fragmento)
            else:
                lineas_ajustadas.append(datos)

        # Calcular la altura necesaria si no se ha proporcionado
        altura_linea = tamaño_fuente + 5  # Altura de línea con margen
        altura_necesaria = (altura_linea * len(lineas_ajustadas)) + 20  # Espacio adicional para márgenes

        if altura_imagen is None :
            altura_imagen = altura_necesaria

        # Crear la imagen con las dimensiones calculadas
        imagen = Image.new('RGB', (anchura_imagen, altura_imagen), color='white')
        dibujo = ImageDraw.Draw(imagen)

        # Dibujar el texto en la imagen
        posicion_y = 10  # Margen superior
        for linea in lineas_ajustadas:
            if posicion_y + altura_linea > altura_imagen - 10:  # Detener si excede la altura de la imagen
                raise Exception("No es posible añadir tanto datos a la imagen")
            dibujo.text((10, posicion_y), linea, font=fuente, fill='black')
            posicion_y += altura_linea


        return imagen, FORMATO_IMAGEN_OCULTACION



    def desocultar(self):

        #Extraer el texto oculto en formato base64
        texto_base64 = pytesseract.image_to_string(self.imagen, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')

        
        # Eliminar caracteres que no sean válidos en base64
        texto_base64 = ''.join(filter(lambda c: c.isalnum() or c in '+/=', texto_base64))

        print(texto_base64)
        print("WWWWWWWWWWWWWWWWWWWWWWWWWW")

        # Fase 3: Decodificar el texto base64 a bytes
        try:
            datos_decodificados = base64.b64decode(texto_base64)
            print("Datos decodificados exitosamente")
            print(datos_decodificados)
        except base64.binascii.Error:
            raise ValueError("El texto extraído no es una cadena válida de base64")

        # Fase 4: Retornar los datos decodificados en bytes
        return datos_decodificados
