import streamlit as st

from frontend.pages.explorer_page import render_explorer_page
from frontend.pages.home_page import render_home_page
from frontend.pages.info_page import render_info_page
from frontend.pages.scouting_page import render_scouting_page
from frontend.styles import apply_dark_theme
from frontend.utils import load_scouting_datasets
from frontend.i18n import t

st.set_page_config(
    page_title="Football Player Similarity Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_dark_theme()

if "lang" not in st.session_state:
    st.session_state["lang"] = "es"

if "view" not in st.session_state:
    st.session_state["view"] = "nav_home"

# Map internal view names to translation keys
nav_items = ["nav_home", "nav_scouting", "nav_compare", "nav_info"]
if st.session_state["view"] == "nav_analysis":
    nav_items.append("nav_analysis")

with st.sidebar:
    st.markdown('<div class="nav-title" style="font-size: 1.2rem; margin-bottom: 1rem;">Football DSS</div>', unsafe_allow_html=True)
    
    st.markdown(f"### {t('menu_main')}")
    for item in nav_items:
        button_type = "primary" if st.session_state["view"] == item else "secondary"
        if st.button(t(item), type=button_type, use_container_width=True):
            st.session_state["view"] = item
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"### {t('menu_settings')}")
    
    lang_choice = st.radio("Language / Idioma", ["Español", "English"], index=0 if st.session_state["lang"] == "es" else 1, horizontal=True)
    new_lang = "es" if lang_choice == "Español" else "en"
    if new_lang != st.session_state["lang"]:
        st.session_state["lang"] = new_lang
        st.rerun()

    use_uefa = st.toggle(t("toggle_uefa"), value=True, help=t("toggle_uefa_help"))

try:
    load_scouting_datasets()
except FileNotFoundError as exc:
    st.error(f"{t('error_datasets')} {exc}")
    st.stop()

if st.session_state["view"] == "nav_home":
    render_home_page(use_uefa)
elif st.session_state["view"] == "nav_scouting":
    render_scouting_page(use_uefa)
elif st.session_state["view"] == "nav_compare":
    render_explorer_page(use_uefa)
elif st.session_state["view"] == "nav_analysis":
    from frontend.pages.analysis_page import render_analysis_page
    render_analysis_page(use_uefa)
else:
    render_info_page()
