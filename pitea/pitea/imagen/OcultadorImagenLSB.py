from pitea.imagen.OcultadorImagen import OcultadorImagen


class OcultadorImagenLSB(OcultadorImagen):
    nombre = "lsb"

    def ocultar(self, datos, altura_imagen= None, anchura_imagen=None):
        datos_binarios = "".join(
            format(byte, "08b") for byte in datos
        )  # Convertir los datos a binarios del archivo cifrado

        # Añadir una cabecera con el tamaño de los datos (32 bits)
        tamano_datos_binarios = format(len(datos_binarios), "032b")

        # Cabecera + Datos
        mensaje = tamano_datos_binarios + datos_binarios

        longitud_mensaje = len(mensaje)

        # Comprobar si la imagen tiene suficiente espacio para almacenar los datos
        if longitud_mensaje > self.ancho * self.alto * 3:
            raise ValueError(
                "La imagen no tiene suficiente espacio para almacenar todos los datos."
            )

        indice_datos = 0
        for y in range(self.alto):  # Iterar sobre los píxeles de la imagen
            for x in range(self.ancho):
                pixel = list(self.pixeles[x, y])  # Obtener el valor de los píxeles
                for canal in range(3):  # Iterar sobre los canales de color (RGB)
                    if (
                        indice_datos < longitud_mensaje
                    ):  # Si todavía hay datos para ocultar
                        pixel[canal] = (pixel[canal] & ~1) | int(
                            mensaje[indice_datos]
                        )  # Ocultar el bit menos significativo
                        indice_datos += 1
                self.pixeles[x, y] = tuple(pixel)  # Actualizar el valor de los píxeles
                if (
                    indice_datos >= longitud_mensaje
                ):  # Si ya se han ocultado todos los datos
                    break
            if indice_datos >= longitud_mensaje:
                break

        return self.imagen, self.formato

    def desocultar(self):
        datos_binarios = ""
        tamano_datos = 0

        for y in range(self.alto):
            for x in range(self.ancho):
                pixel = list(self.pixeles[x, y])
                for canal in range(3):
                    datos_binarios += str(
                        pixel[canal] & 1
                    )  # Extraer el bit menos significativo
                    if len(datos_binarios) >= 32:
                        tamano_datos = int(
                            datos_binarios[:32], 2
                        )  # Leer el tamaño de los datos
                        datos_binarios = datos_binarios[32:]  # Eliminar la cabecera

                        # Si el tamaño de los datos es mayor que 0, seguimos extrayendo los datos
                        if tamano_datos > 0:
                            break
                if tamano_datos > 0:
                    break
            if tamano_datos > 0:
                break

        if tamano_datos == 0:
            raise ValueError("No se pudo extraer el tamaño de los datos ocultos.")

        while len(datos_binarios) < tamano_datos + 32:
            for y in range(self.alto):
                for x in range(self.ancho):
                    pixel = list(self.pixeles[x, y])
                    for canal in range(3):
                        datos_binarios += str(pixel[canal] & 1)
                        if len(datos_binarios) >= tamano_datos + 32:
                            break
                    if len(datos_binarios) >= tamano_datos + 32:
                        break
                if len(datos_binarios) >= tamano_datos + 32:
                    break

        # Convertir los datos binarios en bytes
        datos_binarios = datos_binarios[32:]  # Eliminar la cabecera
        datos_extraidos = int(datos_binarios, 2).to_bytes(
            tamano_datos // 8, byteorder="big"
        )

        return datos_extraidos
