# TFG-PITEA

## EJEMPLO DE LLAMADA

```bash
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen "lsb" \
  --modo-cifrado-audio "lsb" \
  -i "archivos_prueba/prueba.txt \
     archivos_prueba/imagen.png \
     archivos_prueba/audio.wav" \
  -o ./audio_salida.wav \
  --contraseña "qwqwqw" \
  --formato-salida wav \
  -v
```

```bash
  python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen "lsb" \
  --modo-cifrado-audio "lsb" \
  -i audio_salida.wav \
  -o datos_desocultos.txt \
  --contraseña "qwqwqw" \
  -v
```

```bash
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen "lsb" \
  --modo-cifrado-audio "sstv" \
  -i "archivos_prueba/prueba.txt \
     archivos_prueba/imagen.png" \  
  -o ./sstv.wav \
  --contraseña "qwqwqw" \
  --formato-salida wav \
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
