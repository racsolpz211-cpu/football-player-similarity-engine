from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.components.comparison_table import render_comparison_table, render_similarity_summary
from frontend.components.radar_chart import build_radar_chart
from frontend.styles import metric_strip
from frontend.utils import format_player_label, numeric_features, preferred_radar_features


def render_player_comparison(
    df: pd.DataFrame,
    player_a: pd.Series,
    player_b: pd.Series,
    metrics: list[str] | None = None,
) -> None:
    if player_a is None or player_b is None:
        st.warning("No se han encontrado datos suficientes para construir la comparativa.")
        return

    fallback_radar_metrics = preferred_radar_features(df)
    table_metrics = metrics or fallback_radar_metrics
    table_metrics = [metric for metric in table_metrics if metric in numeric_features(df)]
    if not table_metrics:
        table_metrics = fallback_radar_metrics

    radar_metrics = table_metrics[:10]
    if len(radar_metrics) < 3:
        radar_metrics = radar_metrics + [
            metric for metric in fallback_radar_metrics if metric not in radar_metrics
        ][: 3 - len(radar_metrics)]

    st.markdown('<div class="section-title">Cara a cara</div>', unsafe_allow_html=True)
    metric_strip(
        [
            ("Jugador objetivo", format_player_label(player_a)),
            ("Jugador comparado", format_player_label(player_b)),
            ("Metricas evaluadas", str(len(table_metrics))),
        ]
    )

    radar_col, table_col = st.columns([1, 1.08])
    with radar_col:
        st.plotly_chart(
            build_radar_chart(df, player_a, player_b, radar_metrics),
            use_container_width=True,
            config={"displayModeBar": False, "responsive": True},
        )
    with table_col:
        render_comparison_table(player_a, player_b, table_metrics[:18])

    st.markdown("---")
    render_similarity_summary(df, player_a, player_b, table_metrics)
