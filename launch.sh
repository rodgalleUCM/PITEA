#!/bin/bash
source "/opt/PITEA/venv/bin/activate"

# Evitar Qt por completo: usar GTK o el sistema nativo
export QT_QPA_PLATFORM_PLUGIN_PATH=/opt/PITEA/venv/lib/python3.11/site-packages/cv2/qt/plugins
export QT_QPA_PLATFORM=xcb


python3 "/home/alberto/tfg/TFG-PITEA/pitea/launch.py" "$@"

deactivate
