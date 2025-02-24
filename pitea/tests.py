import subprocess 
import os
import tempfile
from PIL import Image
from pitea.imagen.OcultadorImagenLSB import OcultadorImagenLSB

# Ruta del script principal
SCRIPT_PATH = "script_ejecucion.py"

def ejecutar_comando(command):
    stdout_temp_path = "SalidaPitea.log"
    stderr_temp_path = "ErroresPitea.log"
    
    with open(stdout_temp_path, 'w') as stdout_temp, open(stderr_temp_path, 'w') as stderr_temp:
        result = subprocess.run(
            command,
            stdout=stdout_temp,
            stderr=stderr_temp,
            text=True,
            check=True
        )
    
    print(f"Se ha guardado stdout en: {stdout_temp_path}")
    print(f"Se ha guardado stderr en: {stderr_temp_path}")
    return result

def  test_transformada():
    # Test de transformaciones sin ocultar datos
    ruta_imagen_prueba = "archivos_prueba/imagen_salida_sstv.png"
    imagen_original = Image.open(ruta_imagen_prueba)
    # Crear instancia de OcultadorImagen
    ocultador = OcultadorImagenLSB(ruta_imagen_prueba, modo_cifrador="none")
    # Transformar la imagen
    imagen_transformada = ocultador.transformar_imagen(imagen_original)
    # Invertir la transformación
    imagen_revertida = ocultador.transformar_imagen_inversa(imagen_transformada)
    # Comparar píxeles para verificar reversibilidad completa
    assert list(imagen_original.getdata()) == list(imagen_revertida.getdata()), " Las transformaciones no son reversibles."
    print("✅ Prueba de transformación completamente reversible, completada con éxito \n")

def test_ocultar_desocultar_lsb():
    command = [
        "python3", SCRIPT_PATH, "ocultar",
        "--modo-cifrado", "aes",
        "--modo-cifrado-imagen", "lsb",
        "--modo-cifrado-audio", "lsb",
        "--contraseña", "prueba123",
        "-i", "archivos_prueba/prueba.txt",
        "--input_imagen", "archivos_prueba/imagen.png", 
        "--input_audio", "archivos_prueba/audio.wav",  
        "-o", "archivos_prueba/audio_salida.wav",
        "-v"
    ]
    ejecutar_comando(command)

    command = [
        "python3", SCRIPT_PATH, "desocultar",
        "--modo-cifrado", "aes",
        "--modo-cifrado-imagen", "lsb",
        "--modo-cifrado-audio", "lsb",
        "--input_audio", "archivos_prueba/audio_salida.wav",
        "-o", "archivos_prueba/datos_desocultos.txt",
        "--contraseña", "prueba123",
        "-v"
    ]
    ejecutar_comando(command)
    
    with open("archivos_prueba/prueba.txt", "rb") as file1, open("archivos_prueba/datos_desocultos.txt", "rb") as file2:
        assert file1.read() == file2.read(), "Los archivos no son iguales"
    
    print("✅ Prueba de ocultar y desocultar completada con éxito")
    os.remove("archivos_prueba/datos_desocultos.txt")
    os.remove("archivos_prueba/audio_salida.wav")

#def test_ocultar_desocultar_sstv():
    
# Ejecutar los casos de prueba
def run_tests():
        try:
            
            # Ejecutar las pruebas
            print("Ejecutando pruebas... \n")

            print("🧪 Prueba de ocultar y desocultar con cifrado AES y LSB")
            test_ocultar_desocultar_lsb()
            test_transformada()
            

            print(" \n🎉 Todas las pruebas han pasado correctamente. \n")
        except AssertionError as error:
            print("❌ Error en la prueba:", error)
            exit(1)
        except subprocess.CalledProcessError as error:
            print("❌ Error en subproceso:", error)
            exit(1)
        

if __name__ == "__main__":
    run_tests()
