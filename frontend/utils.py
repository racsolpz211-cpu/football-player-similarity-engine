from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd
import streamlit as st

from src.models.scouting_engine import ScoutEngine
from frontend.i18n import t

METADATA_COLS = {
    "player",
    "team",
    "league",
    "season",
    "pos_",
    "nation_",
    "age_",
    "born_",
    "Playing Time_Min",
    "Playing Time_MP",
    "Playing Time_Starts",
    "Playing Time_90s",
}

DATA_DIR = Path("data/processed")

SPANISH_ATTRIBUTE_LABELS = {
    "league": "Liga",
    "season": "Temporada",
    "team": "Club",
    "player": "Jugador",
    "nation_": "Nacionalidad",
    "pos_": "Posición",
    "age_": "Edad",
    "born_": "Año de nacimiento",
    "Playing Time_MP": "Partidos jugados",
    "Playing Time_Starts": "Partidos como titular",
    "Playing Time_Min": "Minutos jugados",
    "Playing Time_90s": "Partidos completos equivalentes",
    "Performance_Gls": "Goles",
    "Performance_Ast": "Asistencias",
    "Performance_G+A": "Goles + asistencias",
    "Performance_G-PK": "Goles sin penalti",
    "Performance_PK": "Penaltis anotados",
    "Performance_PKatt": "Penaltis intentados",
    "Performance_CrdY": "Tarjetas amarillas",
    "Performance_CrdR": "Tarjetas rojas",
    "Performance_Crs": "Centros",
    "Performance_Fld": "Faltas recibidas",
    "Performance_Fls": "Faltas cometidas",
    "Performance_Int": "Intercepciones de rendimiento",
    "Performance_OG": "Goles en propia",
    "Performance_Off": "Fueras de juego",
    "Performance_Recov": "Recuperaciones",
    "Performance_TklW": "Entradas ganadas de rendimiento",
    "Expected_xG": "Goles esperados",
    "Expected_npxG": "Goles esperados sin penalti",
    "Expected_xAG": "Asistencias esperadas",
    "Expected_npxG+xAG": "xG sin penalti + xAG",
    "Expected_G-xG": "Goles - xG",
    "Expected_xA": "Asistencias esperadas xA",
    "Progression_PrgC": "Conducciones progresivas de avance",
    "Progression_PrgP": "Pases progresivos de avance",
    "Progression_PrgR": "Recepciones progresivas",
    "Per 90 Minutes_Gls": "Goles por 90",
    "Per 90 Minutes_Ast": "Asistencias por 90",
    "Per 90 Minutes_G+A": "Goles + asistencias por 90",
    "Per 90 Minutes_xG": "xG por 90",
    "Per 90 Minutes_xAG": "xAG por 90",
    "Per 90 Minutes_npxG": "xG sin penalti por 90",
    "Standard_Sh": "Tiros totales",
    "Standard_SoT": "Tiros a puerta",
    "Standard_SoT%": "Precisión de tiro",
    "Standard_Sh/90": "Tiros por 90",
    "Standard_SoT/90": "Tiros a puerta por 90",
    "Standard_G/Sh": "Goles por tiro",
    "Standard_Dist": "Distancia media de tiro",
    "KP_": "Pases clave",
    "PPA_": "Pases al área",
    "PrgP_": "Pases progresivos completados",
    "1/3_": "Pases al último tercio",
    "CrsPA_": "Centros al área",
    "Total_Att": "Pases intentados",
    "Total_Cmp": "Pases completados",
    "Total_Cmp%": "Precisión de pase",
    "Long_Cmp%": "Precisión pase largo",
    "Medium_Cmp%": "Precisión pase medio",
    "Short_Cmp%": "Precisión pase corto",
    "SCA_SCA": "Acciones que crean tiro",
    "SCA_SCA90": "Acciones que crean tiro por 90",
    "GCA_GCA": "Acciones que crean gol",
    "GCA_GCA90": "Acciones que crean gol por 90",
    "Tackles_Tkl": "Entradas totales",
    "Tackles_TklW": "Entradas defensivas ganadas",
    "Int_": "Intercepciones defensivas",
    "Blocks_Blocks": "Bloqueos totales",
    "Blocks_Sh": "Tiros bloqueados",
    "Blocks_Pass": "Pases bloqueados",
    "Clr_": "Despejes",
    "Err_": "Errores que acaban en tiro/gol",
    "Carries_Carries": "Conducciones totales",
    "Carries_PrgC": "Conducciones progresivas con balón",
    "Carries_CPA": "Conducciones al área",
    "Carries_1/3": "Conducciones al último tercio",
    "Touches_Touches": "Toques totales",
    "Touches_Att Pen": "Toques en área rival",
    "Take-Ons_Att": "Regates intentados",
    "Take-Ons_Succ": "Regates completados",
    "Take-Ons_Succ%": "Éxito en regate",
    "Team Success_PPM": "Puntos por partido con jugador",
    "Team Success_+/-": "Diferencia de goles en campo",
    "Team Success_+/-90": "Diferencia de goles por 90",
    "Team Success_On-Off": "Impacto on/off",
    "Aerial Duels_Won": "Duelos aéreos ganados",
    "Aerial Duels_Lost": "Duelos aéreos perdidos",
    "Aerial Duels_Won%": "Éxito en duelos aéreos",
}

ENGLISH_ATTRIBUTE_LABELS = {
    "league": "League",
    "season": "Season",
    "team": "Club",
    "player": "Player",
    "nation_": "Nationality",
    "pos_": "Position",
    "age_": "Age",
    "born_": "Birth Year",
    "Playing Time_MP": "Matches played",
    "Playing Time_Starts": "Matches started",
    "Playing Time_Min": "Total minutes played",
    "Playing Time_90s": "Minutes converted into full 90-minute matches",
    "Performance_Gls": "Goals scored",
    "Performance_Ast": "Assists",
    "Performance_G+A": "Goals + assists",
    "Performance_G-PK": "Non-penalty goals",
    "Performance_PK": "Penalty goals scored",
    "Performance_PKatt": "Penalty attempts",
    "Performance_CrdY": "Yellow cards",
    "Performance_CrdR": "Red cards",
    "Performance_Crs": "Crosses delivered",
    "Performance_Fld": "Fouls drawn",
    "Performance_Fls": "Fouls committed",
    "Performance_Int": "Interceptions",
    "Performance_OG": "Own goals",
    "Performance_Off": "Offsides",
    "Performance_Recov": "Ball recoveries",
    "Performance_TklW": "Tackles won",
    "Expected_xG": "Expected goals",
    "Expected_npxG": "Non-penalty expected goals",
    "Expected_xAG": "Expected assisted goals",
    "Expected_npxG+xAG": "Non-penalty xG + xAG",
    "Expected_G-xG": "Goals minus expected goals",
    "Expected_xA": "Expected assists",
    "Progression_PrgC": "Progressive carries",
    "Progression_PrgP": "Progressive passes",
    "Progression_PrgR": "Progressive receptions",
    "Per 90 Minutes_Gls": "Goals per 90",
    "Per 90 Minutes_Ast": "Assists per 90",
    "Per 90 Minutes_G+A": "Goals + assists per 90",
    "Per 90 Minutes_xG": "Expected goals per 90",
    "Per 90 Minutes_xAG": "Expected assisted goals per 90",
    "Per 90 Minutes_npxG": "Non-penalty xG per 90",
    "Standard_Sh": "Total shots",
    "Standard_SoT": "Shots on target",
    "Standard_SoT%": "Shot accuracy",
    "Standard_Sh/90": "Shots per 90",
    "Standard_SoT/90": "Shots on target per 90",
    "Standard_G/Sh": "Goals per shot",
    "Standard_Dist": "Average shot distance",
    "KP_": "Key passes",
    "PPA_": "Passes into penalty area",
    "PrgP_": "Progressive passes",
    "1/3_": "Passes into final third",
    "CrsPA_": "Crosses into penalty area",
    "Total_Att": "Total passes attempted",
    "Total_Cmp": "Total passes completed",
    "Total_Cmp%": "Pass completion rate",
    "Long_Cmp%": "Long pass completion rate",
    "Medium_Cmp%": "Medium pass completion rate",
    "Short_Cmp%": "Short pass completion rate",
    "SCA_SCA": "Shot-creating actions",
    "SCA_SCA90": "Shot-creating actions per 90",
    "GCA_GCA": "Goal-creating actions",
    "GCA_GCA90": "Goal-creating actions per 90",
    "Tackles_Tkl": "Total tackles",
    "Tackles_TklW": "Tackles won",
    "Int_": "Interceptions",
    "Blocks_Blocks": "Total blocks",
    "Blocks_Sh": "Shots blocked",
    "Blocks_Pass": "Passes blocked",
    "Clr_": "Clearances",
    "Err_": "Errors leading to shots/goals",
    "Carries_Carries": "Total carries",
    "Carries_PrgC": "Progressive carries",
    "Carries_CPA": "Carries into penalty area",
    "Carries_1/3": "Carries into final third",
    "Touches_Touches": "Total touches",
    "Touches_Att Pen": "Touches in opponent penalty area",
    "Take-Ons_Att": "Dribbles attempted",
    "Take-Ons_Succ": "Successful dribbles",
    "Take-Ons_Succ%": "Dribble success rate",
    "Team Success_PPM": "Points per match with player",
    "Team Success_+/-": "Goal difference with player on pitch",
    "Team Success_+/-90": "Goal difference per 90",
    "Team Success_On-Off": "On/off pitch goal differential impact",
    "Aerial Duels_Won": "Aerial duels won",
    "Aerial Duels_Lost": "Aerial duels lost",
    "Aerial Duels_Won%": "Aerial duel win rate",
}

@st.cache_data(show_spinner="Cargando datasets precalculados...")
def load_scouting_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_parquet(DATA_DIR / "scouting_dataset_raw.parquet")
    uefa = pd.read_parquet(DATA_DIR / "scouting_dataset_uefa.parquet")
    return raw, uefa


@st.cache_resource(show_spinner=False)
def get_engine(dataset_name: str, _df: pd.DataFrame) -> ScoutEngine:
    return ScoutEngine(_df, base_min_minutes=0)


def active_dataset(use_uefa: bool) -> tuple[pd.DataFrame, str]:
    raw, uefa = load_scouting_datasets()
    return (uefa, "UEFA") if use_uefa else (raw, "Raw")


def player_options(df: pd.DataFrame) -> list[str]:
    return sorted(df["player"].dropna().astype(str).unique())


def fuzzy_player_matches(query: str, players: list[str], limit: int = 12) -> list[str]:
    if not query:
        return players

    query_norm = query.strip().lower()
    scored: list[tuple[float, str]] = []
    for player in players:
        player_norm = player.lower()
        contains_bonus = 0.45 if query_norm in player_norm else 0.0
        starts_bonus = 0.2 if player_norm.startswith(query_norm) else 0.0
        score = SequenceMatcher(None, query_norm, player_norm).ratio() + contains_bonus + starts_bonus
        scored.append((score, player))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [player for _, player in scored[:limit]]


def smart_player_select(label: str, df: pd.DataFrame, key: str) -> str | None:
    players = player_options(df)
    return st.selectbox(
        label,
        players,
        index=None,
        key=f"{key}_select",
        placeholder=t("search_ph"),
    )


def player_numeric_stats(row: pd.Series, metrics: list[str], limit: int = 30) -> pd.DataFrame:
    data = []
    for metric in metrics[:limit]:
        value = pd.to_numeric(pd.Series([row.get(metric)]), errors="coerce").iloc[0]
        if pd.notna(value):
            data.append({t("metric_col"): metric_display_name(metric), t("value_col"): round(float(value), 3)})
    return pd.DataFrame(data)


def seasons_for_player(df: pd.DataFrame, player: str | None) -> list[str]:
    if not player:
        return []
    values = df.loc[df["player"].astype(str) == player, "season"].dropna().astype(str).unique()
    return sorted(values, reverse=True)


def numeric_features(df: pd.DataFrame) -> list[str]:
    return [
        col
        for col in df.columns
        if col not in METADATA_COLS and pd.api.types.is_numeric_dtype(df[col])
    ]


def format_player_label(row: pd.Series) -> str:
    season = row.get("season", "")
    team = row.get("team", "")
    player = row.get("player", "")
    return f"{player} - {team} - {season}"


def get_player_row(
    df: pd.DataFrame,
    player: str,
    season: str | int | None = None,
    team: str | None = None,
) -> pd.Series | None:
    mask = df["player"].astype(str).str.lower() == str(player).lower()
    if season is not None:
        mask &= df["season"].astype(str) == str(season)
    if team:
        mask &= df["team"].astype(str).str.lower() == str(team).lower()

    rows = df[mask].sort_values("season", ascending=False)
    if rows.empty:
        return None
    return rows.iloc[0]


def preferred_radar_features(df: pd.DataFrame) -> list[str]:
    preferred = [
        "Per 90 Minutes_Gls",
        "Per 90 Minutes_Ast",
        "Expected_xG",
        "Expected_xAG",
        "Progression_PrgC",
        "Progression_PrgP",
        "Standard_Sh/90",
        "Total_Cmp%",
        "Tackles_Tkl",
        "Int_",
        "Blocks_Blocks",
        "Touches_Touches",
    ]
    available = [col for col in preferred if col in df.columns]
    if len(available) >= 6:
        return available[:8]
    return numeric_features(df)[:8]


def _fallback_metric_name(metric: str) -> str:
    return metric.replace("_", " ").replace("/", " / ").replace("  ", " ").strip()


def metric_display_name(metric: str) -> str:
    is_en = st.session_state.get("lang", "es") == "en"
    labels_dict = ENGLISH_ATTRIBUTE_LABELS if is_en else SPANISH_ATTRIBUTE_LABELS

    base_metric = metric.replace("_90_padj", "").replace("_padj", "").replace("_90", "")

    if base_metric in labels_dict:
        return labels_dict[base_metric]

    if base_metric.endswith("/90"):
        without_suffix = base_metric[:-3]
        if without_suffix in labels_dict:
            return labels_dict[without_suffix]

    return _fallback_metric_name(base_metric)
