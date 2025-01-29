# TFG-PITEA

## EJEMPLO DE LLAMADA

```bash
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen lsb \
  --modo-cifrado-audio lsb \
  -i archivos_prueba/prueba.txt \
  --input_imagen archivos_prueba/imagen.png \
  --input_audio  archivos_prueba/audio.wav \
  -o ./archivos_prueba/audio_salida.wav \
  --contraseña qwqwqw \
  -v
```

```bash
  python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen lsb \
  --modo-cifrado-audio lsb \
  -i ./archivos_prueba/audio_salida.wav \
  -o ./archivos_prueba/datos_desocultos.txt \
  --contraseña qwqwqw \
  -v
```

```bash
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio sstv \
  -i archivos_prueba/prueba.txt \
  -o ./archivos_prueba/sstv.wav \
  --contraseña qwqwqw \
  -v
```

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
