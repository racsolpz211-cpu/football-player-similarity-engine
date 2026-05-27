from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.components.player_comparison import render_player_comparison
from frontend.styles import metric_strip
from frontend.utils import (
    active_dataset,
    get_engine,
    get_player_row,
    metric_display_name,
    numeric_features,
    preferred_radar_features,
    seasons_for_player,
    smart_player_select,
)
from frontend.i18n import t

def _friendly_metric(metric: str) -> str:
    names = {
        "cosine": t("scout_dist_cosine"),
        "euclidean": t("scout_dist_euclidean"),
        "hybrid": t("scout_dist_hybrid"),
    }
    return names.get(metric, metric)


def _render_results_table(results: pd.DataFrame):
    visible = results.rename(
        columns={
            "player": t("col_player"),
            "team": t("col_team"),
            "league": t("col_league"),
            "season": t("col_season"),
            "pos_": t("col_pos"),
            "nation_": t("col_nation"),
            "age_": t("col_age"),
            "Playing Time_Min": t("col_minutes"),
            "similarity_%": t("col_sim"),
        }
    )
    return st.dataframe(
        visible,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="scouting_results_table",
    )


def render_scouting_page(use_uefa: bool) -> None:
    df, dataset_name = active_dataset(use_uefa)
    engine = get_engine(dataset_name, df)
    search_df = df

    controls_col, content_col = st.columns([0.9, 3], gap="large")

    with controls_col:
        st.markdown(f"### {t('scout_params')}")
        target_player = smart_player_select(t("scout_target"), search_df, "scout_target")
        target_seasons = seasons_for_player(search_df, target_player)
        target_season = st.selectbox(t("scout_target_season"), target_seasons, key="target_season") if target_seasons else None

        all_seasons = sorted(search_df["season"].dropna().astype(str).unique(), reverse=True)
        result_seasons = st.multiselect(t("scout_result_seasons"), all_seasons, default=all_seasons[:1])

        team_filter = st.text_input(t("scout_team_filter"), placeholder=t("scout_team_ph"))
        min_minutes = st.slider(t("scout_min_minutes"), 0, 3500, 900, 50)
        top_n = st.slider(t("scout_num_results"), 3, 25, 10, 1)

        features = numeric_features(search_df)
        selected_features = st.multiselect(
            t("scout_specific_attrs"),
            features,
            default=[],
            format_func=metric_display_name,
            help=t("scout_specific_help"),
        )

        metric_label = st.selectbox(
            t("scout_dist_metric"),
            [t("scout_dist_hybrid"), t("scout_dist_cosine"), t("scout_dist_euclidean")],
        )
        metric_map = {
            t("scout_dist_cosine"): "cosine",
            t("scout_dist_euclidean"): "euclidean",
            t("scout_dist_hybrid"): "hybrid",
        }
        metric = metric_map[metric_label]
        alpha = st.slider(t("scout_alpha"), 0.0, 1.0, 0.5, 0.05, disabled=metric != "hybrid")
        run = st.button(t("scout_run_btn"), use_container_width=True)

    with content_col:
        st.title(t("scout_title"))
        st.caption(t("scout_caption"))

        metric_strip(
            [
                (t("exp_dataset"), dataset_name),
                (t("scout_mode"), t("scout_mode_pca") if not selected_features else t("scout_mode_specific")),
                (t("scout_dist"), _friendly_metric(metric)),
                (t("scout_min_minutes"), f"{min_minutes:,}"),
            ]
        )

        if not target_player:
            st.info(t("scout_no_target"))
            return

        if run:
            try:
                st.session_state["scouting_results"] = engine.find_similar_players(
                    target_player_name=target_player,
                    target_season=target_season,
                    result_seasons=result_seasons or None,
                    result_team=team_filter.strip() or None,
                    min_minutes=min_minutes,
                    features=selected_features or None,
                    metric=metric,
                    alpha=alpha,
                    top_n=top_n,
                )
                st.session_state["scouting_target"] = {
                    "player": target_player,
                    "season": target_season,
                    "features": selected_features,
                }
            except Exception as exc:
                st.error(f"{t('scout_error')} {exc}")

        results = st.session_state.get("scouting_results")
        target = st.session_state.get("scouting_target")
        if results is None:
            st.markdown(
                f"""
                <div class="info-note">
                    {t("scout_note")}
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        if results.empty:
            st.warning(t("scout_no_results"))
            return

        st.markdown(f'<div class="section-title">{t("scout_results_title")}</div>', unsafe_allow_html=True)
        event = _render_results_table(results)
        selected_rows = event.selection.rows if event and event.selection else []

        if selected_rows:
            candidate = results.iloc[selected_rows[0]]
        else:
            st.caption(t("scout_select_row"))
            candidate = results.iloc[0]

        default_compare_metrics = target.get("features") or preferred_radar_features(df)
        default_compare_metrics = [metric for metric in default_compare_metrics if metric in numeric_features(df)]
        compare_metrics = st.multiselect(
            t("scout_1v1_attrs"),
            numeric_features(df),
            default=default_compare_metrics,
            format_func=metric_display_name,
            help=t("scout_1v1_help"),
        )

        candidate_seasons = seasons_for_player(df, candidate["player"])
        
        col_cand1, col_cand2 = st.columns([1, 3])
        with col_cand1:
            if candidate_seasons:
                chosen_candidate_season = st.selectbox(
                    t("scout_season_of", player=candidate['player']),
                    candidate_seasons,
                    index=candidate_seasons.index(str(candidate["season"])) if str(candidate["season"]) in candidate_seasons else 0,
                    key="scouting_candidate_season"
                )
            else:
                chosen_candidate_season = candidate["season"]

        target_row = get_player_row(df, target["player"], target["season"])
        candidate_row = get_player_row(df, candidate["player"], chosen_candidate_season)
        render_player_comparison(df, target_row, candidate_row, compare_metrics or None)
