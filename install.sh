#!/bin/bash

set -e  # Salir al primer error

APP_NAME="PITEA"
VENV_DIR="/opt/$APP_NAME/venv"
PYTHON_BIN="python3"
LAUNCHER_PATH="/usr/local/bin/pitea"

# -------------------------------
function info() {
  echo -e "\033[1;34m[INFO]\033[0m $1"
}

function error() {
  echo -e "\033[1;31m[ERROR]\033[0m $1" >&2
  exit 1
}

# -------------------------------
function check_dependencies() {
  info "Verificando dependencias del sistema..."
  
  command -v $PYTHON_BIN >/dev/null 2>&1 || error "Python3 no está instalado."
  command -v pip3 >/dev/null 2>&1 || error "pip3 no está instalado."

  if ! "$PYTHON_BIN" -m venv --help >/dev/null 2>&1; then
    error "El módulo venv no está disponible. Instálalo con:\n  sudo apt install python3-venv"
  fi
}

# -------------------------------
function create_virtualenv() {
  if [ -d "$VENV_DIR" ]; then
    info "El entorno virtual ya existe en $VENV_DIR"
  else
    info "Creando entorno virtual en $VENV_DIR"
    sudo mkdir -p "$(dirname "$VENV_DIR")"
    sudo chown "$USER":"$USER" "$(dirname "$VENV_DIR")"
    $PYTHON_BIN -m venv "$VENV_DIR"
  fi

  source "$VENV_DIR/bin/activate"
}

# -------------------------------
function install_requirements() {
  info "Instalando dependencias desde requirements.txt"
  pip install --upgrade pip setuptools wheel
  pip install -r requirements.txt
}

# -------------------------------
function install_tesseract() {
  info "Instalando Tesseract OCR"
  sudo apt install -y tesseract-ocr
}

# -------------------------------
function install_fuentes() {
  info "Instalando fuentes"
  mkdir -p ~/.local/share/fonts
  cp pitea/fuentes/* ~/.local/share/fonts/
  fc-cache -f -v
}

# -------------------------------
function install_qsstv() {
  info "Instalando QSSTV"
  sudo apt install -y qsstv
}

# -------------------------------
function create_launcher() {
  info "Creando script ejecutable global 'pitea' en /usr/local/bin"

  INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  sudo tee "$LAUNCHER_PATH" > /dev/null <<EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"

# Evitar Qt por completo: usar GTK o el sistema nativo
export QT_QPA_PLATFORM_PLUGIN_PATH=/opt/PITEA/venv/lib/python3.11/site-packages/cv2/qt/plugins
export QT_QPA_PLATFORM=xcb


python3 "$INSTALL_DIR/pitea/launch.py" "\$@"

deactivate
EOF

  sudo chmod +x "$LAUNCHER_PATH"
}


function install_qt_xcb_deps() {
  info "Instalando dependencias de sistema para Qt + OpenCV"
  sudo apt install -y libx11-xcb1 libxcb1 libxcb-glx0 libxcb-keysyms1 libxcb-image0 \
  libxcb-shm0 libxcb-icccm4 libxcb-sync1 libxcb-xfixes0 libxcb-shape0 \
  libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxkbcommon-x11-0
}

# -------------------------------
function main() {
  info "Iniciando instalación para $APP_NAME"

  check_dependencies
  create_virtualenv
  install_requirements
  install_tesseract
  install_fuentes
  install_qsstv
  install_qt_xcb_deps
  create_launcher

  info "✅ Instalación completada. Ejecuta con: pitea"
}

main "$@"
