import streamlit as st
from frontend.i18n import t

def render_info_page() -> None:
    css = """
<style>
.info-page-container {
    font-family: Inter, Roboto, Arial, sans-serif;
    color: var(--text);
    margin-top: -1rem;
}

.info-hero {
    padding-bottom: 2.5rem;
    margin-bottom: 2rem;
}

.info-hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
    margin: 0 0 0.8rem 0;
    line-height: 1.1;
    letter-spacing: -0.02em;
}

.info-hero p {
    color: var(--text);
    font-size: 1.1rem;
    line-height: 1.6;
    max-width: 850px;
    margin: 0;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.2rem;
    margin-top: 2rem;
}

.section-header h2 {
    font-size: 1.3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.01em;
}

.grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
}

.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.2rem;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.2rem;
}

.info-card {
    background: var(--panel-soft);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}

.info-card.border-secondary { border-color: rgba(255, 79, 216, 0.4); }

.card-icon {
    width: 24px;
    height: 24px;
    margin-bottom: 1.2rem;
}

.card-icon.primary { color: var(--primary); }
.card-icon.secondary { color: var(--secondary); }
.card-icon.white { color: #FFFFFF; }

.card-title {
    font-weight: 800;
    font-size: 1rem;
    margin-bottom: 0.8rem;
}

.text-primary { color: var(--primary); }
.text-secondary { color: var(--secondary); }
.text-white { color: #FFFFFF; }

.card-desc {
    color: var(--muted);
    font-size: 0.88rem;
    line-height: 1.6;
    flex-grow: 1;
}

.tags-container {
    display: flex;
    gap: 0.5rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}

.tag {
    background: rgba(255, 255, 255, 0.08);
    padding: 0.35rem 0.6rem;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #C0C5CE;
    text-transform: uppercase;
}

.mode-card {
    background: #11151E;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 2.2rem;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.mode-card.primary { border-color: rgba(255, 79, 216, 0.5); }
.mode-card.secondary { border-color: rgba(29, 233, 182, 0.5); }

.mode-title {
    font-size: 1.4rem;
    font-weight: 800;
    margin-bottom: 1rem;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}

.mode-icon {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    opacity: 0.25;
    width: 52px;
    height: 52px;
}

.alpha-bar {
    margin-top: 1.8rem;
    width: 100%;
}

.alpha-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.65rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.alpha-labels .left { color: var(--primary); }
.alpha-labels .right { color: var(--secondary); }

.alpha-track {
    height: 4px;
    background: linear-gradient(to right, var(--primary) 50%, var(--secondary) 50%);
    border-radius: 2px;
    position: relative;
}

.alpha-thumb {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 12px;
    height: 12px;
    background: #FFFFFF;
    border-radius: 50%;
}

.alpha-val {
    text-align: center;
    font-size: 0.75rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-top: 0.6rem;
}

.phase-desc {
    color: var(--text);
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
    margin-top: 0;
}
</style>
"""

    html = f"""
<div class="info-page-container">
<div class="info-hero">
<h1>{t('info_hero_title')}</h1>
<p>{t('info_hero_desc')}</p>
</div>

<!-- FASE 1 -->
<div class="section-header">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
<h2>{t('info_f1_title')}</h2>
</div>
<p class="phase-desc">{t('info_f1_desc1')}</p>

<div class="grid-2">
    <div class="info-card">
        <svg class="card-icon primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        <div class="card-desc">{t('info_f1_li1')}</div>
    </div>
    <div class="info-card">
        <svg class="card-icon primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path><path d="M2 12h20"></path></svg>
        <div class="card-desc">{t('info_f1_li2')}</div>
    </div>
</div>

<!-- FASE 2 -->
<div class="section-header">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
<h2>{t('info_f2_title')}</h2>
</div>
<p class="phase-desc">{t('info_f2_desc1')}</p>

<div class="grid-3">
    <div class="info-card">
        <div class="card-desc">{t('info_f2_li1')}</div>
    </div>
    <div class="info-card">
        <div class="card-desc">{t('info_f2_li2')}</div>
    </div>
    <div class="info-card">
        <div class="card-desc">{t('info_f2_li3')}</div>
    </div>
</div>

<!-- FASE 3 -->
<div class="section-header">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
<h2>{t('info_f3_title')}</h2>
</div>
<p class="phase-desc">{t('info_f3_desc1')}</p>

<div class="grid-3">
    <div class="info-card">
        <svg class="card-icon primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        <div class="card-desc">{t('info_f3_li1')}</div>
    </div>
    <div class="info-card">
        <svg class="card-icon primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"></path><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path></svg>
        <div class="card-desc">{t('info_f3_li2')}</div>
    </div>
    <div class="info-card">
        <svg class="card-icon primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        <div class="card-desc">{t('info_f3_li3')}</div>
    </div>
</div>

<!-- FASE 4 -->
<div class="section-header">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--secondary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="4"></circle><line x1="12" y1="2" x2="12" y2="8"></line><line x1="12" y1="16" x2="12" y2="22"></line><line x1="2" y1="12" x2="8" y2="12"></line><line x1="16" y1="12" x2="22" y2="12"></line></svg>
<h2>{t('info_f4_title')}</h2>
</div>
<p class="phase-desc">{t('info_f4_desc1')}</p>

<div class="grid-3">
    <div class="mode-card primary" style="padding: 1.5rem;">
        <div class="mode-title" style="font-size: 1.1rem; margin-bottom:0.5rem;">StandardScaler</div>
        <div class="card-desc" style="color: rgba(255,255,255,0.8);">{t('info_f4_li1').replace('<strong>1. StandardScaler (Poniendo todo en la misma escala):</strong> ', '').replace('<strong>1. StandardScaler (Putting everything on the same scale):</strong> ', '')}</div>
    </div>
    <div class="mode-card secondary" style="padding: 1.5rem;">
        <div class="mode-title" style="font-size: 1.1rem; margin-bottom:0.5rem;">PCA</div>
        <div class="card-desc" style="color: rgba(255,255,255,0.8);">{t('info_f4_li2').replace('<strong>2. PCA (Análisis de Componentes Principales):</strong> ', '').replace('<strong>2. PCA (Principal Component Analysis):</strong> ', '')}</div>
    </div>
    <div class="mode-card" style="padding: 1.5rem; border-color: rgba(150, 150, 150, 0.5);">
        <div class="mode-title" style="font-size: 1.1rem; margin-bottom:0.5rem;">K-NN Search</div>
        <div class="card-desc" style="color: rgba(255,255,255,0.8);">{t('info_f4_li3').replace('<strong>3. Búsqueda de Similitudes (La filosofía K-NN):</strong> ', '').replace('<strong>3. Similarity Search (The K-NN Philosophy):</strong> ', '')}</div>
    </div>
</div>

<!-- FASE 5 -->
<div class="section-header">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#E6EDF3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
<h2>{t('info_f5_title')}</h2>
</div>
<p class="phase-desc">{t('info_f5_desc1')}</p>

<div class="grid-3">
    <div class="info-card">
        <svg class="card-icon primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 22h20L12 2z"></path></svg>
        <div class="card-title text-primary">{t('info_f5_card1_title')}</div>
        <div class="card-desc">{t('info_f5_card1_desc')}</div>
    </div>
    <div class="info-card">
        <svg class="card-icon secondary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="12" x2="16" y2="12"></line><circle cx="20" cy="12" r="2"></circle></svg>
        <div class="card-title text-secondary">{t('info_f5_card2_title')}</div>
        <div class="card-desc">{t('info_f5_card2_desc')}</div>
    </div>
    <div class="info-card border-secondary">
        <svg class="card-icon white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg>
        <div class="card-title text-white">{t('info_f5_card3_title')}</div>
        <div class="card-desc">{t('info_f5_card3_desc')}</div>
        <div class="alpha-bar">
            <div class="alpha-labels">
                <span class="left">STYLE</span>
                <span class="right">VOLUME</span>
            </div>
            <div class="alpha-track">
                <div class="alpha-thumb"></div>
            </div>
            <div class="alpha-val">α = 0.5</div>
        </div>
    </div>
</div>
</div>
    """
    
    clean_css = "\n".join(line.lstrip() for line in css.split('\n'))
    clean_html = "\n".join(line.lstrip() for line in html.split('\n'))
    
    st.markdown(clean_css + clean_html, unsafe_allow_html=True)

