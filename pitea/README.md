# TFG-PITEA

## EJEMPLO DE LLAMADA
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-audio 1 \
  -i "archivos_prueba/prueba.txt \
     archivos_prueba/imagen.png \
     archivos_prueba/audio.wav" \
  -o /home/alberto/salida/audio_salida.wav \
  --contraseña "qwqwqw" \
  --formato-salida wav

## Arbol de directorio provisional de pitea
```TFG-PITEA/
├── README.md
├── pitea/
│   ├── README.md
│   ├── pitea/
│   │   ├── audio/
│   │   │   ├── desocultador.py
│   │   │   ├── ocultador.py
│   │   │   └── procesamiento.py
│   │   ├── cache/
│   │   │   ├── audio/
│   │   │   │   ├── contenedroes/
│   │   │   │   └── limpio/
│   │   │   ├── imagenes/
│   │   │   │   ├── contenedores/
│   │   │   │   └── limpio/
│   │   ├── imagen/
│   │   │   ├── desocultador.py
│   │   │   ├── ocultador.py
│   │   │   └── procesamiento.py
│   │   ├── constantes.py
│   └── script_ejecucion.py
└── pyproject.toml
