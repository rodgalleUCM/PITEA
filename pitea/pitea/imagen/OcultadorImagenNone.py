import base64

from pitea.imagen.OcultadorImagen import OcultadorImagen

from pitea.constantes import RUTA_DATOS_CIFRADOS_DESOCULTACION
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
