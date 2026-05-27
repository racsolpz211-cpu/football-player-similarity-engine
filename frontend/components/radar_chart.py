from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from frontend.styles import ACCENT_PRIMARY, ACCENT_SECONDARY, BACKGROUND, MUTED, TEXT
from frontend.utils import metric_display_name


def _percentile_values(df: pd.DataFrame, row: pd.Series, metrics: list[str]) -> list[float]:
    values: list[float] = []
    for metric in metrics:
        series = pd.to_numeric(df[metric], errors="coerce").fillna(0)
        value = float(pd.to_numeric(pd.Series([row.get(metric, 0)]), errors="coerce").fillna(0).iloc[0])
        percentile = float((series <= value).mean() * 100)
        values.append(round(percentile, 2))
    return values


def build_radar_chart(
    df: pd.DataFrame,
    player_a: pd.Series,
    player_b: pd.Series | None,
    metrics: list[str],
) -> go.Figure:
    labels = [metric_display_name(metric) for metric in metrics]
    values_a = _percentile_values(df, player_a, metrics)

    if labels:
        labels = labels + [labels[0]]
        values_a = values_a + [values_a[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_a,
            theta=labels,
            fill="toself",
            name=str(player_a.get("player", "Jugador A")),
            line=dict(color=ACCENT_PRIMARY, width=2),
            fillcolor="rgba(29, 233, 182, 0.14)",
        )
    )
    if player_b is not None:
        values_b = _percentile_values(df, player_b, metrics)
        if labels:
            values_b = values_b + [values_b[0]]
        fig.add_trace(
            go.Scatterpolar(
                r=values_b,
                theta=labels,
                fill="toself",
                name=str(player_b.get("player", "Jugador B")),
                line=dict(color=ACCENT_SECONDARY, width=2),
                fillcolor="rgba(255, 79, 216, 0.12)",
            )
        )
    fig.update_layout(
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,
        font=dict(color=TEXT, family="Inter"),
        margin=dict(l=36, r=36, t=36, b=36),
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
        polar=dict(
            bgcolor=BACKGROUND,
            radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor="#253246"),
            angularaxis=dict(gridcolor="#253246", color=MUTED),
        ),
        height=430,
    )
    return fig
