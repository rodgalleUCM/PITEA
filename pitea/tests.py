import subprocess 
import os

# Ruta del script a probar
SCRIPT_PATH = "script_ejecucion.py"

# Casos de prueba: cada uno es un conjunto de argumentos para el script
TEST_CASES = [
    {
        "description": "Prueba básica de ocultar con cifrado AES y LSB",
        "command": [
            "python3", SCRIPT_PATH, "ocultar",
            "--modo-cifrado", "aes",
            "--modo-cifrado-imagen", "lsb",
            "--modo-cifrado-audio", "lsb",
            "--contraseña", "prueba123",
            "-i", "archivos_prueba/prueba.txt archivos_prueba/imagen.png archivos_prueba/audio.wav",  
            "-o", "archivos_prueba/audio_salida.wav",
        ]
    },
    {
        "description": "Prueba de desocultar con cifrado AES y LSB",
        "command": [
            "python3", SCRIPT_PATH, "desocultar",
            "--modo-cifrado", "aes",
            "--modo-cifrado-imagen", "lsb",
            "--modo-cifrado-audio", "lsb",
            "--contraseña", "prueba123",
            "-i", "archivos_prueba/audio_salida.wav",
            "-o", "archivos_prueba/datos_desocultos.txt",
        ]
    },
    {
        "description": "Prueba básica pasar texto a audio SSTV",
        "command": [
            "python3", SCRIPT_PATH, "ocultar",
            "--modo-cifrado", "aes",
            "--modo-cifrado-imagen", "lsb",
            "--modo-cifrado-audio", "sstv",
            "-i", "archivos_prueba/prueba.txt archivos_prueba/imagen.png",
            "-o", "./sstv.wav",
            "--contraseña", "qwqwqw",
        ]
    },
    # Agrega más casos de prueba aquí
]

# Ejecutar los casos de prueba
def run_tests():
    for idx, test_case in enumerate(TEST_CASES, 1):
        print(f"\nEjecutando prueba #{idx}: {test_case['description']}")
        try:
            # Ejecuta el comando usando subprocess
            result = subprocess.run(
                test_case["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Imprime la salida de la prueba
            #print(f"Comando: {' '.join(test_case['command'])}")
            #print(f"Salida estándar:\n{result.stdout}")
            #print(f"Error estándar:\n{result.stderr}")
            
            # Validación de resultados
            if result.returncode == 0:
                print("✅ Prueba completada con éxito.")
            else:
                print(f"❌ Error en la prueba. Código de salida: {result.returncode}")
        except Exception as e:
            print(f"⚠️ Error al ejecutar la prueba: {e}")

if __name__ == "__main__":
    run_tests()
