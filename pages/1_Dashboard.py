import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        background: #f8f9fa !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Strip ALL streamlit padding */
    [data-testid="stMainBlockContainer"],
    [data-testid="stAppViewBlockContainer"],
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        background: #f8f9fa !important;
    }

    /* ========== HEADER ========== */
    .header {
        padding: 3rem 5rem;
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 188, 212, 0.2);
        margin-bottom: 2.5rem;
    }

    .header::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(0,188,212,0.2) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255,255,255,0.08) 0%, transparent 50%);
        pointer-events: none;
    }

    .header h1 { margin: 0; font-size: 2.6rem; font-weight: 900; letter-spacing: -1px; position: relative; z-index: 1; color: white !important; }
    .header p  { margin: 0.7rem 0 0; opacity: 0.95; font-size: 1.05rem; font-weight: 300; position: relative; z-index: 1; color: white !important; }

    /* ========== CONTENT WRAPPER ========== */
    /* We pad each section individually so Streamlit columns don't break */
    .padded { padding: 0 5rem; }

    /* ========== IMPACT EXPLAINER ========== */
    .impact-explainer {
        background: white;
        border-left: 5px solid #00bcd4;
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin: 0 5rem 1.8rem;
        box-shadow: 0 4px 15px rgba(0,188,212,0.08);
        border: 1px solid rgba(0,188,212,0.15);
        display: flex;
        align-items: center;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .impact-explainer .formula {
        font-size: 1rem;
        font-weight: 800;
        color: #0d47a1;
        background: rgba(0,188,212,0.1);
        padding: 0.5rem 1.1rem;
        border-radius: 8px;
        white-space: nowrap;
    }

    .impact-explainer .explanation {
        font-size: 0.9rem;
        color: #444;
        line-height: 1.6;
    }

    .impact-explainer .explanation strong { color: #0d47a1; }

    /* ========== PARADOX BANNER ========== */
    .paradox-wrap { padding: 0 5rem; margin-bottom: 1.8rem; }

    .paradox-banner {
        background: linear-gradient(135deg, rgba(13,71,161,0.05) 0%, rgba(0,188,212,0.08) 100%);
        border: 1px solid rgba(0,188,212,0.2);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        display: flex;
        gap: 1rem;
        align-items: center;
        flex-wrap: wrap;
    }

    .paradox-title { width: 100%; font-size: 0.95rem; font-weight: 700; color: #0d47a1; margin-bottom: 0.5rem; }

    .paradox-stat {
        flex: 1; min-width: 160px; text-align: center;
        padding: 1rem; background: white; border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,188,212,0.08);
    }

    .paradox-stat .p-value { font-size: 1.7rem; font-weight: 900; color: #0d47a1; }
    .paradox-stat .p-label { font-size: 0.78rem; color: #666; margin-top: 0.3rem; line-height: 1.4; }
    .paradox-arrow { font-size: 1.4rem; color: #00bcd4; }

    /* ========== FILTER SECTION ========== */
    .filter-wrap { padding: 0 5rem; margin-bottom: 1.8rem; }

    .filter-section {
        background: white;
        padding: 1.8rem 2rem;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,188,212,0.08);
        border: 1px solid rgba(0,188,212,0.12);
    }

    .filter-title { font-size: 1rem; font-weight: 700; color: #0d47a1; margin-bottom: 1rem; }

    /* ========== TOP PERFORMER — pure inline styles used for reliability ========== */
    .top-performer-wrap { padding: 0 5rem; margin-bottom: 1.8rem; }

    /* ========== METRIC CARDS inside top performer (rendered via st.columns) ========== */
    .pm-card {
        background: rgba(255,255,255,0.15) !important;
        padding: 1.2rem 1.4rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.25);
        height: 100%;
    }

    .pm-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        color: rgba(255,255,255,0.85) !important;
        margin-bottom: 0.4rem;
    }

    .pm-value {
        font-size: 1.5rem;
        font-weight: 900;
        color: #ffffff !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .pm-sub {
        font-size: 0.72rem;
        color: rgba(255,255,255,0.7) !important;
        margin-top: 0.25rem;
    }

    /* ========== DATA SECTION ========== */
    .data-wrap { padding: 0 5rem; margin-bottom: 2rem; }

    .data-section {
        background: white;
        padding: 2rem;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,188,212,0.08);
        border: 1px solid rgba(0,188,212,0.12);
    }

    .data-section h2 { margin: 0 0 1.2rem; color: #0d47a1; font-size: 1.3rem; font-weight: 800; }

    /* ========== TABLE ========== */
    [data-testid="stDataFrame"] th {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%) !important;
        color: white !important; font-weight: 700 !important;
        text-transform: uppercase !important; font-size: 0.8rem !important;
    }
    [data-testid="stDataFrame"] td {
        padding: 0.85rem 1rem !important;
        border-bottom: 1px solid rgba(0,188,212,0.1) !important;
        color: #222 !important;
    }

    /* ========== NO RESULTS ========== */
    .no-results {
        padding: 2.5rem; border-radius: 14px; text-align: center;
        color: #d32f2f; border: 1px solid rgba(244,67,54,0.2);
        background: rgba(244,67,54,0.05);
    }

    /* ========== INPUTS ========== */
    .stTextInput > div > div > input {
        border: 1.5px solid rgba(0,188,212,0.3) !important;
        border-radius: 8px !important; padding: 0.7rem 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00bcd4 !important;
        box-shadow: 0 0 0 3px rgba(0,188,212,0.1) !important;
    }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 1024px) {
        .header, .impact-explainer, .paradox-wrap,
        .filter-wrap, .top-performer-wrap, .data-wrap { padding-left: 2.5rem !important; padding-right: 2.5rem !important; }
    }
    @media (max-width: 768px) {
        .header { padding: 2rem 1.5rem !important; }
        .impact-explainer, .paradox-wrap, .filter-wrap,
        .top-performer-wrap, .data-wrap { padding-left: 1.2rem !important; padding-right: 1.2rem !important; }
        .header h1 { font-size: 1.8rem !important; }
        .paradox-arrow { display: none; }
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Load & Prepare Data ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data_cleaned.csv")
    df['Impact Score'] = (df['Eng Rate'] * np.log10(df['Followers'])).round(2)
    return df

df = load_data()

top25_eng    = df[df['Followers'] >= df['Followers'].quantile(0.75)]['Eng Rate'].mean()
bottom25_eng = df[df['Followers'] <= df['Followers'].quantile(0.25)]['Eng Rate'].mean()
multiplier   = bottom25_eng / top25_eng

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <h1>📊 Influencer Impact Dashboard</h1>
    <p>Search, filter, and analyze influencer impact — beyond just follower count</p>
</div>
""", unsafe_allow_html=True)

# ── Impact Score Explainer ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="impact-explainer">
    <div class="formula">📐 Impact Score = Engagement Rate × log₁₀(Followers)</div>
    <div class="explanation">
        A creator with <strong>500K followers &amp; 8% engagement</strong> scores higher than one with
        <strong>50M followers &amp; 0.3% engagement</strong> —
        because <strong>quality of influence matters more than quantity.</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Paradox Banner ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="paradox-wrap">
<div class="paradox-banner">
    <div class="paradox-title">⚡ The Influence Paradox — What the data reveals:</div>
    <div class="paradox-stat">
        <div class="p-value">{top25_eng:.2f}%</div>
        <div class="p-label">Avg engagement<br><strong>Top 25% most followed</strong></div>
    </div>
    <div class="paradox-arrow">→</div>
    <div class="paradox-stat">
        <div class="p-value">{bottom25_eng:.2f}%</div>
        <div class="p-label">Avg engagement<br><strong>Bottom 25% by followers</strong></div>
    </div>
    <div class="paradox-arrow">→</div>
    <div class="paradox-stat">
        <div class="p-value" style="color:#e53935;">{multiplier:.1f}x</div>
        <div class="p-label">Smaller influencers are<br><strong>more engaging</strong></div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# ── Filter Section ─────────────────────────────────────────────────────────────
st.markdown('<div class="filter-wrap"><div class="filter-section">', unsafe_allow_html=True)
st.markdown('<div class="filter-title">🔍 Search & Filter</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    search_name = st.text_input("name", placeholder="e.g., instagram, cristiano...", label_visibility="collapsed")
with col2:
    category_filter = st.selectbox("category", ["All"] + sorted(df['Category'].dropna().unique().tolist()), label_visibility="collapsed")
with col3:
    sort_by = st.selectbox("sort", ["Impact Score", "Engagement Rate", "Followers", "Posts", "Avg Likes"], label_visibility="collapsed")

st.markdown('</div></div>', unsafe_allow_html=True)

# ── Filter & Sort ──────────────────────────────────────────────────────────────
filtered_df = df.copy()
if search_name:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]
if category_filter != "All":
    filtered_df = filtered_df[filtered_df['Category'] == category_filter]

sort_map = {"Impact Score": "Impact Score", "Engagement Rate": "Eng Rate",
            "Followers": "Followers", "Posts": "Posts", "Avg Likes": "Avg. Likes"}
filtered_df = filtered_df.sort_values(sort_map[sort_by], ascending=False)

# ── Top Performer ──────────────────────────────────────────────────────────────
if len(filtered_df) > 0:
    top = filtered_df.iloc[0]
    impact_pct = (top['Impact Score'] / df['Impact Score'].max()) * 100
    tier = "🔥 Elite" if impact_pct >= 80 else ("⭐ High" if impact_pct >= 50 else "📈 Rising")
    cat  = top['Category'] if pd.notna(top['Category']) else 'N/A'

    st.markdown('<div class="top-performer-wrap">', unsafe_allow_html=True)

    # The gradient box using a full inline-styled div — most reliable approach
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        padding: 2rem 2.2rem 1.5rem;
        border-radius: 14px;
        box-shadow: 0 10px 40px rgba(0,188,212,0.25);
        margin-bottom: 0.5rem;
    ">
        <div style="font-size:1.4rem; font-weight:800; color:#fff; margin-bottom:1.2rem;">
            🏆 Top Performer
            <span style="font-size:0.9rem; font-weight:400; opacity:0.75; margin-left:0.6rem;">
                — sorted by {sort_by}
            </span>
        </div>
        <div style="display:grid; grid-template-columns:repeat(5,1fr); gap:1rem;">
            <div style="background:rgba(255,255,255,0.14); padding:1rem 1.2rem; border-radius:10px; border:1px solid rgba(255,255,255,0.2);">
                <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; color:rgba(255,255,255,0.8); margin-bottom:0.3rem;">Name</div>
                <div style="font-size:1.1rem; font-weight:900; color:#fff; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{top['name']}</div>
                <div style="font-size:0.7rem; color:rgba(255,255,255,0.65); margin-top:0.2rem;">{cat}</div>
            </div>
            <div style="background:rgba(255,255,255,0.14); padding:1rem 1.2rem; border-radius:10px; border:1px solid rgba(255,255,255,0.2);">
                <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; color:rgba(255,255,255,0.8); margin-bottom:0.3rem;">Followers</div>
                <div style="font-size:1.5rem; font-weight:900; color:#fff;">{int(top['Followers']/1_000_000)}M</div>
                <div style="font-size:0.7rem; color:rgba(255,255,255,0.65); margin-top:0.2rem;">Total reach</div>
            </div>
            <div style="background:rgba(255,255,255,0.14); padding:1rem 1.2rem; border-radius:10px; border:1px solid rgba(255,255,255,0.2);">
                <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; color:rgba(255,255,255,0.8); margin-bottom:0.3rem;">Avg Likes</div>
                <div style="font-size:1.5rem; font-weight:900; color:#fff;">{int(top['Avg. Likes']):,}</div>
                <div style="font-size:0.7rem; color:rgba(255,255,255,0.65); margin-top:0.2rem;">Per post</div>
            </div>
            <div style="background:rgba(255,255,255,0.14); padding:1rem 1.2rem; border-radius:10px; border:1px solid rgba(255,255,255,0.2);">
                <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; color:rgba(255,255,255,0.8); margin-bottom:0.3rem;">Engagement</div>
                <div style="font-size:1.5rem; font-weight:900; color:#fff;">{top['Eng Rate']:.2f}%</div>
                <div style="font-size:0.7rem; color:rgba(255,255,255,0.65); margin-top:0.2rem;">Audience activity</div>
            </div>
            <div style="background:rgba(255,255,255,0.22); padding:1rem 1.2rem; border-radius:10px; border:1.5px solid rgba(255,255,255,0.4);">
                <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; color:rgba(255,255,255,0.8); margin-bottom:0.3rem;">⚡ Impact Score</div>
                <div style="font-size:1.5rem; font-weight:900; color:#fff;">{top['Impact Score']}</div>
                <div style="font-size:0.7rem; color:rgba(255,255,255,0.65); margin-top:0.2rem;">{tier}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Data Table ─────────────────────────────────────────────────────────────────
st.markdown('<div class="data-wrap"><div class="data-section">', unsafe_allow_html=True)

if len(filtered_df) > 0:
    st.markdown(f'<h2>📋 Results ({len(filtered_df)} found)</h2>', unsafe_allow_html=True)
    display_df = filtered_df[['rank','name','Category','Followers','Avg. Likes','Eng Rate','Impact Score']].copy()
    display_df['Followers'] = (display_df['Followers']/1_000_000).round(1).astype(str) + 'M'
    display_df.columns = ['Rank','Name','Category','Followers','Avg Likes','Engagement %','⚡ Impact Score']
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.markdown("""
    <div class="no-results">
        <h3>😕 No Results Found</h3>
        <p>Try adjusting your search filters or category selection</p>
    </div>""", unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
st.markdown('<div style="margin-top:3rem;"></div>', unsafe_allow_html=True)