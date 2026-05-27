"""
Módulo de Configuración Global.

Centraliza la definición de rutas y constantes del proyecto. 
El uso de `pathlib.Path` asegura que las rutas sean agnósticas al sistema operativo
(funcionan igual en Windows, macOS o Linux) y facilita la resolución de directorios
relativos a la ubicación de este propio archivo, independientemente desde dónde se ejecute.
"""
from pathlib import Path

# Resuelve la ruta absoluta de la raíz del proyecto basándose en la ubicación de este script.
# `__file__` apunta a src/config.py, `.parent` es src/, y `.parent.parent` es la raíz absoluta.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Definición de las capas lógicas de almacenamiento para el pipeline de datos (Arquitectura Medallion simplificada).
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"             # Almacenamiento inmutable para datos brutos.
PROCESSED_DATA_DIR = DATA_DIR / "processed" # Almacenamiento final para datasets curados listos para modelado.

# Coeficiente UEFA por defecto, utilizado como fallback en caso de que un equipo/liga 
# no requiera o no disponga de ajuste de dificultad en la fase de normalización.
COEF_UEFA_DEFAULT = 1.0