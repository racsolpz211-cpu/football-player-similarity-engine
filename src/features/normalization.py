"""
Módulo de Normalización y Ajuste Matemático.

Este componente concentra el núcleo matemático del procesamiento estadístico.
Contiene diccionarios estáticos de reglas y funciones puras vectorizadas de Pandas
para realizar transformaciones complejas (Per-90, Possession Adjustment, UEFA Coefficients)
garantizando alta eficiencia y bajo acoplamiento.
"""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# --- DICCIONARIO HISTÓRICO DE COEFICIENTES UEFA ---
# Actúa como una base de conocimiento embebida (Knowledge Base).
# Refleja la ponderación de competitividad (1º = 1.00, 2º = 0.95, etc.) que permite
# proyectar estadísticamente el paso de un jugador de una liga menor a la Premier, por ejemplo.
UEFA_COEFFICIENTS = {
    '1718': {'ESP-La Liga': 1.00, 'ENG-Premier League': 0.95, 'ITA-Serie A': 0.90, 'GER-Bundesliga': 0.85, 'FRA-Ligue 1': 0.80},
    '1819': {'ESP-La Liga': 1.00, 'ENG-Premier League': 0.95, 'ITA-Serie A': 0.90, 'GER-Bundesliga': 0.85, 'FRA-Ligue 1': 0.80},
    '1920': {'ESP-La Liga': 1.00, 'ENG-Premier League': 0.95, 'GER-Bundesliga': 0.90, 'ITA-Serie A': 0.85, 'FRA-Ligue 1': 0.80},
    '2021': {'ENG-Premier League': 1.00, 'ESP-La Liga': 0.95, 'ITA-Serie A': 0.90, 'GER-Bundesliga': 0.85, 'FRA-Ligue 1': 0.80},
    '2122': {'ENG-Premier League': 1.00, 'ESP-La Liga': 0.95, 'ITA-Serie A': 0.90, 'GER-Bundesliga': 0.85, 'FRA-Ligue 1': 0.80},
    '2223': {'ENG-Premier League': 1.00, 'ESP-La Liga': 0.95, 'GER-Bundesliga': 0.90, 'ITA-Serie A': 0.85, 'FRA-Ligue 1': 0.80},
    '2324': {'ENG-Premier League': 1.00, 'ITA-Serie A': 0.95, 'ESP-La Liga': 0.90, 'GER-Bundesliga': 0.85, 'FRA-Ligue 1': 0.80},
    '2425': {'ENG-Premier League': 1.00, 'ITA-Serie A': 0.95, 'ESP-La Liga': 0.90, 'GER-Bundesliga': 0.85, 'FRA-Ligue 1': 0.80},
    '2526': {'ENG-Premier League': 1.00, 'ITA-Serie A': 0.95, 'ESP-La Liga': 0.90, 'GER-Bundesliga': 0.85, 'FRA-Ligue 1': 0.80} # Proyección heurística
}

# Constantes de dominio: Definen qué atributos exactos de la matriz deben ser procesados
METRICS_TO_90 = [
    # --- Defensivas ---
    'Tackles_Tkl', 'Tackles_TklW', 'Int_', 'Blocks_Blocks',
    'Blocks_Sh', 'Blocks_Pass', 'Clr_', 'Err_', 'Performance_Recov',
    # --- Pases y Progresión ---
    'Progression_PrgC', 'Progression_PrgP', 'Progression_PrgR',
    'KP_', 'PPA_', '1/3_', 'CrsPA_', 'Total_Att', 'Total_Cmp',
    # --- Conducciones y Toques ---
    'Carries_Carries', 'Carries_CPA', 'Carries_1/3',
    'Touches_Touches', 'Touches_Att Pen',
    # --- Duelos y Faltas ---
    'Aerial Duels_Won', 'Aerial Duels_Lost', 'Performance_Fld', 'Performance_Fls',
    # --- Ofensivas
    'Performance_Crs', 'Standard_Sh', 'Standard_SoT', 'Take-Ons_Att', 'Take-Ons_Succ'
]

# Variables que por su naturaleza (sin balón) deben ser ajustadas por Posesión Inversa
DEFENSIVE_PADJ_METRICS = [
    'Tackles_Tkl_90', 'Tackles_TklW_90', 'Int__90', 'Blocks_Blocks_90',
    'Blocks_Sh_90', 'Blocks_Pass_90', 'Clr__90', 'Performance_Recov_90'
]

# Variables que por su naturaleza (con balón) deben ser ajustadas por Posesión Directa
POSSESSION_PADJ_METRICS = [
    'Progression_PrgC_90', 'Progression_PrgP_90', 'Progression_PrgR_90',
    'KP__90', 'PPA__90', '1/3__90', 'CrsPA__90', 'Total_Att_90',
    'Total_Cmp_90', 'Carries_Carries_90', 'Carries_CPA_90', 'Carries_1/3_90',
    'Touches_Touches_90', 'Touches_Att Pen_90'
]

def normalize_per_90(df: pd.DataFrame, columns: list, minutes_col: str = 'Playing Time_Min') -> pd.DataFrame:
    """
    Convierte estadísticas de volumen total a tasas proyectadas por cada 90 minutos jugados (un partido).
    
    Técnica Matemática Segura: 
    Implementa un mecanismo para evitar divisiones por cero (`ZeroDivisionError` o `np.inf` en Pandas)
    sustituyendo los ceros iniciales por NaN temporalmente, lo que asegura que el motor de ML posterior
    pueda gestionarlos (por ejemplo, mediante imputaciones o filtrados) sin provocar crash matemático.
    """
    df_norm = df.copy() # Inmutabilidad: No altera el dataframe ingresado.
    logger.info(f"Normalizando {len(columns)} métricas a /90 minutos...")

    if minutes_col not in df_norm.columns:
        logger.error(f"Columna de minutos '{minutes_col}' no encontrada. Abortando normalización.")
        raise KeyError(f"Falta la columna base de tiempo: {minutes_col}")

    # 1. Crear una Serie segura (safe division strategy)
    safe_minutes = df_norm[minutes_col].replace(0, np.nan)

    for col in columns:
        if col in df_norm.columns:
            # 2. Generación programática del nuevo label (feature base)
            new_col_name = f"{col}_90"
            # 3. Cálculo matricial vectorizado (O(1) a nivel de abstracción Pandas)
            df_norm[new_col_name] = (df_norm[col] / safe_minutes) * 90
        else:
            logger.warning(f"La columna {col} no se encontró en el DataFrame para normalizar /90.")

    return df_norm

def apply_padj(df: pd.DataFrame, columns: list, mode: str, possession_col: str = 'possession', k: float = 0.5) -> pd.DataFrame:
    """
    Algoritmo PAdj (Possession-Adjusted Stats). Contextualiza el dato bruto según 
    la oportunidad de intervención táctica del jugador basada en el estilo del equipo.
    
    Técnica Matemática:
    - 'defensive' (Factor inverso): Posesión alta = Menor tiempo sin balón = Menos oportunidad de robar. 
      -> Un tackle en el City vale estadísticamente más que en el Burnley.
    - 'possession' (Factor directo): Posesión baja = Menor tiempo con balón = Menos oportunidad de pase.
      -> Un pase completado en el Burnley vale más que en el City.
      
    Args:
        k: Constante de suavizado logarítmico (factor base). Evita penalizaciones excesivas
           por la no-linealidad de la estadística avanzada (default estándar de la industria = 0.5 o 50%).
    """
    df_adj = df.copy()

    # Validación fail-fast
    if possession_col not in df_adj.columns:
        logger.error(f"Columna de posesión '{possession_col}' no encontrada.")
        raise KeyError(f"Falta la columna: {possession_col}")

    # Transformación a base decimal (ratio matemático)
    possession_ratio = df_adj[possession_col] / 100.0

    # Estrategia de blindaje asintótico (Clipping) para prevenir divisiones por 0 o anomalías algorítmicas
    if mode == 'defensive':
        safe_ratio = possession_ratio.clip(upper=0.99)
        factor = 1 - safe_ratio
    elif mode == 'possession':
        safe_ratio = possession_ratio.clip(lower=0.01)
        factor = safe_ratio
    else:
        raise ValueError("El parámetro 'mode' debe ser 'defensive' o 'possession'.")

    # Operación vectorizada sobre matriz M x N
    for col in columns:
        if col in df_adj.columns:
            new_col_name = f"{col}_padj"
            df_adj[new_col_name] = (df_adj[col] / factor) * k

    return df_adj

def apply_uefa_coefficient(df: pd.DataFrame, columns: list, apply: bool = True, mode: str = 'selective') -> pd.DataFrame:
    """
    Aplica multiplicadores de dificultad de la liga. Modifica la métrica final simulando 
    qué habría ocurrido matemáticamente si el jugador hubiese generado el mismo output en una 
    liga top absoluta (coeficiente 1.00).
    
    Técnica Vectorizada (Apply optimizado):
    Implementa una lógica de búsqueda hash-map bidimensional (Temporada -> Liga) usando un 
    functor aplicable (`apply(get_multiplier, axis=1)`) sobre el indexado de Pandas.
    """
    df_uefa = df.copy()

    # Interruptor arquitectónico (Feature Toggle) para A/B Testing o simulaciones sin sesgo geográfico
    if not apply:
        logger.info("Ajuste UEFA apagado por el usuario (apply=False). Retornando datos originales.")
        return df_uefa

    # Subset conceptual: Sólo métricas de "éxito final" o "calidad" que realmente
    # varían en base a la dificultad de los rivales.
    QUALITY_METRICS = [
        'Performance_Gls_90', 'Performance_Ast_90', 'Expected_xG_90',
        'SCA_SCA90', 'GCA_GCA90', 'Standard_Sh/90'
    ]

    # Resolución del modo operativo
    if mode == 'selective':
        cols_to_process = [c for c in columns if c in QUALITY_METRICS]
        logger.info(f"Modo 'selective': Ajustando {len(cols_to_process)} métricas de calidad.")
    elif mode == 'global':
        cols_to_process = columns
        logger.info(f"Modo 'global': Ajustando todas las {len(cols_to_process)} métricas.")
    else:
        raise ValueError("El parámetro 'mode' debe ser 'selective' o 'global'.")

    if not cols_to_process:
        logger.warning("No hay columnas coincidentes para ajustar en este modo.")
        return df_uefa

    # Inner Function estática para resolución O(1) en diccionario indexado doble
    def get_multiplier(row):
        season = str(row['season']).strip()
        league = str(row['league']).strip()
        return UEFA_COEFFICIENTS.get(season, {}).get(league, 1.0) # Fallback 1.0 si no hay registro

    # Computación de la matriz de escalares multiplicadores a nivel de fila (Row-Level Array)
    multipliers = df_uefa.apply(get_multiplier, axis=1)

    # Transformación matemática in-place para las columnas seleccionadas
    for col in cols_to_process:
        if col in df_uefa.columns:
            df_uefa[col] = df_uefa[col] * multipliers
        else:
            logger.warning(f"La columna {col} no existe.")

    return df_uefa
