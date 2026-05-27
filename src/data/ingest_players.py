"""
Módulo de Ingesta de Datos de Jugadores.

Este script automatiza la descarga y extracción del dataset principal de rendimiento
de jugadores desde Kaggle ('top-5-league-football-player-stats-2017-2025').
Forma la primera fase del proceso ETL (Extract), obteniendo los datos brutos
necesarios para el posterior procesamiento estadístico.
"""

import logging
import kagglehub
import shutil
from pathlib import Path
from src.config import RAW_DATA_DIR

# Configuración estándar del logger para trazar la ejecución del pipeline de datos
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ingest_players_data():
    """
    Descarga el dataset de jugadores desde Kaggle y lo ubica en el directorio raw.
    
    Flujo de ejecución:
    1. Utiliza `kagglehub` para resolver y descargar el dataset. Este método utiliza caché local,
       por lo que si el dataset ya está actualizado, evita descargas redundantes de red.
    2. Identifica el archivo CSV principal dentro de la estructura devuelta por Kaggle.
    3. Asegura la existencia del directorio destino (`data/raw`) y realiza una copia segura
       del archivo, renombrándolo a un formato estándar ('players.csv').
       
    Raises:
        FileNotFoundError: Si el dataset se descarga pero no contiene archivos .csv procesables.
        Exception: Captura y loguea cualquier excepción subyacente (I/O, Red, Permisos) antes de relanzarla.
    """
    try:
        logger.info("Iniciando descarga desde Kaggle...")
        
        # Retorna un Path hacia la caché temporal donde kagglehub aloja los archivos.
        download_path = Path(kagglehub.dataset_download("emrey3lmaz/top-5-league-football-player-stats-2017-2025"))

        # Extracción dinámica: buscaremos cualquier CSV, asumiendo que el dataset
        # principal es el primer match. Previene fallos si el autor cambia el nombre del archivo.
        csv_files = list(download_path.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError("No se encontró ningún archivo CSV en la carpeta descargada de Kaggle.")
        source_csv = csv_files[0]

        # Creación recursiva del directorio de destino si no existe (equivalente a `mkdir -p`)
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        destination_path = RAW_DATA_DIR / "players.csv"
        
        # Realizamos una copia (shutil.copy) en lugar de un movimiento (shutil.move) 
        # para no alterar el estado de la caché interna gestionada por kagglehub.
        shutil.copy(source_csv, destination_path)

        logger.info(f"Dataset de jugadores integrado en {destination_path}")
        
    except Exception as e:
        logger.error(f"Fallo en la ingesta de jugadores: {e}")
        # Relanzar la excepción es crítico para que los orquestadores superiores (ej. scripts bash) 
        # detecten que el paso ETL ha fallado y detengan el pipeline.
        raise

if __name__ == "__main__":
    # Permite la ejecución del módulo como un script independiente
    ingest_players_data()
