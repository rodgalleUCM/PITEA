from pitea.mensajes import *
from pitea.cifradores.factory import CifradorFactory
from pitea.imagen.factory import OcultadorImagenFactory
from pitea.audio.factory import OcultadorAudioFactory

def flujo_de_trabajo_ocultar(modo_cifrado,modo_cifrado_imagen, modo_cifrado_audio, input, output, contraseña, formato_salida) :
    # Renombramiento de variables
    archivo_entrada_texto = input[0]
    archivo_entrada_imagen = input[1]
    archivo_entrada_audio = input[2] if len(input) == 3 else None

    archivo_salida_audio = output[0]

    print(MENSAJE_INICIO_FLUJO % "ocultación")

    print("Creando cifrador...")
    cifrador= CifradorFactory.get_builder(modo_cifrado,contraseña)

    print("Cifrador creado , cifrando datos ...")
    datos_cifrados = cifrador.cifrar(archivo_entrada_texto)

    print(f"Creando ocultador en imagenes ...")
    ocultador_imagen = OcultadorImagenFactory.get_builder(modo_cifrado_imagen,archivo_entrada_imagen)

    print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
    imagen_contenedora,formato = ocultador_imagen.ocultar()

    print(f"Creando ocultador en audio ...")
    ocultador_audio = OcultadorAudioFactory.get_builder(modo_cifrado_audio,archivo_entrada_audio)

    print("Ocultador en audio  creado, ocultando imagen en audio ...")
    ocultador_audio.ocultar(formato,archivo_salida_audio)

    print("Proceso realizado")


def flujo_de_trabajo_desocultar(modo_cifrado, modo_cifrado_imagen,modo_cifrado_audio, input, output, contraseña, formato_salida) :
    # Renombramiento de variables
    archivo_entrada_texto = input[0]
    archivo_entrada_imagen = input[1]
    archivo_entrada_audio = input[2] if len(input) == 3 else None

    archivo_salida_audio = output[0]
    archivo_salida_imagen = output[1] if len(output) == 2 else None

    print(MENSAJE_INICIO_FLUJO % "desocultación")
    
    print(f"Creando ocultador en audio ...")
    ocultador_audio = OcultadorAudioFactory.get_builder(modo_cifrado_audio,archivo_entrada_audio)

    print("Ocultador en audio  creado, ocultando imagen en audio ...")
    ocultador_audio.desocultar()

    print(f"Creando ocultador en imagenes ...")
    ocultador_imagen = OcultadorImagenFactory.get_builder(modo_cifrado_imagen,)

    print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
    imagen_contenedora = ocultador_imagen.desocultar()

    print("Creando cifrador...")
    cifrador= CifradorFactory.get_builder(modo_cifrado,contraseña)

    print("Cifrador creado, cifrando datos ...")
    datos_cifrados = cifrador.descifrar()