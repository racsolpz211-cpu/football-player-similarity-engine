"""
Módulo de Ingesta de Datos de Posesión (Contexto de Equipo).

Se encarga de descargar métricas a nivel de equipo desde FBref mediante web scraping,
utilizando la librería `soccerdata`. Estos datos son fundamentales para realizar
el "Ajuste por Posesión" (PAdj) en las estadísticas individuales de los jugadores,
permitiendo contextualizar el volumen defensivo u ofensivo según el estilo táctico de su equipo.
"""
import logging
from pathlib import Path
import soccerdata as sd
from src.config import RAW_DATA_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ingest_team_possession():
    """
    Orquesta la extracción de datos de posesión colectiva y su persistencia en local.
    
    Flujo técnico:
    1. Instancia el scraper de `soccerdata` enfocado en las 5 grandes ligas de Europa
       (Big 5 European Leagues Combined) a lo largo de varias temporadas históricas.
    2. Realiza el parseo tabular de la sección "standard" a nivel de equipo ('team_season_stats').
    3. Persiste el resultado en formato CSV crudo dentro de la capa `RAW_DATA_DIR`.
    
    Raises:
        Exception: Captura fallos críticos como timeout de conectividad, bloqueos anti-scraping 
                   (HTTP 429 Too Many Requests) o cambios en el DOM de FBref que rompan el parser.
    """
    logger.info("Iniciando descarga de datos de posesión desde FBref...")

    try:
        # soccerdata maneja su propia caché local y control de rate-limits internamente para evitar baneos.
        # Definimos las ligas top y el rango de temporadas para alinear el contexto colectivo con los datos individuales.
        fbref = sd.FBref(
            leagues=['Big 5 European Leagues Combined'], 
            seasons=['1718', '1819', '1920', '2021', '2122', '2223', '2324', '2425']
        )

        # Extrae las estadísticas estándar agregadas por equipo para la temporada solicitada.
        # opponent_stats=False optimiza el consumo de red y memoria al descartar métricas de rivales que no usaremos.
        possession_df = fbref.read_team_season_stats(stat_type='standard', opponent_stats=False)

        destination_path: Path = RAW_DATA_DIR / "team_possession.csv"

        # Asegura de forma preventiva y recursiva que toda la jerarquía de directorios destino exista.
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        # Volcado de la estructura cruda. Se asume compatibilidad de índices CSV.
        possession_df.to_csv(destination_path)

        logger.info(f"Datos de posesión guardados exitosamente en {destination_path}")

    except Exception as e:
        logger.error(f"Error crítico durante la ingesta de posesión (Scraping FBref): {e}")
        # Interrumpir el proceso propagando el error es mandatorio; sin este contexto de equipo, 
        # el cálculo de PAdj fallará silenciosamente o de forma en cascada más adelante.
        raise

if __name__ == "__main__":
    # Facilita el testeo unitario y la ejecución manual del módulo ETL de posesión.
    ingest_team_possession()
