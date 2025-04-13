from pitea.audio.OcultadorAudio import OcultadorAudio


class OcultadorAudioLSB(OcultadorAudio):
    """Clase que implementa la ocultación de datos en archivos de audio utilizando el método LSB (Least Significant Bit).

    Este método inserta bits de la imagen dentro de los bits menos significativos de las muestras de audio.

    Attributes:
        __nombre (str): Nombre del método de ocultación.
    """


    def __init__(self, ruta_audio):
        """
        Inicializa el objeto con un archivo de audio.

        Args:
            ruta_audio (str): Ruta del archivo de audio en el que se ocultarán/extrarán datos.
        """
        super().__init_(ruta_audio)
        self.__nombre= "lsb"
       


    def _ocultar(self, datos_imagen):
        """Oculta los datos de una imagen dentro de un archivo de audio utilizando el método LSB.

        Args:
            datos_imagen (bytes): Datos binarios de la imagen a ocultar.

        Returns:
            bytearray: Frames del audio con los datos ocultos.

        Raises:
            ValueError: Si la imagen es demasiado grande para ser almacenada en el audio.
            AssertionError: Si el audio no tiene una resolución de 16 bits.
        """
        binarios_imagen = "".join(format(byte, "08b") for byte in datos_imagen)

        # Añadir una cabecera con el tamaño de los datos (32 bits)
        tamano_datos = format(len(binarios_imagen), "032b")
        binarios_imagen = tamano_datos + binarios_imagen  # Cabecera + datos

        assert self.audio.getsampwidth() == 2, "El archivo de audio debe ser de 16 bits"

        frames = bytearray(list(self.audio.readframes(self.audio.getnframes())))

        if len(binarios_imagen) > len(frames) * 8:
            raise ValueError("La imagen es demasiado grande para ser ocultada en este archivo de audio.")

        indice_datos = 0
        for i in range(len(frames)):
            if indice_datos < len(binarios_imagen):
                frames[i] = (frames[i] & 254) | int(binarios_imagen[indice_datos])  # Ocultar el bit menos significativo
                indice_datos += 1

        self.audio.close()

        return frames

    def _desocultar(self):
        """Extrae los datos ocultos del archivo de audio utilizando el método LSB.

        Este método lee los bits menos significativos de los frames de audio y reconstruye los datos ocultos (en este caso, los datos de la imagen).

        Returns:
            bytes: Datos extraídos del archivo de audio.

        Raises:
            ValueError: Si no se puede extraer correctamente el tamaño de los datos ocultos.
        """
        frames = bytearray(list(self.audio.readframes(self.audio.getnframes())))
        self.audio.close()

        datos_binarios = ""
        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)  # Extraer el bit menos significativo
            if len(datos_binarios) >= 32:
                tamano_datos = int(datos_binarios[:32], 2)  # Leer el tamaño de los datos
                datos_binarios = datos_binarios[32:]  # Eliminar la cabecera
                break

        # Verificar que la cabecera tenga el tamaño correcto
        if tamano_datos == 0:
            raise ValueError("No se pudo extraer el tamaño de los datos ocultos.")

        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)  # Extraer el bit menos significativo
            if len(datos_binarios) >= tamano_datos + 32:
                break

        datos_binarios = datos_binarios[32:]

        datos_extraidos = int(datos_binarios, 2).to_bytes(tamano_datos // 8, byteorder="big")

        return datos_extraidos
