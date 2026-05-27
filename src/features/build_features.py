"""
Módulo de Construcción de Atributos (Feature Engineering Pipeline).

Actúa como orquestador central de la fase analítica del ETL. Toma el dataset
maestro en bruto y ejecuta secuencialmente las transformaciones estadísticas avanzadas
(Normalización Per-90, Ajuste por Posesión PAdj, Coeficientes UEFA).
Genera múltiples versiones del dataset (bruto y ajustado por UEFA) para dar
flexibilidad al usuario final.
"""
import logging
from src.data.loader import DataLoader
from src.features.normalization import (
    normalize_per_90,
    apply_padj,
    apply_uefa_coefficient,
    METRICS_TO_90,
    DEFENSIVE_PADJ_METRICS,
    POSSESSION_PADJ_METRICS
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def build_features():
    """
    Ejecuta el flujo secuencial de transformaciones estadísticas sobre el dataset maestro.
    
    Técnica (Pipeline Arquitectónico):
    1. Carga de datos base.
    2. Homogeneización de tiempo (Per-90): Transforma métricas de volumen a tasas base (rates).
    3. Contextualización Táctica (PAdj): Modifica las tasas según la posesión del equipo.
    4. Guardado versión Raw (sin sesgo UEFA).
    5. Contextualización Competitiva (UEFA): Aplica peso a las tasas base según nivel de liga.
    6. Guardado versión final para el motor.
    """
    loader = DataLoader()

    logger.info("Cargando master_dataset.parquet...")
    try:
        df = loader.load_processed_dataset("master_dataset.parquet")
    except FileNotFoundError:
        logger.error("No se encontró master_dataset.parquet. Ejecuta src/data/create_master.py primero.")
        raise

    # Transformación 1: Elimina el sesgo de minutos jugados. 
    # Indispensable para comparar suplentes vs titulares.
    logger.info("Fase 1: Normalización /90")
    df = normalize_per_90(df, columns=METRICS_TO_90)

    # Transformación 2: Acciones sin balón. Se penaliza a jugadores de equipos sin posesión 
    # (que naturalmente defienden más) y se bonifica a equipos dominadores.
    logger.info("Fase 2: Ajuste PAdj (Defensivo)")
    df = apply_padj(df, columns=DEFENSIVE_PADJ_METRICS, mode='defensive')

    # Transformación 3: Acciones con balón. Se penaliza a jugadores en equipos dominadores 
    # (mayor oportunidad estadística natural) y se bonifica a equipos reactivos.
    logger.info("Fase 3: Ajuste PAdj (Posesión)")
    df = apply_padj(df, columns=POSSESSION_PADJ_METRICS, mode='possession')

    # Persistencia del modelo estadístico intermedio (ideal para análisis no sesgados por ligas)
    logger.info("Guardando versión PURO (scouting_dataset_raw.parquet)...")
    loader.save_processed_dataset(df, "scouting_dataset_raw.parquet")

    # Transformación 4: Ajuste de Dificultad (Calidad de la Liga).
    # 'selective' aplica solo a métricas de impacto u output directo (Ej: Goles).
    logger.info("Fase 4: Aplicando Coeficientes UEFA (Modo selective)")
    df_uefa = apply_uefa_coefficient(df, columns=df.columns.tolist(), apply=True, mode='selective')

    # Persistencia del modelo estadístico final, el cual nutre al Scouting Engine
    logger.info("Guardando versión UEFA (scouting_dataset_uefa.parquet)...")
    loader.save_processed_dataset(df_uefa, "scouting_dataset_uefa.parquet")

    logger.info("Pipeline de features completado exitosamente.")

if __name__ == "__main__":
    build_features()