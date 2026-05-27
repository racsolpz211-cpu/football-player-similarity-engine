from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from frontend.utils import metric_display_name


def _value(row: pd.Series, metric: str) -> float:
    return float(pd.to_numeric(pd.Series([row.get(metric, 0)]), errors="coerce").fillna(0).iloc[0])


def render_comparison_table(player_a: pd.Series, player_b: pd.Series, metrics: list[str]) -> None:
    rows: list[str] = []
    for metric in metrics:
        value_a = _value(player_a, metric)
        value_b = _value(player_b, metric)
        class_a = "dominates-left" if value_a > value_b else ""
        class_b = "dominates-right" if value_b > value_a else ""
        rows.append(
            "<tr>"
            f'<td class="{class_a}">{value_a:,.2f}</td>'
            f'<td class="metric-name">{html.escape(metric_display_name(metric))}</td>'
            f'<td class="{class_b}">{value_b:,.2f}</td>'
            "</tr>"
        )

    table = (
        '<table class="comparison-table">'
        "<thead><tr>"
        f"<th>{html.escape(str(player_a.get('player', 'Jugador A')))}</th>"
        "<th>Metrica</th>"
        f"<th>{html.escape(str(player_b.get('player', 'Jugador B')))}</th>"
        "</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
    )
    st.markdown(table, unsafe_allow_html=True)


def render_similarity_summary(
    df: pd.DataFrame,
    player_a: pd.Series,
    player_b: pd.Series,
    metrics: list[str],
) -> None:
    scored: list[tuple[float, str, float, float]] = []
    for metric in metrics:
        series = pd.to_numeric(df[metric], errors="coerce")
        spread = float(series.std()) if float(series.std() or 0) > 0 else 1.0
        value_a = _value(player_a, metric)
        value_b = _value(player_b, metric)
        scored.append((abs(value_a - value_b) / spread, metric, value_a, value_b))

    closest = sorted(scored, key=lambda item: item[0])[:4]
    different = sorted(scored, key=lambda item: item[0], reverse=True)[:4]

    left, right = st.columns(2)
    with left:
        st.markdown("**Mayores similitudes**")
        for _, metric, value_a, value_b in closest:
            st.write(f"{metric_display_name(metric)}: {value_a:.2f} vs {value_b:.2f}")
    with right:
        st.markdown("**Mayores diferencias**")
        for _, metric, value_a, value_b in different:
            st.write(f"{metric_display_name(metric)}: {value_a:.2f} vs {value_b:.2f}")
