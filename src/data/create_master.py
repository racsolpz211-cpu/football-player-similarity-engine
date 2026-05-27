"""
Módulo de Construcción del Dataset Maestro.

Este script ejecuta la fase "Transform & Load" temprana del pipeline ETL. 
Su responsabilidad es tomar los datasets crudos (rendimiento individual y contexto 
de equipo), realizar limpieza y estandarización de llaves primarias (nombres de equipos, 
temporadas) y fusionarlos (Merge) en un único Dataset Maestro ('master_dataset.parquet').
Incluye lógica de validación y generación de reportes de auditoría en caso de pérdida de datos.
"""
import logging
import pandas as pd
from pathlib import Path

# Arquitectura: Importamos el cargador de datos unificado para operaciones I/O.
from src.data.loader import DataLoader

# Configuración del Logger para observabilidad del pipeline
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diccionario estático de mapeo para resolución de entidades (Entity Resolution).
# Resuelve discrepancias de nomenclatura entre Kaggle (jugadores) y FBref (posesión).
TEAM_NAME_MAP = {
    'newcastle utd': 'newcastle united',
    'tottenham': 'tottenham hotspur',
    'west ham': 'west ham united',
    'manchester utd': 'manchester united',
    'sheffield utd': 'sheffield united',
    'nott\'ham forest': 'nottingham forest',
    'betis': 'real betis',
    'eint frankfurt': 'eintracht frankfurt',
    'paris s-g': 'paris saint-germain',
    'huddersfield': 'huddersfield town',
    'la coruña': 'deportivo la coruña'
}

def clean_team_names(series: pd.Series) -> pd.Series:
    """
    Estandariza los nombres de los equipos para asegurar una unión (merge) perfecta.
    Operaciones vectorizadas de Pandas para máxima eficiencia en grandes volúmenes de datos.
    """
    # 1. Cast a string seguro, 2. Trim de espacios, 3. Lowercase, 4. Aplicar mapa de resolución.
    return series.astype(str).str.strip().str.lower().replace(TEAM_NAME_MAP)

def create_master_dataset():
    """
    Orquesta la unificación (Join) de datos individuales y de posesión de equipos.
    
    Técnica:
    Utiliza un LEFT JOIN sobre [Equipo, Temporada] asegurando que no perdamos a ningún
    jugador, incluso si falla la ingesta de su equipo. Posteriormente, un sistema de
    auditoría detecta estos fallos y genera un reporte accionable en `reports/`.
    """
    loader = DataLoader()

    # --- 1. CARGA DE DATOS CRUDOS ---
    players_path = loader.raw_path / "players.csv"
    logger.info(f"Cargando dataset de jugadores desde: {players_path}")

    if not players_path.exists():
        logger.error("No se encontró players.csv. Ejecuta ingest_players.py primero.")
        raise FileNotFoundError(f"Archivo no encontrado: {players_path}")

    try:
        # Crucial: El dataset de Kaggle usa ';' como separador y ',' para decimales.
        # Fallar en esto provocaría que Pandas lea todo como strings monolíticos.
        df_players = pd.read_csv(players_path, sep=';', decimal=',')
    except Exception as e:
        logger.error(f"Error al leer players.csv: {e}")
        raise

    possession_path = loader.raw_path / "team_possession.csv"
    logger.info(f"Cargando dataset de posesión desde: {possession_path}")

    if not possession_path.exists():
        logger.error("No se encontró team_possession.csv. Ejecuta ingest_possession.py primero.")
        raise FileNotFoundError(f"Archivo no encontrado: {possession_path}")

    try:
        # El parser de soccerdata exporta 3 filas de MultiIndex. Se saltan para forzar un df plano.
        df_possession = pd.read_csv(possession_path, skiprows=3, header=None)

        # Extracción selectiva de columnas: 0(league), 1(season), 2(team), 5(Possession)
        # Se usa .copy() para evitar warnings de vista vs copia en memoria.
        df_possession = df_possession[[0, 1, 2, 5]].copy()
        df_possession.columns = ['league', 'season', 'team', 'possession']

        # Cast forzado a numérico de la posesión, coercionando errores (e.g. strings corruptos) a NaN.
        df_possession['possession'] = pd.to_numeric(df_possession['possession'], errors='coerce')
    except Exception as e:
        logger.error(f"Error al procesar team_possession.csv: {e}")
        raise

    # --- 2. ESTANDARIZACIÓN DE LLAVES ---
    logger.info("Estandarizando llaves de unión (Equipo y Temporada)...")

    # Limpieza de nombres de equipo (Minúsculas, trim, map de equivalencias)
    df_players['team_clean'] = clean_team_names(df_players['team'])
    df_possession['team_clean'] = clean_team_names(df_possession['team'])

    # Unificación de formato de temporada (Evita fallos si uno es int y otro string)
    df_players['season_str'] = df_players['season'].astype(str).str.strip()
    df_possession['season_str'] = df_possession['season'].astype(str).str.strip()

    # Preservamos los valores originales para usarlos en el log de auditoría
    df_players['team_clean_report'] = df_players['team_clean']
    df_players['season_str_report'] = df_players['season_str']

    # --- 3. MERGE Y CALIDAD DE DATOS ---
    logger.info("Ejecutando la unión (Merge) de los datasets...")
    # LEFT JOIN: Conservamos todos los jugadores. Si falta la posesión de su equipo, será NaN.
    df_master = pd.merge(
        df_players,
        df_possession[['team_clean', 'season_str', 'possession']],
        on=['team_clean', 'season_str'],
        how='left'
    )

    # Limpieza de memorias intermedias
    df_master.drop(columns=['team_clean', 'season_str'], inplace=True)

    # Validación de integridad de datos (Data Quality Check)
    total_rows = len(df_master)
    null_possession = df_master['possession'].isna().sum()

    logger.info(f"Unión completada. Filas totales procesadas: {total_rows}")

    if null_possession > 0:
        # Sistema de alertas si hay registros huérfanos sin datos de contexto colectivo
        porcentaje_error = round((null_possession / total_rows) * 100, 2)
        logger.warning(f"¡Atención! {null_possession} filas ({porcentaje_error}%) sin dato de posesión.")
        logger.info("Generando reporte de auditoría para diagnosticar el fallo...")

        # Aislamiento de los registros defectuosos
        df_fallos = df_master[df_master['possession'].isna()]

        # Compresión: Extraemos qué equipos en qué temporadas fallaron (únicos)
        df_reporte = df_fallos[['team_clean_report', 'season_str_report']].drop_duplicates().sort_values(by=['team_clean_report', 'season_str_report'])
        df_reporte.columns = ['team_clean', 'season_str']

        from src.config import PROJECT_ROOT

        # Generación de artefacto de auditoría accionable
        report_path = PROJECT_ROOT / "reports" / "missing_possession.csv"
        report_path.parent.mkdir(parents=True, exist_ok=True) 

        df_reporte.to_csv(report_path, index=False)
        logger.info(f"🔍 Auditoría guardada: Revisa {report_path} para actualizar TEAM_NAME_MAP.")

        # Limpiamos las columnas adicionales y purgamos filas inválidas (necesitamos la posesión para PAdj)
        df_master.drop(columns=['team_clean_report', 'season_str_report'], inplace=True)
        df_master.dropna(subset=['possession'], inplace=True)

    else:
        logger.info("¡Merge perfecto! 0 valores nulos en la columna de posesión.")
        df_master.drop(columns=['team_clean_report', 'season_str_report'], inplace=True)

    # --- 4. PERSISTENCIA ---
    logger.info("Guardando Dataset Maestro en formato Parquet...")
    try:
        loader.save_processed_dataset(df_master, "master_dataset.parquet")
        logger.info("✅ Dataset Maestro creado y guardado exitosamente en data/processed/")
    except Exception as e:
        logger.error(f"Error crítico al guardar master_dataset.parquet: {e}")
        raise

if __name__ == "__main__":
    create_master_dataset()
