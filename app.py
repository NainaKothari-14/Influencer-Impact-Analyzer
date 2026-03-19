import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Influencer Impact Analyzer", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        background: #f8f9fa !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    [data-testid="stMainBlockContainer"], .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        background: #f8f9fa !important;
    }

    /* ========== HERO ========== */
    .hero {
        padding: 5rem 4rem;
        background: linear-gradient(135deg, rgba(13,71,161,0.93) 0%, rgba(25,118,210,0.88) 50%, rgba(0,188,212,0.82) 100%),
                    url('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1400&h=700&fit=crop') center/cover;
        min-height: 420px;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        text-align: center; color: white;
        position: relative; overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,188,212,0.2);
    }

    .hero::before {
        content: ''; position: absolute; inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(0,188,212,0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(13,71,161,0.1) 0%, transparent 50%);
        pointer-events: none;
    }

    .hero-content { position: relative; z-index: 2; }
    .hero-badge {
        display: inline-block; margin-bottom: 1.2rem;
        background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
        color: white; font-size: 0.82rem; font-weight: 700;
        padding: 0.4rem 1.2rem; border-radius: 20px;
        text-transform: uppercase; letter-spacing: 1.5px;
    }
    .hero h1 {
        font-size: 3.6rem; font-weight: 900; margin-bottom: 1.2rem;
        letter-spacing: -2px; color: white !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .hero p {
        font-size: 1.2rem; font-weight: 400; max-width: 650px;
        line-height: 1.7; color: rgba(255,255,255,0.95) !important;
    }

    /* ========== SECTION ========== */
    .section-title {
        font-size: 1.8rem; font-weight: 900; color: #0d47a1;
        letter-spacing: -0.5px; margin-bottom: 0.4rem;
    }
    .section-sub { font-size: 0.95rem; color: #666; margin-bottom: 2rem; line-height: 1.6; }

    /* ========== INFLUENCER CARD ========== */
    .inf-card {
        background: white; border-radius: 16px; overflow: hidden;
        box-shadow: 0 4px 15px rgba(13,71,161,0.08);
        border: 1px solid rgba(0,188,212,0.12);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    .inf-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0,188,212,0.25);
        border-color: rgba(0,188,212,0.4);
    }

    .inf-photo-wrap {
        position: relative; height: 200px; overflow: hidden;
    }

    .inf-photo {
        width: 100%; height: 200px;
        object-fit: cover; object-position: center top;
        display: block;
        transition: transform 0.4s ease;
    }
    .inf-card:hover .inf-photo { transform: scale(1.05); }

    /* Overlay on photo */
    .inf-photo-overlay {
        position: absolute; inset: 0;
        background: linear-gradient(180deg, transparent 40%, rgba(13,71,161,0.7) 100%);
    }

    /* Rank badge on photo */
    .inf-rank {
        position: absolute; top: 10px; left: 10px;
        background: rgba(13,71,161,0.9); color: white;
        font-size: 0.72rem; font-weight: 800; padding: 0.3rem 0.7rem;
        border-radius: 20px; letter-spacing: 0.5px;
        backdrop-filter: blur(4px);
    }

    /* Impact badge on photo */
    .inf-impact-badge {
        position: absolute; bottom: 10px; right: 10px;
        background: rgba(0,188,212,0.92); color: white;
        font-size: 0.78rem; font-weight: 800; padding: 0.3rem 0.8rem;
        border-radius: 20px; backdrop-filter: blur(4px);
    }

    .inf-body { padding: 1.3rem 1.5rem; }
    .inf-name { font-size: 1.1rem; font-weight: 800; color: #0d47a1; margin-bottom: 0.25rem; letter-spacing: -0.3px; }
    .inf-category { font-size: 0.73rem; color: #00838f; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.9rem; }
    .inf-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
    .inf-stat { background: rgba(0,188,212,0.07); border-radius: 8px; padding: 0.6rem 0.8rem; border-left: 3px solid #00bcd4; }
    .inf-stat-label { font-size: 0.65rem; color: #1976d2; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; margin-bottom: 0.15rem; }
    .inf-stat-value { font-size: 0.95rem; font-weight: 900; color: #0d47a1; }

    /* ========== METRICS ========== */
    .metric-card {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        padding: 2rem; border-radius: 14px; color: white;
        text-align: center; position: relative; overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,188,212,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card::before {
        content: ''; position: absolute; inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.12) 0%, transparent 60%);
        pointer-events: none;
    }
    .metric-card:hover { transform: translateY(-6px); box-shadow: 0 18px 45px rgba(0,188,212,0.3); }
    .metric-number { font-size: 2.4rem; font-weight: 900; color: white !important; display: block; position: relative; z-index: 1; }
    .metric-text   { font-size: 0.82rem; font-weight: 600; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; color: white !important; position: relative; z-index: 1; }

    /* ========== CTA ========== */
    .cta {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        padding: 4rem; border-radius: 20px; text-align: center; color: white;
        position: relative; overflow: hidden;
        box-shadow: 0 15px 50px rgba(0,188,212,0.25);
    }
    .cta::before {
        content: ''; position: absolute; inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(0,188,212,0.2) 0%, transparent 50%);
        pointer-events: none;
    }
    .cta h2 { font-size: 2.2rem; margin-bottom: 1rem; font-weight: 800; letter-spacing: -1px; position: relative; z-index: 1; color: white !important; }
    .cta p  { font-size: 1.05rem; opacity: 0.9; margin-bottom: 2rem; position: relative; z-index: 1; color: white !important; }

    .stButton > button {
        background: linear-gradient(135deg, #00bcd4 0%, #0097a7 100%) !important;
        color: white !important; padding: 0.9rem 2.5rem !important;
        font-size: 0.95rem !important; font-weight: 700 !important;
        border: none !important; border-radius: 50px !important;
        box-shadow: 0 8px 25px rgba(0,188,212,0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important; letter-spacing: 1.5px !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(0,188,212,0.5) !important;
    }

    .footer {
        text-align: center; padding: 2.5rem; color: #999;
        font-size: 0.88rem; border-top: 1px solid rgba(0,188,212,0.1);
    }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 1024px) {
        .hero { padding: 4rem 2.5rem; }
    }
    @media (max-width: 768px) {
        .hero { padding: 3rem 1.5rem; min-height: 320px; }
        .hero h1 { font-size: 2.2rem; }
        .inf-photo, .inf-photo-wrap { height: 160px; }
        .cta { padding: 2.5rem 1.5rem; }
        .cta h2 { font-size: 1.6rem; }
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data_cleaned.csv")
    df['Impact Score'] = (df['Eng Rate'] * np.log10(df['Followers'])).round(2)
    return df

df = load_data()

# ── Category → Unsplash photo pool (all reliable, no login needed) ─────────────
CATEGORY_PHOTOS = {
    "entertainment": [
        "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=600&h=400&fit=crop",
    ],
    "sports": [
        "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1526676037777-05a232554f77?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1565992441121-4367d2a52691?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1518091043644-c1d4457512c6?w=600&h=400&fit=crop",
    ],
    "fashion": [
        "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1445205170230-053b83016050?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600&h=400&fit=crop",
    ],
    "fitness": [
        "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1549060279-7e168fcee0c2?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1590487988256-9ed24133863e?w=600&h=400&fit=crop",
    ],
    "music": [
        "https://images.unsplash.com/photo-1511379938547-c1f69b13d835?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1468164016595-6108e4c60c8b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1571330735066-03aaa9429d89?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1501612780327-45045538702b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=600&h=400&fit=crop",
    ],
    "beauty": [
        "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1519415510236-718bdfcd89c8?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1503236823255-94609f598e71?w=600&h=400&fit=crop",
    ],
    "travel": [
        "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1501555088652-021faa106b9b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1503220317375-aaad61436b1b?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1527631746610-bca00a040d60?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1473625247510-8ceb1760943f?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1500835556837-99ac94a94552?w=600&h=400&fit=crop",
    ],
    "food": [
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&h=400&fit=crop",
    ],
    "default": [
        "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=600&h=400&fit=crop",
    ]
}

def get_photo_for(name, category, idx):
    """Pick a consistent photo based on category and index."""
    cat = str(category).lower() if pd.notna(category) else ""

    if "sport" in cat or "football" in cat or "cricket" in cat or "fitness" in cat and "health" in cat:
        pool = CATEGORY_PHOTOS["sports"]
    elif "fashion" in cat:
        pool = CATEGORY_PHOTOS["fashion"]
    elif "fitness" in cat or "health" in cat:
        pool = CATEGORY_PHOTOS["fitness"]
    elif "music" in cat or "sing" in cat:
        pool = CATEGORY_PHOTOS["music"]
    elif "beauty" in cat or "makeup" in cat:
        pool = CATEGORY_PHOTOS["beauty"]
    elif "travel" in cat:
        pool = CATEGORY_PHOTOS["travel"]
    elif "food" in cat or "cook" in cat:
        pool = CATEGORY_PHOTOS["food"]
    elif "entertain" in cat or "comedy" in cat or "actor" in cat:
        pool = CATEGORY_PHOTOS["entertainment"]
    else:
        pool = CATEGORY_PHOTOS["default"]

    return pool[idx % len(pool)]

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-badge">⚡ Impact Score Powered</div>
        <h1>Influencer Impact Analyzer</h1>
        <p>Discover & analyze the top 200 Instagram influencers — ranked by real influence, not just follower count.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Top 8 Cards ────────────────────────────────────────────────────────────────
top_8 = df.nlargest(8, 'Impact Score')

st.markdown("""
<div style="padding: 2.5rem 5rem 1rem;">
    <div class="section-title">🏆 Top Influencers by Impact Score</div>
    <div class="section-sub">Ranked by Impact Score = Engagement Rate × log₁₀(Followers) — quality over quantity</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="padding: 0 5rem 2.5rem;">', unsafe_allow_html=True)
cols = st.columns(4, gap="large")

for idx, (_, row) in enumerate(top_8.iterrows()):
    col      = cols[idx % 4]
    name     = row['name']
    followers= int(row['Followers'] / 1_000_000)
    eng      = f"{row['Eng Rate']:.1f}%"
    category = str(row['Category']) if pd.notna(row['Category']) else "Creator"
    likes    = int(row['Avg. Likes'])
    impact   = row['Impact Score']
    rank     = int(row['rank'])
    photo    = get_photo_for(name, category, idx)

    with col:
        st.markdown(f"""
        <div class="inf-card">
            <div class="inf-photo-wrap">
                <img class="inf-photo" src="{photo}" alt="{category}">
                <div class="inf-photo-overlay"></div>
                <div class="inf-rank">#{rank}</div>
                <div class="inf-impact-badge">⚡ {impact}</div>
            </div>
            <div class="inf-body">
                <div class="inf-name">{name}</div>
                <div class="inf-category">{category}</div>
                <div class="inf-stats">
                    <div class="inf-stat">
                        <div class="inf-stat-label">Followers</div>
                        <div class="inf-stat-value">{followers}M</div>
                    </div>
                    <div class="inf-stat">
                        <div class="inf-stat-label">Engagement</div>
                        <div class="inf-stat-value">{eng}</div>
                    </div>
                    <div class="inf-stat">
                        <div class="inf-stat-label">Avg Likes</div>
                        <div class="inf-stat-value">{likes:,}</div>
                    </div>
                    <div class="inf-stat">
                        <div class="inf-stat-label">Category</div>
                        <div class="inf-stat-value" style="font-size:0.82rem;">{category[:15]}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Metrics ────────────────────────────────────────────────────────────────────
st.markdown('<div style="padding: 0 5rem 2.5rem;">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(f"""<div class="metric-card">
        <span class="metric-number">{len(df)}</span>
        <span class="metric-text">Influencers Analyzed</span>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <span class="metric-number">{int(df['Followers'].mean()/1_000_000)}M</span>
        <span class="metric-text">Avg Followers</span>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card">
        <span class="metric-number">{df['Eng Rate'].mean():.2f}%</span>
        <span class="metric-text">Avg Engagement Rate</span>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card">
        <span class="metric-number">{df['Impact Score'].max():.1f}</span>
        <span class="metric-text">Highest Impact Score</span>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── CTA ────────────────────────────────────────────────────────────────────────
st.markdown('<div style="padding: 0 5rem 4rem;">', unsafe_allow_html=True)
st.markdown("""
<div class="cta">
    <h2>Ready to Find Your Perfect Influencer?</h2>
    <p>Explore detailed analytics, advanced search filters, and strategic insights powered by Impact Score</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("📊 Go to Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚡ Built with Streamlit &nbsp;|&nbsp; Impact Score = Engagement × log₁₀(Followers) &nbsp;|&nbsp; 200 Top Influencers Analyzed
</div>
""", unsafe_allow_html=True)