"""
Módulo de Acceso a Datos (Data Access Layer - DAL).

Encapsula toda la lógica de lectura y escritura de datasets en disco mediante Pandas.
Al aislar la I/O en la clase `DataLoader`, se desacopla la lógica de persistencia
de la lógica de negocio (Pipeline ETL y Machine Learning). Esto facilita el testing
(mediante mocks) y asegura un único punto de cambio si se migra el almacenamiento
(por ejemplo, de sistema de archivos local a S3 o Base de Datos).
"""
import pandas as pd
from pathlib import Path
import logging
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Fachada utilitaria para la carga y guardado de DataFrames.
    
    Técnica: Soporta inyección de dependencias en el constructor. Permite a los tests
    inyectar directorios temporales en lugar de sobrescribir los datos de producción,
    usando por defecto las rutas globales de `src.config`.
    """

    def __init__(self, raw_path: Path = RAW_DATA_DIR, processed_path: Path = PROCESSED_DATA_DIR):
        self.raw_path = raw_path
        self.processed_path = processed_path

    def load_raw_dataset(self, filename: str) -> pd.DataFrame:
        """
        Lee archivos estructurados en formato CSV desde la capa de datos inmutables (Raw).
        Diseñado específicamente para la fase "Extract" del proceso ETL.
        """
        if not self.raw_path:
            logger.error("No se ha definido la ruta de datos raw (RAW_PATH).")
            raise ValueError("RAW_PATH no está configurado de forma segura.")

        full_path = self.raw_path / filename

        # Verificación anticipada (fail-fast) para evitar errores crípticos de Pandas.
        if not full_path.exists():
            logger.error(f"El archivo origen no existe en la ruta especificada: {full_path}")
            raise FileNotFoundError(f"No se encontró: {full_path}")

        logger.info(f"Iniciando carga de datos raw desde: {full_path}")
        try:
            return pd.read_csv(full_path)
        except Exception as e:
            logger.error(f"Error I/O o incompatibilidad de formato al parsear el CSV: {e}")
            raise

    def save_processed_dataset(self, df: pd.DataFrame, filename: str) -> None:
        """
        Vuelca a disco el dataset enriquecido, producto final del pipeline ETL.
        
        Técnica: Se emplea formato Parquet en lugar de CSV por diseño. Parquet es un formato 
        columnar, binario y tipado, lo que garantiza preservación estricta de dtypes (categorías,
        fechas), reduce drásticamente el uso de disco por compresión y es sustancialmente 
        más rápido de cargar en memoria para procesos de Machine Learning recurrentes.
        """
        full_path = self.processed_path / filename
        
        # Operación idempotente: garantiza que el árbol de directorios `data/processed/` 
        # exista antes de escribir, evitando FileNotFoundError.
        full_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Guardando datos procesados finales en: {full_path}")
        try:
            # Requiere la librería `pyarrow` o `fastparquet` en el backend instalada.
            df.to_parquet(full_path)
        except Exception as e:
            logger.error(f"Fallo de serialización al guardar DataFrame como Parquet: {e}")
            raise

    def load_processed_dataset(self, filename: str) -> pd.DataFrame:
        """
        Deserializa un dataset final desde disco (Parquet), típicamente invocado
        directamente por el `ScoutingEngine` o el Frontend.
        """
        if not self.processed_path:
            logger.error("No se ha definido la ruta de almacenamiento de datos procesados.")
            raise ValueError("PROCESSED_PATH no está configurado.")

        full_path = self.processed_path / filename

        if not full_path.exists():
            logger.error(f"Target file no existe: {full_path}")
            raise FileNotFoundError(f"No se encontró el dataset procesado: {full_path}")

        logger.info(f"Cargando dataset analítico optimizado desde: {full_path}")
        try:
            # Deserialización binaria columnar rápida. Restaura automáticamente tipos complejos.
            return pd.read_parquet(full_path)
        except Exception as e:
            logger.error(f"Corrupción de archivo o error I/O al leer Parquet: {e}")
            raise