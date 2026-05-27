import streamlit as st

from frontend.components.radar_chart import build_radar_chart
from frontend.styles import metric_strip
from frontend.utils import (
    active_dataset,
    get_player_row,
    numeric_features,
    preferred_radar_features,
    player_numeric_stats,
    metric_display_name
)
from frontend.i18n import t

def render_analysis_page(use_uefa: bool) -> None:
    df, dataset_name = active_dataset(use_uefa)
    
    player = st.session_state.get("analysis_player")
    season = st.session_state.get("analysis_season")
    
    if not player or not season:
        st.warning(t("ana_no_player"))
        if st.button(t("ana_back_btn")):
            st.session_state["view"] = "nav_home"
            st.rerun()
        return
    from frontend.utils import seasons_for_player
    
    seasons = seasons_for_player(df, player)
    if not seasons:
        st.error(t("ana_no_seasons", player=player))
        return

    season = st.selectbox(
        t("ana_select_season"), 
        seasons, 
        index=seasons.index(season) if season in seasons else 0,
        key="analysis_season_select"
    )
    
    if season != st.session_state.get("analysis_season"):
        st.session_state["analysis_season"] = season
        st.rerun()

    row = get_player_row(df, player, season)
    
    if row is None:
        st.error(t("ana_no_data", player=player, season=season))
        return

    st.title(t("ana_title", player=player))
    
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
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    default_metrics = preferred_radar_features(df)
    default_metrics = [m for m in default_metrics if m in numeric_features(df)]
    
    with col1:
        st.markdown(f'<div class="section-title">{t("ana_radar_title")}</div>', unsafe_allow_html=True)
        selected_metrics = st.multiselect(
            t("ana_radar_select"),
            numeric_features(df),
            default=default_metrics,
            format_func=metric_display_name
        )
        if selected_metrics:
            fig = build_radar_chart(df, row, None, selected_metrics)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t("ana_radar_info"))
            
    with col2:
        st.markdown(f'<div class="section-title">{t("ana_stats_title")}</div>', unsafe_allow_html=True)
        stats = player_numeric_stats(row, numeric_features(df), limit=100)
        st.dataframe(stats, use_container_width=True, hide_index=True, height=500)
