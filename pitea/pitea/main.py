from pitea.mensajes import MENSAJE_INICIO_FLUJO, print
from pitea.cifradores.cifradorfactory import CifradorFactory
from pitea.imagen.imagenfactory import OcultadorImagenFactory
from pitea.audio.audiofactory import OcultadorAudioFactory
from pitea.constantes import ARCHIVO_CONFIG, LISTA_DIR_CACHE_DESOCULTACION, LISTA_DIR_CACHE_OCULTACION, MODES_SSTV, RUTA_IMAGEN_DESOCULTACION
from pitea.utils import cargar_configuracion, crear_cache


def flujo_de_trabajo_ocultar(
    modo_cifrado,
    modo_cifrado_imagen,
    modo_cifrado_audio,
    input,
    input_imagen,
    input_audio,
    output,
    contraseña,
):
    print("Creando estructura de la cache")
    crear_cache(LISTA_DIR_CACHE_OCULTACION)


    print(MENSAJE_INICIO_FLUJO % "ocultación")

    print("Creando cifrador...")
    cifrador = CifradorFactory.get_builder(modo_cifrado, contraseña, None)

    print("Cifrador creado , cifrando datos ...")
    cifrador.cifrar_guardar(input)

    print("Creando ocultador en imagenes ...")
    ocultador_imagen = OcultadorImagenFactory.get_builder(
        modo_cifrado_imagen, input_imagen
    )

    print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
    if modo_cifrado_audio not in ["sstv"] :
        imagen_contenedora, formato = ocultador_imagen.ocultar_guardar()
    else :
        conf = cargar_configuracion(ARCHIVO_CONFIG)
        modo_sstv = conf["modo_sstv"]
        anchura = MODES_SSTV[modo_sstv][1][0]
        altura = MODES_SSTV[modo_sstv][1][1]
        imagen_contenedora, formato = ocultador_imagen.ocultar_guardar(altura,anchura)

    print("Creando ocultador en audio ...")
    ocultador_audio = OcultadorAudioFactory.get_builder(
        modo_cifrado_audio, input_audio
    )

    print("Ocultador en audio  creado, ocultando imagen en audio ...")
    ocultador_audio.ocultar_guardar(formato, output)

    print("Proceso realizado")


def flujo_de_trabajo_desocultar(
    modo_cifrado, modo_cifrado_imagen, modo_cifrado_audio, input_audio,input_imagen, output, contraseña
):
    print("Creando estructura de la cache")
    crear_cache(LISTA_DIR_CACHE_DESOCULTACION)

    print(MENSAJE_INICIO_FLUJO % "desocultación")

    #Opcion de pasar el sstv ya decodificado como imagen
    if input_audio :
        print("Creando ocultador en audio ...")
        ocultador_audio = OcultadorAudioFactory.get_builder(modo_cifrado_audio, input_audio)

        print("Ocultador en audio  creado, ocultando imagen en audio ...")
        ocultador_audio.desocultar_guardar()

    if not input_imagen : 
        print("Creando ocultador en imagenes ...")
        ocultador_imagen = OcultadorImagenFactory.get_builder(
            modo_cifrado_imagen, str(RUTA_IMAGEN_DESOCULTACION) % "png"
        )

        print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
        ocultador_imagen.desocultar_guardar()
    else :
        print("Creando ocultador en imagenes ...")
        ocultador_imagen = OcultadorImagenFactory.get_builder(
            modo_cifrado_imagen, input_imagen
        )

        print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
        ocultador_imagen.desocultar_guardar()

    print("Creando cifrador...")
    cifrador = CifradorFactory.get_builder(modo_cifrado, contraseña, output)

    print("Cifrador creado, cifrando datos ...")
    cifrador.descifrar_guardar()
