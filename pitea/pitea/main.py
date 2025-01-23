from pitea.mensajes import *
from pitea.cifradores.cifradorfactory import CifradorFactory
from pitea.imagen.imagenfactory import OcultadorImagenFactory
from pitea.audio.audiofactory import OcultadorAudioFactory
from pitea.utils import crear_cache
import builtins 

def flujo_de_trabajo_ocultar(modo_cifrado,modo_cifrado_imagen, modo_cifrado_audio, input, output, contraseña, formato_salida) :

    print("Creando estructura de la cache")
    crear_cache(constantes.LISTA_DIR_CACHE_OCULTACION)

    # Renombramiento de variables
    archivo_entrada_texto = input[0]
    archivo_entrada_imagen = input[1]
    archivo_entrada_audio = input[2] if len(input) == 3 else None

    archivo_salida_audio = output[0]

    print(MENSAJE_INICIO_FLUJO % "ocultación")

    print("Creando cifrador...")
    cifrador= CifradorFactory.get_builder(modo_cifrado,contraseña,None)

    print("Cifrador creado , cifrando datos ...")
    datos_cifrados = cifrador.cifrar_guardar(archivo_entrada_texto)

    print(f"Creando ocultador en imagenes ...")
    ocultador_imagen = OcultadorImagenFactory.get_builder(modo_cifrado_imagen,archivo_entrada_imagen)

    print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
    imagen_contenedora,formato = ocultador_imagen.ocultar_guardar()

    print(f"Creando ocultador en audio ...")
    ocultador_audio = OcultadorAudioFactory.get_builder(modo_cifrado_audio,archivo_entrada_audio)

    print("Ocultador en audio  creado, ocultando imagen en audio ...")
    ocultador_audio.ocultar_guardar(formato,archivo_salida_audio)

    print("Proceso realizado")


def flujo_de_trabajo_desocultar(modo_cifrado, modo_cifrado_imagen,modo_cifrado_audio, input, output, contraseña) :

    print("Creando estructura de la cache")
    crear_cache(constantes.LISTA_DIR_CACHE_DESOCULTACION)

    print(MENSAJE_INICIO_FLUJO % "desocultación")
    
    print(f"Creando ocultador en audio ...")
    ocultador_audio = OcultadorAudioFactory.get_builder(modo_cifrado_audio,input)

    print("Ocultador en audio  creado, ocultando imagen en audio ...")
    ocultador_audio.desocultar_guardar()

    print(f"Creando ocultador en imagenes ...")
    ocultador_imagen = OcultadorImagenFactory.get_builder(modo_cifrado_imagen,str(constantes.RUTA_IMAGEN_DESOCULTACION) % "png")

    print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
    ocultador_imagen.desocultar_guardar()

    print("Creando cifrador...")
    cifrador= CifradorFactory.get_builder(modo_cifrado,contraseña,output)

    print("Cifrador creado, cifrando datos ...")
    cifrador.descifrar_guardar()