import streamlit as st

from frontend.styles import render_hero, metric_strip
from frontend.utils import active_dataset, get_player_row, numeric_features, player_numeric_stats, seasons_for_player, smart_player_select
from frontend.i18n import t

def render_home_page(use_uefa: bool) -> None:
    df, dataset_name = active_dataset(use_uefa)
    render_hero()

    metric_strip(
        [
            (t("home_players_season"), f"{len(df):,}"),
            (t("home_unique_players"), f"{df['player'].nunique():,}"),
            (t("home_seasons"), f"{df['season'].nunique():,}"),
            (t("home_active_dataset"), dataset_name),
        ]
    )

    st.markdown(f'<div class="section-title">{t("home_search_title")}</div>', unsafe_allow_html=True)
    player = smart_player_select(t("home_player"), df, "home_player")
    seasons = seasons_for_player(df, player)

    if player and seasons:
        season = st.selectbox(t("home_season"), seasons, key="home_season")
        row = get_player_row(df, player, season)
        if row is not None:
            minutes = int(row.get("Playing Time_Min", 0))
            st.markdown(
                f"""
                <div class="panel">
                    <strong>{row.get('player')}</strong><br>
                    <span style="color:#91A4B7">
                        {row.get('team')} · {row.get('league')} · {row.get('season')} ·
                        {row.get('pos_', 'N/D')} · {minutes:,} {t("home_minutes").lower()}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f'<div class="section-title">{t("home_summary_title")}</div>', unsafe_allow_html=True)
            stat_cols = st.columns(4)
            stat_cols[0].metric(t("home_minutes"), f"{minutes:,}")
            stat_cols[1].metric(t("home_age"), row.get("age_", "N/D"))
            stat_cols[2].metric(t("home_matches"), row.get("Playing Time_MP", "N/D"))
            stat_cols[3].metric(t("home_starts"), row.get("Playing Time_Starts", "N/D"))

            stats = player_numeric_stats(row, numeric_features(df), limit=80)
            st.dataframe(stats, use_container_width=True, hide_index=True)
            
            if st.button(t("home_analyze_btn"), type="primary", use_container_width=True):
                st.session_state["view"] = "nav_analysis"
                st.session_state["analysis_player"] = player
                st.session_state["analysis_season"] = season
                st.rerun()
    else:
        st.markdown(
            f"""
            <div class="info-note">
                {t("home_empty_search")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    left, middle, right = st.columns(3)
    with left:
        if st.button(t("home_go_scouting"), key="home_go_scouting", use_container_width=True):
            st.session_state["view"] = "nav_scouting"
            st.rerun()
    with middle:
        if st.button(t("home_go_compare"), key="home_go_compare", use_container_width=True):
            st.session_state["view"] = "nav_compare"
            st.rerun()
    with right:
        if st.button(t("home_go_info"), key="home_go_info", use_container_width=True):
            st.session_state["view"] = "nav_info"
            st.rerun()

    st.markdown(
        f"""
        <div class="info-note">
            {t("home_note")}
        </div>
        """,
        unsafe_allow_html=True,
    )
