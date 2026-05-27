import streamlit as st

from frontend.components.player_comparison import render_player_comparison
from frontend.styles import metric_strip
from frontend.utils import active_dataset, get_player_row, metric_display_name, numeric_features, seasons_for_player, smart_player_select
from frontend.i18n import t

def render_explorer_page(use_uefa: bool) -> None:
    df, dataset_name = active_dataset(use_uefa)
    st.title(t("exp_title"))
    st.caption(t("exp_caption"))

    metric_strip(
        [
            (t("exp_dataset"), dataset_name),
            (t("exp_unique_players"), f"{df['player'].nunique():,}"),
            (t("exp_num_vars"), f"{len(numeric_features(df)):,}"),
        ]
    )

    left, right = st.columns(2)
    with left:
        player_a = smart_player_select(t("exp_player_a"), df, "compare_a")
        seasons_a = seasons_for_player(df, player_a)
        season_a = st.selectbox(t("exp_season_a"), seasons_a, key="compare_season_a") if seasons_a else None
    with right:
        player_b = smart_player_select(t("exp_player_b"), df, "compare_b")
        seasons_b = seasons_for_player(df, player_b)
        season_b = st.selectbox(t("exp_season_b"), seasons_b, key="compare_season_b") if seasons_b else None

    selected_metrics = st.multiselect(
        t("exp_metrics_title"),
        numeric_features(df),
        default=[],
        format_func=metric_display_name,
        help=t("exp_metrics_help"),
    )

    if player_a and player_b and season_a and season_b:
        row_a = get_player_row(df, player_a, season_a)
        row_b = get_player_row(df, player_b, season_b)
        render_player_comparison(df, row_a, row_b, selected_metrics or None)
    else:
        st.info(t("exp_select_warning"))
