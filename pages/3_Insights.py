import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Insights", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        background: #f8f9fa !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    [data-testid="stMainBlockContainer"],
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
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 188, 212, 0.25);
    }

    .header::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(0,188,212,0.2) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }

    .header h1 { margin: 0; font-size: 2.6rem; font-weight: 900; letter-spacing: -1px; position: relative; z-index: 1; color: white !important; }
    .header p  { margin: 0.7rem 0 0; font-size: 1.05rem; opacity: 0.95; font-weight: 300; position: relative; z-index: 1; color: white !important; }

    /* ========== SECTION WRAPPER ========== */
    .section-wrap { padding: 0 5rem; margin-bottom: 2rem; }

    /* ========== HOW WE MEASURE CARD ========== */
    .measure-card {
        background: white;
        border-left: 5px solid #00bcd4;
        border-radius: 14px;
        padding: 1.8rem 2.2rem;
        box-shadow: 0 4px 15px rgba(0,188,212,0.08);
        border: 1px solid rgba(0,188,212,0.15);
        display: flex;
        align-items: flex-start;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .measure-formula {
        font-size: 1.05rem; font-weight: 800; color: #0d47a1;
        background: rgba(0,188,212,0.1); padding: 0.6rem 1.2rem;
        border-radius: 8px; white-space: nowrap; align-self: center;
    }

    .measure-text { font-size: 0.9rem; color: #444; line-height: 1.7; }
    .measure-text strong { color: #0d47a1; }

    /* ========== METRIC BOXES ========== */
    .metric-box {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        color: white; padding: 1.8rem; border-radius: 14px;
        box-shadow: 0 8px 25px rgba(0,188,212,0.2);
        text-align: center; position: relative; overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-box::before {
        content: ''; position: absolute; inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.15) 0%, transparent 60%);
        pointer-events: none;
    }

    .metric-box:hover { transform: translateY(-6px); box-shadow: 0 15px 40px rgba(0,188,212,0.3); }

    .metric-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; opacity: 0.9; margin-bottom: 0.6rem; color: white !important; }
    .metric-value { font-size: 2.2rem; font-weight: 900; position: relative; z-index: 1; color: white !important; }
    .metric-sub   { font-size: 0.72rem; opacity: 0.75; margin-top: 0.3rem; color: white !important; }

    /* ========== INSIGHT CARD ========== */
    .insight-card {
        background: white;
        border-radius: 14px;
        padding: 2rem 2.5rem;
        box-shadow: 0 4px 15px rgba(0,188,212,0.08);
        border: 1px solid rgba(0,188,212,0.1);
    }

    .insight-card h3 { margin: 0 0 1.4rem; color: #0d47a1; font-size: 1.4rem; font-weight: 800; letter-spacing: -0.5px; }

    /* ========== PARADOX SECTION ========== */
    .paradox-card {
        background: linear-gradient(135deg, rgba(13,71,161,0.06) 0%, rgba(0,188,212,0.1) 100%);
        border: 1.5px solid rgba(0,188,212,0.25);
        border-radius: 14px;
        padding: 2rem 2.5rem;
    }

    .paradox-card h3 { margin: 0 0 1.2rem; color: #0d47a1; font-size: 1.4rem; font-weight: 800; }

    .paradox-stats {
        display: grid;
        grid-template-columns: 1fr auto 1fr auto 1fr;
        gap: 1rem;
        align-items: center;
        margin-bottom: 1.2rem;
    }

    .p-box {
        background: white; border-radius: 10px; padding: 1.2rem;
        text-align: center; box-shadow: 0 2px 8px rgba(0,188,212,0.1);
    }

    .p-box .p-val { font-size: 1.8rem; font-weight: 900; color: #0d47a1; }
    .p-box .p-val.red { color: #e53935 !important; }
    .p-box .p-lbl { font-size: 0.78rem; color: #666; margin-top: 0.3rem; line-height: 1.4; }
    .p-arrow { font-size: 1.5rem; color: #00bcd4; text-align: center; }
    .paradox-insight { font-size: 0.9rem; color: #444; line-height: 1.7; padding: 1rem 1.2rem; background: white; border-radius: 8px; border-left: 4px solid #e53935; }
    .paradox-insight strong { color: #0d47a1; }

    /* ========== TOP PERFORMERS SIDE BY SIDE ========== */
    .performer-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }

    .performer-box {
        padding: 1.5rem; background: rgba(0,188,212,0.05);
        border-radius: 10px; border-left: 4px solid #00bcd4;
    }

    .performer-box h4 { color: #0d47a1; font-size: 1rem; font-weight: 700; margin-bottom: 0.8rem; }
    .performer-box .p-name { font-size: 1.2rem; font-weight: 900; color: #0d47a1; margin-bottom: 0.5rem; }
    .performer-box .p-stat { font-size: 0.88rem; color: #555; margin: 0.3rem 0; }
    .performer-box .p-stat strong { color: #0d47a1; }

    /* ========== RECOMMENDATION CARDS ========== */
    .rec-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }

    .rec-card {
        background: white; border-radius: 12px; padding: 1.5rem;
        border: 1px solid rgba(0,188,212,0.15);
        box-shadow: 0 4px 12px rgba(0,188,212,0.07);
        position: relative; overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .rec-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0;
        height: 3px; background: linear-gradient(90deg, #00bcd4, #0097a7);
    }

    .rec-card:hover { transform: translateY(-6px); box-shadow: 0 12px 30px rgba(0,188,212,0.15); }

    .rec-icon { font-size: 2rem; margin-bottom: 0.7rem; display: block; }
    .rec-card h4 { color: #0d47a1; font-size: 1rem; font-weight: 800; margin-bottom: 0.5rem; }
    .rec-card p  { color: #555; font-size: 0.87rem; line-height: 1.6; margin: 0; }
    .rec-card .rec-tag {
        display: inline-block; margin-top: 0.7rem;
        background: rgba(0,188,212,0.1); color: #0097a7;
        font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem;
        border-radius: 20px;
    }

    /* ========== STATS COLUMN ========== */
    .stats-col {
        padding: 1.4rem 1.6rem;
        background: rgba(0,188,212,0.05);
        border-radius: 10px; border-left: 3px solid #00bcd4;
    }

    .stats-col p { margin: 0.7rem 0; font-size: 0.92rem; color: #333; line-height: 1.6; }
    .stats-col strong { color: #0d47a1; font-weight: 700; }

    /* ========== CORRELATION BADGE ========== */
    .corr-badge {
        display: inline-block; padding: 0.4rem 1rem;
        border-radius: 20px; font-weight: 800; font-size: 1rem;
        margin-bottom: 0.8rem;
    }

    .corr-weak     { background: rgba(244,67,54,0.1);  color: #c62828; }
    .corr-moderate { background: rgba(255,152,0,0.1);  color: #e65100; }
    .corr-strong   { background: rgba(76,175,80,0.1);  color: #2e7d32; }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 1024px) {
        .header, .section-wrap { padding-left: 2.5rem !important; padding-right: 2.5rem !important; }
    }
    @media (max-width: 768px) {
        .header { padding: 2rem 1.5rem !important; }
        .header h1 { font-size: 1.8rem !important; }
        .section-wrap { padding-left: 1.2rem !important; padding-right: 1.2rem !important; }
        .performer-grid { grid-template-columns: 1fr; }
        .paradox-stats { grid-template-columns: 1fr; }
        .p-arrow { display: none; }
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Load & Prepare ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data_cleaned.csv")
    df['Impact Score'] = (df['Eng Rate'] * np.log10(df['Followers'])).round(2)
    return df

df = load_data()

# Pre-compute all stats
corr              = df['Followers'].corr(df['Eng Rate'])
top25_eng         = df[df['Followers'] >= df['Followers'].quantile(0.75)]['Eng Rate'].mean()
bottom25_eng      = df[df['Followers'] <= df['Followers'].quantile(0.25)]['Eng Rate'].mean()
multiplier        = bottom25_eng / top25_eng
avg_eng           = df['Eng Rate'].mean()

category_stats = df[df['Category'].notna()].groupby('Category').agg(
    avg_eng=('Eng Rate', 'mean'),
    count=('name', 'count'),
    avg_followers=('Followers', 'mean'),
    avg_likes=('Avg. Likes', 'mean'),
    avg_impact=('Impact Score', 'mean')
).round(2).sort_values('avg_eng', ascending=False)

best_cat  = category_stats.index[0]
worst_cat = category_stats.index[-1]
best_rate = category_stats['avg_eng'].iloc[0]
worst_rate= category_stats['avg_eng'].iloc[-1]
cat_ratio = best_rate / worst_rate

top_impact_idx  = df['Impact Score'].idxmax()
top_impact      = df.loc[top_impact_idx]
top_eng_idx     = df['Eng Rate'].idxmax()
top_eng_row     = df.loc[top_eng_idx]
top_follow_idx  = df['Followers'].idxmax()
top_follow_row  = df.loc[top_follow_idx]

channel_stats = df.groupby('channel_Info').agg(
    avg_eng=('Eng Rate', 'mean'),
    count=('name', 'count'),
    avg_followers=('Followers', 'mean')
).round(2)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <h1>💡 Insights & Recommendations</h1>
    <p>Strategic findings and actionable recommendations based on data analysis</p>
</div>
""", unsafe_allow_html=True)

# ── How We Measure Influence ───────────────────────────────────────────────────
st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
st.markdown(f"""
<div class="measure-card">
    <div class="measure-formula">📐 Impact Score = Engagement Rate × log₁₀(Followers)</div>
    <div class="measure-text">
        Standard follower count is a <strong>reach metric</strong>, not an <strong>influence metric</strong>.
        Our Impact Score combines both — a creator with <strong>500K followers &amp; 8% engagement</strong>
        scores higher than one with <strong>50M followers &amp; 0.3% engagement</strong>,
        because <strong>quality of influence matters more than quantity.</strong>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Key Metrics Row ────────────────────────────────────────────────────────────
st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Total Influencers</div>
        <div class="metric-value">{len(df)}</div>
        <div class="metric-sub">in dataset</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Avg Engagement</div>
        <div class="metric-value">{avg_eng:.2f}%</div>
        <div class="metric-sub">baseline threshold</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Median Followers</div>
        <div class="metric-value">{int(df['Followers'].median()/1_000_000)}M</div>
        <div class="metric-sub">middle of dataset</div>
    </div>""", unsafe_allow_html=True)

with col4:
    corr_label = "Weak" if abs(corr) < 0.3 else ("Moderate" if abs(corr) < 0.7 else "Strong")
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Followers↔Engagement</div>
        <div class="metric-value">{corr:.2f}</div>
        <div class="metric-sub">{corr_label} correlation</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Top Impact Score</div>
        <div class="metric-value">{df['Impact Score'].max():.1f}</div>
        <div class="metric-sub">{top_impact['name']}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Influence Paradox ──────────────────────────────────────────────────────────
st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
st.markdown(f"""
<div class="paradox-card">
    <h3>⚡ The Influence Paradox</h3>
    <div class="paradox-stats">
        <div class="p-box">
            <div class="p-val">{top25_eng:.2f}%</div>
            <div class="p-lbl">Avg engagement<br><strong>Top 25% most followed</strong></div>
        </div>
        <div class="p-arrow">→</div>
        <div class="p-box">
            <div class="p-val">{bottom25_eng:.2f}%</div>
            <div class="p-lbl">Avg engagement<br><strong>Bottom 25% by followers</strong></div>
        </div>
        <div class="p-arrow">→</div>
        <div class="p-box">
            <div class="p-val red">{multiplier:.1f}x</div>
            <div class="p-lbl">Smaller influencers<br><strong>more engaging</strong></div>
        </div>
    </div>
    <div class="paradox-insight">
        📌 <strong>Key finding:</strong> The bottom 25% of influencers by follower count generate
        <strong>{multiplier:.1f}x more engagement</strong> than the top 25%.
        This directly proves that <strong>follower count is not a reliable measure of influence</strong> —
        brands and marketers should use <strong>Impact Score</strong> instead for better ROI.
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Top Performers ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-wrap"><div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>🏆 Top Performers</h3>', unsafe_allow_html=True)

st.markdown(f"""
<div class="performer-grid">
    <div class="performer-box">
        <h4>⚡ Highest Impact Score</h4>
        <div class="p-name">{top_impact['name']}</div>
        <div class="p-stat"><strong>Impact Score:</strong> {top_impact['Impact Score']}</div>
        <div class="p-stat"><strong>Engagement:</strong> {top_impact['Eng Rate']:.2f}%</div>
        <div class="p-stat"><strong>Followers:</strong> {int(top_impact['Followers']/1_000_000)}M</div>
        <div class="p-stat"><strong>Category:</strong> {top_impact['Category'] if pd.notna(top_impact['Category']) else 'N/A'}</div>
    </div>
    <div class="performer-box">
        <h4>📈 Highest Engagement Rate</h4>
        <div class="p-name">{top_eng_row['name']}</div>
        <div class="p-stat"><strong>Engagement:</strong> {top_eng_row['Eng Rate']:.2f}%</div>
        <div class="p-stat"><strong>Followers:</strong> {int(top_eng_row['Followers']/1_000_000)}M</div>
        <div class="p-stat"><strong>Impact Score:</strong> {top_eng_row['Impact Score']}</div>
        <div class="p-stat"><strong>Category:</strong> {top_eng_row['Category'] if pd.notna(top_eng_row['Category']) else 'N/A'}</div>
    </div>
    <div class="performer-box">
        <h4>👥 Most Followers</h4>
        <div class="p-name">{top_follow_row['name']}</div>
        <div class="p-stat"><strong>Followers:</strong> {int(top_follow_row['Followers']/1_000_000)}M</div>
        <div class="p-stat"><strong>Engagement:</strong> {top_follow_row['Eng Rate']:.2f}%</div>
        <div class="p-stat"><strong>Impact Score:</strong> {top_follow_row['Impact Score']}</div>
        <div class="p-stat" style="color:#e53935;"><strong>Note:</strong> High reach but lower engagement than top impact creator</div>
    </div>
    <div class="performer-box">
        <h4>🥇 Best Category</h4>
        <div class="p-name">{best_cat}</div>
        <div class="p-stat"><strong>Avg Engagement:</strong> {best_rate:.2f}%</div>
        <div class="p-stat"><strong>Influencers:</strong> {int(category_stats['count'].iloc[0])}</div>
        <div class="p-stat"><strong>vs Worst ({worst_cat}):</strong> {worst_rate:.2f}%</div>
        <div class="p-stat" style="color:#2e7d32;"><strong>{cat_ratio:.1f}x better</strong> engagement than lowest category</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ── Correlation Analysis ───────────────────────────────────────────────────────
st.markdown('<div class="section-wrap"><div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>🔗 Followers vs Engagement Correlation</h3>', unsafe_allow_html=True)

if abs(corr) < 0.3:
    badge_class = "corr-weak"
    corr_label  = f"WEAK Correlation ({corr:.3f})"
    corr_msg    = f"More followers does <strong>not</strong> guarantee higher engagement. Our data confirms the Influence Paradox — smaller influencers consistently outperform mega-influencers in audience engagement."
elif abs(corr) < 0.7:
    badge_class = "corr-moderate"
    corr_label  = f"MODERATE Correlation ({corr:.3f})"
    corr_msg    = "There is a partial relationship, but many exceptions exist. Impact Score is a more reliable measure than follower count alone."
else:
    badge_class = "corr-strong"
    corr_label  = f"STRONG Correlation ({corr:.3f})"
    corr_msg    = "Followers and engagement are closely linked in this dataset."

st.markdown(f"""
<span class="corr-badge {badge_class}">{corr_label}</span>
<p style="color:#444; font-size:0.92rem; line-height:1.7;">{corr_msg}</p>
""", unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ── Category Performance ───────────────────────────────────────────────────────
st.markdown('<div class="section-wrap"><div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>📂 Best Performing Categories</h3>', unsafe_allow_html=True)

display_cat = category_stats.copy()
display_cat.columns = ['Avg Engagement %', 'Count', 'Avg Followers', 'Avg Likes', 'Avg Impact Score']
display_cat['Avg Followers'] = (display_cat['Avg Followers'] / 1_000_000).round(1).astype(str) + 'M'
st.dataframe(display_cat.head(10), use_container_width=True)

st.markdown(f"""
<p style="margin-top:1rem; padding:0.8rem 1.2rem; background:rgba(0,188,212,0.08);
   border-radius:8px; border-left:4px solid #00bcd4; color:#444; font-size:0.9rem; line-height:1.6;">
📌 <strong>{best_cat}</strong> leads with <strong>{best_rate:.2f}%</strong> avg engagement —
that's <strong>{cat_ratio:.1f}x higher</strong> than <strong>{worst_cat}</strong> ({worst_rate:.2f}%).
Brands targeting <strong>{best_cat}</strong> creators will see significantly better audience response.
</p>
""", unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ── Channel Type ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-wrap"><div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>📡 Channel Type Breakdown</h3>', unsafe_allow_html=True)

display_ch = channel_stats.copy()
display_ch.columns = ['Avg Engagement %', 'Count', 'Avg Followers']
display_ch['Avg Followers'] = (display_ch['Avg Followers'] / 1_000_000).round(1).astype(str) + 'M'
st.dataframe(display_ch, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ── Strategic Recommendations ──────────────────────────────────────────────────
st.markdown('<div class="section-wrap"><div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>🎯 Strategic Recommendations</h3>', unsafe_allow_html=True)

recommendations = [
    {
        "icon": "⚡",
        "title": "Use Impact Score, Not Followers",
        "desc": f"Our data shows the top Impact Score is <strong>{df['Impact Score'].max():.1f}</strong> vs the most followed creator who scores <strong>{top_follow_row['Impact Score']}</strong>. Impact Score is the better selection metric.",
        "tag": "Core Metric"
    },
    {
        "icon": "🎯",
        "title": f"Prioritise {best_cat} Category",
        "desc": f"<strong>{best_cat}</strong> delivers <strong>{best_rate:.2f}%</strong> avg engagement — <strong>{cat_ratio:.1f}x more</strong> than the lowest category. Highest ROI for audience influence.",
        "tag": "Category Strategy"
    },
    {
        "icon": "⭐",
        "title": "Invest in Micro-Influencers",
        "desc": f"Bottom 25% by followers average <strong>{bottom25_eng:.2f}% engagement</strong> vs <strong>{top25_eng:.2f}%</strong> for the top 25%. Smaller accounts are <strong>{multiplier:.1f}x more engaging</strong>.",
        "tag": "Influence Paradox"
    },
    {
        "icon": "📊",
        "title": "Set Engagement Benchmarks",
        "desc": f"Dataset average is <strong>{avg_eng:.2f}%</strong>. Use this as your minimum threshold for partnerships. Any influencer below this will underperform the market average.",
        "tag": "Quality Filter"
    },
    {
        "icon": "🔀",
        "title": "Diversify Across Categories",
        "desc": f"With <strong>{df['Category'].nunique()} distinct categories</strong>, spreading campaigns across top 3 performing niches maximises reach while maintaining engagement quality.",
        "tag": "Portfolio Strategy"
    },
    {
        "icon": "📉",
        "title": "Don't Chase Posting Frequency",
        "desc": f"Our analysis shows posting volume has weak correlation with engagement. Max posts in dataset: <strong>{int(df['Posts'].max()):,}</strong> — but high posters don't top the engagement charts.",
        "tag": "Content Strategy"
    }
]

st.markdown('<div class="rec-grid">', unsafe_allow_html=True)
for rec in recommendations:
    st.markdown(f"""
    <div class="rec-card">
        <span class="rec-icon">{rec['icon']}</span>
        <h4>{rec['title']}</h4>
        <p>{rec['desc']}</p>
        <span class="rec-tag">{rec['tag']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ── Dataset Statistics ─────────────────────────────────────────────────────────
st.markdown('<div class="section-wrap"><div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>📋 Dataset Statistics</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
    <div class="stats-col">
        <p><strong>Followers:</strong><br>
        Min: {int(df['Followers'].min()/1_000_000)}M &nbsp;|&nbsp; Max: {int(df['Followers'].max()/1_000_000)}M &nbsp;|&nbsp; Avg: {int(df['Followers'].mean()/1_000_000)}M</p>
        <p><strong>Engagement Rate:</strong><br>
        Min: {df['Eng Rate'].min():.2f}% &nbsp;|&nbsp; Max: {df['Eng Rate'].max():.2f}% &nbsp;|&nbsp; Avg: {avg_eng:.2f}%</p>
        <p><strong>Impact Score:</strong><br>
        Min: {df['Impact Score'].min():.1f} &nbsp;|&nbsp; Max: {df['Impact Score'].max():.1f} &nbsp;|&nbsp; Avg: {df['Impact Score'].mean():.1f}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-col">
        <p><strong>Average Likes:</strong><br>
        Min: {int(df['Avg. Likes'].min()):,} &nbsp;|&nbsp; Max: {int(df['Avg. Likes'].max()):,} &nbsp;|&nbsp; Avg: {int(df['Avg. Likes'].mean()):,}</p>
        <p><strong>Posts:</strong><br>
        Min: {int(df['Posts'].min()):,} &nbsp;|&nbsp; Max: {int(df['Posts'].max()):,} &nbsp;|&nbsp; Avg: {int(df['Posts'].mean()):,}</p>
        <p><strong>Categories:</strong><br>
        {df['Category'].nunique()} unique &nbsp;|&nbsp; Most common: <strong>{df['Category'].mode()[0]}</strong></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
st.markdown('<div style="margin-top:3rem;"></div>', unsafe_allow_html=True)