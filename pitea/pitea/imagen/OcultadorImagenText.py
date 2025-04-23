import base64
import numpy as np
from pitea.imagen.OcultadorImagen import OcultadorImagen
from PIL import Image, ImageDraw, ImageFont
from constantes import constantes
import easyocr
import pytesseract
from pitea.mensajes import print


class OcultadorImagenText(OcultadorImagen):
    """
    Ocultador de imagen que escribe datos como texto en la imagen.

    Convierte bytes de datos a cadena (base64 si estaba cifrado), ajusta líneas
    y dibuja texto sobre fondo blanco. Usa OCR para recuperar datos en desocultación.

    Atributos:
        nombre (str): Identificador del modo, "text".
    """
    
    nombre = "text"

    def __init__(self, ruta_imagen, modo_cifrador, ruta_txt=None):
        """
        Inicializa el ocultador de texto con la ruta de imagen y modo de cifrado.

        Args:
            ruta_imagen (str): Ignorada en este modo, no se usa imagen base.
            modo_cifrador (str): Indica si datos fueron cifrados ("aes") o no.
            ruta_txt (str, optional): Ruta de texto de entrada para ocultar.
        """
        super().__init__(ruta_imagen, modo_cifrador, ruta_txt)
        

    
    def _ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
        """
        Escribe datos como texto en una imagen.

        - Codifica en base64 si `self._cifrado`.
        - Ajusta longitud de línea según configuración.
        - Dibuja cada línea en fondo blanco.

        Args:
            datos (bytes): Datos brutos.
            altura_imagen (int, optional): Altura deseada; se calcula si None.
            anchura_imagen (int, optional): Anchura deseada; usa texto config si None.

        Returns:
            tuple: (PIL.Image, formato) donde formato es `constantes.FORMATO_IMAGEN_OCULTACION`.

        Raises:
            Exception: Si el texto no cabe en la altura disponible.
        """
        # Codificamos los datos en base64 si están cifrados
        if self._cifrado:
            datos = base64.b64encode(datos).decode('utf-8')
        else:
            datos = datos.decode('utf-8')

        # Guardamos los datos en un archivo de texto
        with open(constantes.RUTA_DATOS_OCULTADOR_IMAGEN_TEXT, 'w') as f:
            f.write(datos)

        print(f"Datos escritos en {constantes.RUTA_DATOS_OCULTADOR_IMAGEN_TEXT}")
        
        # Cargamos la configuración
        tamaño_fuente = constantes.conf['Ajustes_ocultador_imagen_text']["tamanio_fuente"]
        anchura_maxima = constantes.conf['Ajustes_ocultador_imagen_text']["anchura_maxima"]
        ruta_fuente = constantes.conf['Ajustes_ocultador_imagen_text']["ruta_fuente"]
        fuente = ImageFont.truetype(ruta_fuente, tamaño_fuente)
        
        # Definir la anchura máxima de las líneas
        if anchura_imagen is None:
            anchura_imagen = anchura_maxima
        else:
            anchura_maxima = anchura_imagen

        ancho_maximo_linea = anchura_imagen - 20  # Margen lateral de 10 píxeles a cada lado

        # Lista que contendrá las líneas de texto
        lineas_ajustadas = []

        if datos:
            # Comprobar si la palabra es demasiado larga para caber en una línea
            ancho_datos = fuente.getlength(datos)
            if ancho_datos > ancho_maximo_linea:
                # Dividir los datos en fragmentos que quepan en una línea
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

        if altura_imagen is None:
            altura_imagen = altura_necesaria

        # Crear la imagen con las dimensiones calculadas
        imagen = Image.new('RGB', (anchura_imagen, altura_imagen), color='white')
        dibujo = ImageDraw.Draw(imagen)

        # Dibujar el texto en la imagen
        posicion_y = 10  # Margen superior
        for linea in lineas_ajustadas:
            if posicion_y + altura_linea > altura_imagen - 10:  # Detener si excede la altura de la imagen
                raise Exception("No es posible añadir tantos datos a la imagen")
            dibujo.text((10, posicion_y), linea, font=fuente, fill='black')
            posicion_y += altura_linea

        return imagen, constantes.FORMATO_IMAGEN_OCULTACION

    def _desocultar(self):
        """
        Recupera datos de la imagen mediante OCR.

        - Usa EasyOCR con GPU si `gpu` en config.
        - O, Tesseract si no cifrado.
        - Filtra caracteres base64 y decodifica.

        Returns:
            bytes: Datos originales.

        Raises:
            ValueError: Si el texto no es base64 válido.
        """
        # Configurar si se usará la GPU
        gpu = True if constantes.conf['Ajustes_ocultador_imagen_text']["gpu"] == "True" else False

        if self._cifrado:
            # Convertir la imagen a un array de NumPy
            imagen_array = np.array(self._imagen)
    
            # Crear el lector OCR
            reader = easyocr.Reader(['en'], gpu=gpu)  

            # Extraer texto de la imagen
            resultado = reader.readtext(imagen_array, detail=0, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=') 
            texto_extraido = ''.join(resultado)  # Obtener solo el texto
        else:
            texto_extraido = pytesseract.image_to_string(self._imagen, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')

        # Filtrar caracteres válidos en base64
        texto_base64 = ''.join(filter(lambda c: c.isalnum() or c in '+/=', texto_extraido))

        # Decodificar el texto base64 a bytes
        try:
            if self._cifrado:
                datos_decodificados = base64.b64decode(texto_base64)
            else:
                datos_decodificados = texto_base64.encode()
            print("Datos decodificados exitosamente")
            return datos_decodificados
        except base64.binascii.Error:
            raise ValueError("El texto extraído no es una cadena válida de base64")
