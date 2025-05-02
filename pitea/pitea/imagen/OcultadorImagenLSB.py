from pitea.imagen.OcultadorImagen import OcultadorImagen
from constantes import constantes


class OcultadorImagenLSB(OcultadorImagen):
    """
    Ocultador de imagen que emplea LSB en componentes RGB.

    Este método inserta los bits de datos en el bit menos significativo de cada canal RGB,
    precedidos por una cabecera de 32 bits que indica el tamaño del mensaje.

    Atributos:
        nombre (str): Identificador del modo, "lsb".
    """
    nombre = "lsb"

    def __init__(self, ruta_imagen, modo_cifrador, ruta_txt=None):
        """
        Inicializa el ocultador LSB con la imagen contenedora y modo de cifrado.

        Args:
            ruta_imagen (str): Ruta al archivo de imagen donde se ocultarán datos.
            modo_cifrador (str): Tipo de cifrado aplicado previamente ('aes' o 'none').
            ruta_txt (str, optional): Ruta a archivo de texto si se emplease (no usado aquí).
        """
        super().__init__(ruta_imagen, modo_cifrador, ruta_txt)
        

    def _ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
        """
        Inserta datos binarios en la imagen usando LSB.

        Convierte el contenido cifrado en una cadena de bits, prepende
        una cabecera de 32 bits con la longitud, y escribe cada bit en el
        bit menos significativo de los canales RGB.

        Args:
            datos (bytes): Datos cifrados a ocultar.
            altura_imagen (int, optional): Altura deseada; no usado en LSB.
            anchura_imagen (int, optional): Anchura deseada; no usado en LSB.

        Returns:
            tuple: (imagen_modificada, formato_str).

        Raises:
            ValueError: Si la imagen no tiene suficiente capacidad para todos los bits.
        """
        datos_binarios = "".join(
            format(byte, "08b") for byte in datos
        )  # Convertir los datos a binarios del archivo cifrado

        pixeles = self._imagen.load()
        ancho, alto = self._imagen.size

        # Comprobar si tiene canal alfa
        if self._imagen.mode == "RGBA":
            for y in range(alto):
                for x in range(ancho):
                    r, g, b, a = pixeles[x, y]
                    if a == 0:
                        # Poner píxel completamente transparente en negro
                        pixeles[x, y] = (0, 0, 0, 255)

        

        # Añadir una cabecera con el tamaño de los datos (32 bits)
        tamano_datos_binarios = format(len(datos_binarios),  "0"+str(constantes._TAMAÑO_CABECERA_LSB)+"b")

        # Cabecera + Datos
        mensaje = tamano_datos_binarios + datos_binarios

        longitud_mensaje = len(mensaje)

        # Comprobar si la imagen tiene suficiente espacio para almacenar los datos
        if longitud_mensaje > ancho * alto * 3:
            raise ValueError(
                "La imagen no tiene suficiente espacio para almacenar todos los datos."
            )

        indice_datos = 0
        for y in range(alto):  # Iterar sobre los píxeles de la imagen
            for x in range(ancho):
                pixel = list(pixeles[x, y])  # Obtener el valor de los píxeles
                for canal in range(3):  # Iterar sobre los canales de color (RGB)
                    if (
                        indice_datos < longitud_mensaje
                    ):  # Si todavía hay datos para ocultar
                        pixel[canal] = (pixel[canal] & ~1) | int(
                            mensaje[indice_datos]
                        )  # Ocultar el bit menos significativo
                        indice_datos += 1
                pixeles[x, y] = tuple(pixel)  # Actualizar el valor de los píxeles
                if (
                    indice_datos >= longitud_mensaje
                ):  # Si ya se han ocultado todos los datos
                    break
            if indice_datos >= longitud_mensaje:
                break

        return self._imagen, self._formato

    def _desocultar(self):
        """
        Extrae datos escondidos en la imagen mediante LSB.

        Lee primero la cabecera de 32 bits para saber la longitud,
        luego recupera esa cantidad de bits y los convierte a bytes.

        Returns:
            bytes: Datos extraídos.

        Raises:
            ValueError: Si la cabecera no indica ningún dato válido.
        """
        pixeles = self._imagen.load()
        ancho, alto = self._imagen.size
        datos_binarios = ""
        tamano_datos = 0

        for y in range(alto):
            for x in range(ancho):
                pixel = list(pixeles[x, y])
                for canal in range(3):
                    datos_binarios += str(
                        pixel[canal] & 1
                    )  # Extraer el bit menos significativo
                    if len(datos_binarios) >= constantes._TAMAÑO_CABECERA_LSB:
                        tamano_datos = int(
                            datos_binarios[:constantes._TAMAÑO_CABECERA_LSB], 2
                        )  # Leer el tamaño de los datos
                        datos_binarios = datos_binarios[constantes._TAMAÑO_CABECERA_LSB:]  # Eliminar la cabecera

                        # Si el tamaño de los datos es mayor que 0, seguimos extrayendo los datos
                        if tamano_datos > 0:
                            break
                if tamano_datos > 0:
                    break
            if tamano_datos > 0:
                break

        if tamano_datos == 0:
            raise ValueError("No se pudo extraer el tamaño de los datos ocultos.")

        while len(datos_binarios) < tamano_datos + constantes._TAMAÑO_CABECERA_LSB:
            for y in range(alto):
                for x in range(ancho):
                    pixel = list(pixeles[x, y])
                    for canal in range(3):
                        datos_binarios += str(pixel[canal] & 1)
                        if len(datos_binarios) >= tamano_datos + constantes._TAMAÑO_CABECERA_LSB:
                            break
                    if len(datos_binarios) >= tamano_datos + constantes._TAMAÑO_CABECERA_LSB:
                        break
                if len(datos_binarios) >= tamano_datos + constantes._TAMAÑO_CABECERA_LSB:
                    break

        # Convertir los datos binarios en bytes
        datos_binarios = datos_binarios[constantes._TAMAÑO_CABECERA_LSB:]  # Eliminar la cabecera
        datos_extraidos = int(datos_binarios, 2).to_bytes(
            tamano_datos // 8, byteorder="big"
        )

        return datos_extraidos
