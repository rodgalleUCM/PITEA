import subprocess
import threading
import itertools
import time
from interfaz.constantes import RESET, VERDE, ROJO, MORADO, SPINNING

def spinner():
    for cursor in itertools.cycle(['|', '/', '-', '\\']):
        if not SPINNING:
            break
        print(MORADO + "\rProcesando... {cursor}" +RESET, end="", flush=True)
        time.sleep(0.1)

def ejecutar_comando(comando):
    global SPINNING
    SPINNING = True

    # Iniciar el spinner en un hilo separado
    hilo_spinner = threading.Thread(target=spinner)
    hilo_spinner.start()

    try:
        result = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        SPINNING = False  # Detener el spinner
        hilo_spinner.join()  # Esperar a que termine el hilo

        print(VERDE + "\r🟢 Proceso de " + comando[2] + " finalizado.\n" + RESET)
        print(MORADO + "Podra encontrar el archivo en la ruta especificada.\n"+ RESET)
        print(result.stdout)
        input(MORADO + "Presione enter para continuar..."+ RESET)
    except subprocess.CalledProcessError as error:
        SPINNING = False
        hilo_spinner.join()
        print(ROJO +"\r❌ Error en la ejecución:\n" + RESET, error.stderr)
        input(MORADO + "Presione enter para continuar..."+ RESET)
