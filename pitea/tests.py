import subprocess 
import os

# Ruta del script a probar
SCRIPT_PATH = "script_ejecucion.py"

def test_ocultar_desocultar_lsb():
    # Prueba de ocultar con cifrado AES y LSB
    command = [
        "python3", SCRIPT_PATH, "ocultar",
        "--modo-cifrado", "aes",
        "--modo-cifrado-imagen", "lsb",
        "--modo-cifrado-audio", "lsb",
        "--contraseña", "prueba123",
        "-i", "archivos_prueba/prueba.txt",
        "--input_imagen", "archivos_prueba/imagen.png", 
        "--input_audio" , "archivos_prueba/audio.wav",  
        "-o", "archivos_prueba/audio_salida.wav",
        "-v"
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    assert result.returncode == 0, f"Error en la prueba. Código de salida: {result.returncode}"

    # Prueba de desocultar con cifrado AES y LSB
    command = [
        "python3", SCRIPT_PATH, "desocultar",
        "--modo-cifrado", "aes",
        "--modo-cifrado-imagen", "lsb",
        "--modo-cifrado-audio", "lsb",
        "-i", "archivos_prueba/audio_salida.wav",
        "-o", "archivos_prueba/datos_desocultos.txt",
        "--contraseña", "prueba123",
        "-v"
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )

    assert result.returncode == 0, f"Error en la prueba. Código de salida: {result.returncode}"
    
    # Validar que los archivos sean iguales
    with open("archivos_prueba/prueba.txt", "rb") as file1, open("archivos_prueba/datos_desocultos.txt", "rb") as file2:
        assert file1.read() == file2.read(), "Los archivos no son iguales"

    print("✅ Prueba de ocultar y desocultar completada con éxito : \n El archivo prueba.txt es igual a datos_desocultos.txt \n")
    
    # Eliminar archivos generados
    os.remove("archivos_prueba/datos_desocultos.txt")
    os.remove("archivos_prueba/audio_salida.wav")

def test_ocultar_desocultar_sstv():
    # Prueba de ocultar con cifrado AES y SSTV
    command = [
        "python3", SCRIPT_PATH, "ocultar",
        "--modo-cifrado", "aes",
        "--modo-cifrado-imagen", "text",
        "--modo-cifrado-audio", "sstv",
        "--contraseña", "prueba123",
        "-i", "archivos_prueba/prueba.txt", 
        "-o", "archivos_prueba/sstv.wav",
        "-v"
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    assert result.returncode == 0, f"Error en la prueba. Código de salida: {result.returncode}"

    # Prueba de desocultar con cifrado AES y SSTV
    command = [
        "python3", SCRIPT_PATH, "desocultar",
        "--modo-cifrado", "aes",
        "--modo-cifrado-imagen", "sstv",
        "--modo-cifrado-audio", "sstv",
        "-i", "archivos_prueba/imagen_salida_sstv.png",
        "-o", "archivos_prueba/datos_desocultos.txt",
        "--contraseña", "prueba123",
        "-v"
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )

    assert result.returncode == 0, f"Error en la prueba. Código de salida: {result.returncode}"
    
    # Validar que los archivos sean iguales
    with open("archivos_prueba/prueba.txt", "rb") as file1, open("archivos_prueba/datos_desocultos.txt", "rb") as file2:
        assert file1.read() == file2.read(), "Los archivos no son iguales"

    print("✅ Prueba de ocultar y desocultar completada con éxito : \n El archivo prueba.txt es igual a datos_desocultos.txt \n")
    
    # Eliminar archivos generados
    os.remove("archivos_prueba/datos_desocultos.txt")
    os.remove("archivos_prueba/imagen_salida_sstv.png")
    os.remove("archivos_prueba/sstv.wav")


# Ejecutar los casos de prueba
def run_tests():
        try:
            
            # Ejecutar las pruebas
            print("Ejecutando pruebas... \n")

            print("🧪 Prueba de ocultar y desocultar con cifrado AES y LSB")
            test_ocultar_desocultar_lsb()
            #test_ocultar_desocultar_sstv()

            print(" \n🎉 Todas las pruebas han pasado correctamente. \n")
        except AssertionError as error:
            print("❌ Error en la prueba:", error)
            exit(1)
        except subprocess.CalledProcessError as error:
            print("❌ Error en la prueba:", error.stderr)
            exit(1)
        

if __name__ == "__main__":
    run_tests()
