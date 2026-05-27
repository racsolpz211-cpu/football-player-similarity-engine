import streamlit as st


ACCENT_PRIMARY = "#1DE9B6"
ACCENT_SECONDARY = "#FF4FD8"
BACKGROUND = "#0E1117"
PANEL = "#1E2633"
PANEL_SOFT = "#151B26"
TEXT = "#E6EDF3"
MUTED = "#91A4B7"
BORDER = "#2B3A4F"


def apply_dark_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {{
            --bg: {BACKGROUND};
            --panel: {PANEL};
            --panel-soft: {PANEL_SOFT};
            --text: {TEXT};
            --muted: {MUTED};
            --border: {BORDER};
            --primary: {ACCENT_PRIMARY};
            --secondary: {ACCENT_SECONDARY};
        }}

        html, body, [class*="stApp"] {{
            background: var(--bg);
            color: var(--text);
            font-family: Inter, Roboto, Arial, sans-serif;
        }}

        .block-container {{
            max-width: 1320px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--text);
            letter-spacing: 0;
        }}

        p, label, span, div {{
            font-family: Inter, Roboto, Arial, sans-serif;
        }}

        [data-testid="stSidebar"] {{
            background: #0A0D12;
            border-right: 1px solid var(--border);
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label {{
            color: var(--text);
        }}

        .hero {{
            padding: 3rem 0 2rem 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.5rem;
        }}

        .eyebrow {{
            color: var(--primary);
            font-size: .78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .12rem;
            margin-bottom: .6rem;
        }}

        .hero h1 {{
            font-size: clamp(2.5rem, 7vw, 5.6rem);
            line-height: .95;
            margin: 0;
            font-weight: 800;
        }}

        .hero p {{
            max-width: 780px;
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.65;
            margin-top: 1.2rem;
        }}

        .panel {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.2rem;
        }}

        .metric-strip {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: .8rem;
            margin: 1rem 0 1.4rem 0;
        }}

        .metric-card {{
            background: var(--panel-soft);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: .95rem;
        }}

        .metric-card small {{
            color: var(--muted);
            display: block;
            margin-bottom: .35rem;
        }}

        .metric-card strong {{
            color: var(--text);
            font-size: 1.2rem;
        }}

        .section-title {{
            margin: .6rem 0 1rem;
            font-size: 1.25rem;
            font-weight: 700;
        }}

        .top-nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: .2rem 0 .6rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: .7rem;
        }}

        .brand {{
            font-weight: 800;
            color: var(--text);
            white-space: nowrap;
        }}

        .nav-title {{
            color: var(--primary);
            font-size: .76rem;
            font-weight: 800;
            letter-spacing: .12rem;
            text-transform: uppercase;
            margin: 0 0 .35rem;
        }}

        div[data-testid="stHorizontalBlock"] div[role="radiogroup"] {{
            display: flex;
            gap: .4rem;
        }}

        div[role="radiogroup"] label[data-baseweb="radio"] {{
            background: #101620;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: .45rem .75rem;
            min-height: 2.3rem;
        }}

        div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {{
            border-color: var(--primary);
            box-shadow: 0 0 0 1px rgba(29, 233, 182, .28);
        }}

        div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {{
            display: none;
        }}

        .search-option {{
            background: #101620;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: .65rem .8rem;
            margin: .35rem 0;
            color: var(--text);
        }}

        .search-option small {{
            color: var(--muted);
        }}

        .info-note {{
            color: var(--muted);
            background: rgba(29, 233, 182, .06);
            border: 1px solid rgba(29, 233, 182, .22);
            border-radius: 8px;
            padding: 1rem;
        }}

        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            overflow: hidden;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-size: .92rem;
        }}

        .comparison-table th {{
            background: #101620;
            color: var(--muted);
            padding: .72rem;
            text-align: center;
            font-weight: 700;
        }}

        .comparison-table td {{
            padding: .62rem .72rem;
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--text);
        }}

        .comparison-table td.metric-name {{
            color: var(--muted);
            font-weight: 600;
            width: 42%;
        }}

        .dominates-left {{
            color: var(--primary) !important;
            font-weight: 800;
        }}

        .dominates-right {{
            color: var(--secondary) !important;
            font-weight: 800;
        }}

        .stButton > button {{
            background: var(--primary);
            color: #05110E;
            border: 0;
            border-radius: 8px;
            font-weight: 800;
            min-height: 2.5rem;
        }}

        .stButton > button:hover {{
            background: #6FFFE2;
            color: #05110E;
            border: 0;
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        textarea,
        input {{
            background-color: #101620 !important;
            border-color: var(--border) !important;
            color: var(--text) !important;
            border-radius: 8px !important;
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }}

        hr {{
            border-color: var(--border);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Cyber-Scouting DSS</div>
            <h1>Football Player Similarity Engine</h1>
            <p>
                Plataforma analítica para localizar perfiles futbolísticos similares,
                comparar jugadores cara a cara y justificar cada recomendación con
                métricas, radar y lectura explicable de diferencias estadísticas.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_strip(items: list[tuple[str, str]]) -> None:
    cards = "".join(
        f'<div class="metric-card"><small>{label}</small><strong>{value}</strong></div>'
        for label, value in items
    )
    st.markdown(f'<div class="metric-strip">{cards}</div>', unsafe_allow_html=True)
