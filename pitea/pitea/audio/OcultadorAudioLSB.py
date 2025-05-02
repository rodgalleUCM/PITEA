from pitea.audio.OcultadorAudio import OcultadorAudio
from constantes import constantes


class OcultadorAudioLSB(OcultadorAudio):
    """
    Ocultador de audio que utiliza LSB (Least Significant Bit).

    Inserta bits de datos de la imagen en cada byte de los frames de audio,
    precedidos por una cabecera de 32 bits que indica la longitud de los datos.

    Atributos:
        nombre (str): Identificador del modo, "lsb".
    """

    nombre= "lsb"

    def __init__(self, ruta_audio):
        """
        Inicializa el LSB en audio WAV.

        Args:
            ruta_audio (str): Ruta al archivo WAV contenedor.

        Raises:
            ValueError: Si el archivo no es de 16 bits o no se puede abrir.
        """
        super().__init__(ruta_audio)
        
       


    def _ocultar(self, datos_imagen):
        """
        Inserta datos binarios en los frames de audio.

        Args:
            datos_imagen (bytes): Datos de la imagen a ocultar.

        Returns:
            bytearray: Frames con bits embebidos en LSB.

        Raises:
            AssertionError: Si el audio no es de 16 bits por muestra.
            ValueError: Si la imagen excede la capacidad de audio.
        """
        binarios_imagen = "".join(format(byte, "08b") for byte in datos_imagen)

        # Añadir una cabecera con el tamaño de los datos (32 bits)
        tamano_datos = format(len(binarios_imagen), "0"+str(constantes._TAMAÑO_CABECERA_LSB)+"b")
        binarios_imagen = tamano_datos + binarios_imagen  # Cabecera + datos

        assert self._audio.getsampwidth() == 2, "El archivo de audio debe ser de 16 bits"

        frames = bytearray(list(self.
        _audio.readframes(self._audio.getnframes())))

        if len(binarios_imagen) > len(frames):
            raise ValueError("La imagen es demasiado grande para ser ocultada en este archivo de audio.")

        indice_datos = 0
        for i in range(len(frames)):
            if indice_datos < len(binarios_imagen):
                frames[i] = (frames[i] & 254) | int(binarios_imagen[indice_datos])  # Ocultar el bit menos significativo
                indice_datos += 1

        self._audio.close()

        return frames

    def _desocultar(self):
        """
        Recupera datos embebidos de los frames de audio.

        Devuelve los bytes de imagen extraídos.

        Returns:
            bytes: Datos de la imagen oculta.

        Raises:
            ValueError: Si la cabecera indica longitud cero o inválida.
        """
        frames = bytearray(list(self._audio.readframes(self._audio.getnframes())))
        self._audio.close()

        datos_binarios = ""
        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)  # Extraer el bit menos significativo
            if len(datos_binarios) >= constantes._TAMAÑO_CABECERA_LSB:
                tamano_datos = int(datos_binarios[:constantes._TAMAÑO_CABECERA_LSB], 2)  # Leer el tamaño de los datos
                datos_binarios = datos_binarios[constantes._TAMAÑO_CABECERA_LSB:]  # Eliminar la cabecera
                break

        # Verificar que la cabecera tenga el tamaño correcto
        if tamano_datos == 0:
            raise ValueError("No se pudo extraer el tamaño de los datos ocultos.")

        for i in range(len(frames)):
            datos_binarios += str(frames[i] & 1)  # Extraer el bit menos significativo
            if len(datos_binarios) >= tamano_datos + constantes._TAMAÑO_CABECERA_LSB:
                break

        datos_binarios = datos_binarios[constantes._TAMAÑO_CABECERA_LSB:]

        datos_extraidos = int(datos_binarios, 2).to_bytes(tamano_datos // 8, byteorder="big")

        return datos_extraidos
