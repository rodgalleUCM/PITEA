from pitea.mensajes import *
from pitea.cifradores.factory import CifradorFactory

def flujo_de_trabajo_ocultar(modo_cifrado, modo_cifrado_audio, input, output, contraseña, formato_salida) :
    # Renombramiento de variables
    archivo_entrada_texto = input[0]
    archivo_entrada_imagen = input[1]
    archivo_entrada_audio = input[2] if len(input) == 3 else None

    archivo_salida_audio = output[0]
    archivo_salida_imagen = output[1] if len(output) == 2 else None

    print(MENSAJE_INICIO_FLUJO % "ocultación")

    print("Creando cifrador...")
    cifrador_builder = CifradorFactory.get_builder(modo_cifrado,contraseña)

    print("Cifrador creado , cifrando texto ...")
    cifrador_builder.cifrar(archivo_entrada_texto)


    



def flujo_de_trabajo_desocultar(modo_cifrado, modo_cifrado_audio, input, output, contraseña, formato_salida) :
    print(MENSAJE_INICIO_FLUJO % "desocultación")
    