#!/bin/bash

# Función para verificar el resultado de los comandos y mostrar mensajes de error
check_result() {
    if [ $? -ne 0 ]; then
        echo -e "\e[0;31m$1\e[0m"
        exit $?
    fi
}

echo ""
echo -e '\e[1;34m Preparing system dependencies \e[0m'
add-apt-repository ppa:deadsnakes/ppa -y
apt install -y \
    software-properties-common \
    build-essential \
    python3.8 \
    python3.8-venv

check_result 'Failed to install dependencies'

echo ""
echo -e '\e[1;34m Creating virtual environment \e[0m'

# Crea un entorno virtual de Python
python3.8 -m venv .venv
check_result 'Failed to create Python virtual environment'

echo ""
echo -e '\e[1;34m Preparing Python environment \e[0m'

# Actualiza las herramientas de Python en el entorno virtual
./.venv/bin/python -m pip install --no-cache --upgrade pip
./.venv/bin/python -m pip install --no-cache --upgrade setuptools 
./.venv/bin/python -m pip install --no-cache --upgrade wheel
./.venv/bin/python -m pip install --no-cache --upgrade cython

check_result 'Failed to prepare Python environment'

echo ""
echo -e '\e[1;34m Installing packages from "requirements.txt" \e[0m'

# Instala las dependencias de Python desde un archivo "requirements.txt"
./.venv/bin/python -m pip install --no-cache -r requirements.txt
check_result 'Failed to install packages from "requirements.txt"'