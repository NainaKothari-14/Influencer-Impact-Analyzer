import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

st.set_page_config(page_title="Analysis", layout="wide", initial_sidebar_state="collapsed")

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
        box-shadow: 0 10px 40px rgba(0, 188, 212, 0.2);
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

    /* ========== CHART CARD ========== */
    .chart-wrap { padding: 0 5rem; margin-bottom: 2rem; }

    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        box-shadow: 0 4px 15px rgba(0,188,212,0.08);
        border: 1px solid rgba(0,188,212,0.1);
    }

    .chart-container h3 {
        margin: 0 0 0.6rem;
        color: #0d47a1;
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .chart-description {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }

    /* ========== CATEGORY TABLE ========== */
    .category-stats {
        background: white;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-top: 1.5rem;
        border: 1px solid rgba(0,188,212,0.15);
        box-shadow: 0 2px 8px rgba(0,188,212,0.05);
    }

    .category-stats h4 {
        color: #0d47a1;
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }

    .category-stats td { padding: 1rem 1.2rem; border-bottom: 1px solid rgba(0,188,212,0.1); color: #333; font-weight: 500; }
    .category-stats tr:nth-child(even) { background-color: rgba(0,188,212,0.03); }
    .category-stats tr:hover { background-color: rgba(0,188,212,0.08) !important; }
    .category-stats tr:last-child td { border-bottom: none; }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 1024px) {
        .header, .chart-wrap { padding-left: 2.5rem !important; padding-right: 2.5rem !important; }
    }
    @media (max-width: 768px) {
        .header { padding: 2rem 1.5rem !important; }
        .header h1 { font-size: 1.8rem !important; }
        .chart-wrap { padding-left: 1.2rem !important; padding-right: 1.2rem !important; }
        .chart-container { padding: 1.2rem !important; }
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

@st.cache_data
def load_data():
    df = pd.read_csv("data_cleaned.csv")
    df['Impact Score'] = (df['Eng Rate'] * np.log10(df['Followers'])).round(2)
    return df

df = load_data()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <h1>📈 Analysis</h1>
    <p>Visual insights and comprehensive data trends</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 1. TOP 15 BY IMPACT SCORE  ← NEW (replaces nothing, added first)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="chart-wrap"><div class="chart-container">', unsafe_allow_html=True)
st.markdown("""
    <h3>⚡ Top 15 Influencers by Impact Score</h3>
    <p class="chart-description">
        Impact Score = Engagement Rate × log₁₀(Followers) — a creator with high engagement
        but fewer followers can outscore a mega-influencer with low engagement.
    </p>
""", unsafe_allow_html=True)

top15_impact = df.nlargest(15, 'Impact Score')

fig, ax = plt.subplots(figsize=(12, 7))
colors = plt.cm.YlOrRd(np.linspace(0.4, 0.9, len(top15_impact)))
bars = ax.barh(range(len(top15_impact)), top15_impact['Impact Score'].values,
               color=colors, edgecolor='#0d47a1', linewidth=0.8)
ax.set_yticks(range(len(top15_impact)))
ax.set_yticklabels(top15_impact['name'].values, fontsize=10, fontweight='500')
ax.set_xlabel("Impact Score", fontsize=11, fontweight='bold')
ax.set_xlim(0, top15_impact['Impact Score'].max() * 1.18)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

for i, (bar, val) in enumerate(zip(bars, top15_impact['Impact Score'].values)):
    ax.text(val + 0.3, i, f"{val:.1f}", va='center', fontweight='bold', fontsize=9, color='#0d47a1')

plt.tight_layout()
st.pyplot(fig, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2. TOP 15 BY ENGAGEMENT RATE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="chart-wrap"><div class="chart-container">', unsafe_allow_html=True)
st.markdown("""
    <h3>🏆 Top 15 Influencers by Engagement Rate</h3>
    <p class="chart-description">The highest performing creators ranked by engagement percentage — note how these differ from the Impact Score ranking above.</p>
""", unsafe_allow_html=True)

top15_eng = df.nlargest(15, 'Eng Rate')

fig, ax = plt.subplots(figsize=(12, 7))
colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(top15_eng)))
bars = ax.barh(range(len(top15_eng)), top15_eng['Eng Rate'].values,
               color=colors, edgecolor='black', linewidth=0.8)
ax.set_yticks(range(len(top15_eng)))
ax.set_yticklabels(top15_eng['name'].values, fontsize=10, fontweight='500')
ax.set_xlabel("Engagement Rate (%)", fontsize=11, fontweight='bold')
ax.set_xlim(0, top15_eng['Eng Rate'].max() * 1.15)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

for i, (bar, val) in enumerate(zip(bars, top15_eng['Eng Rate'].values)):
    ax.text(val + 0.2, i, f"{val:.2f}%", va='center', fontweight='bold', fontsize=9, color='#0d47a1')

plt.tight_layout()
st.pyplot(fig, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 3. FOLLOWERS VS ENGAGEMENT SCATTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="chart-wrap"><div class="chart-container">', unsafe_allow_html=True)
st.markdown("""
    <h3>🔍 Followers vs Engagement Rate</h3>
    <p class="chart-description">
        The downward trend proves the core insight: <strong>more followers ≠ more influence.</strong>
        Colour intensity shows average likes per post.
    </p>
""", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(12, 7))
scatter = ax.scatter(df['Followers']/1_000_000, df['Eng Rate'],
                     c=df['Avg. Likes']/1_000, cmap='viridis',
                     s=200, alpha=0.65, edgecolors='#0d47a1', linewidth=0.8)
ax.set_xlabel("Followers (Millions)", fontsize=11, fontweight='bold')
ax.set_ylabel("Engagement Rate (%)", fontsize=11, fontweight='bold')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label("Avg Likes (Thousands)", fontweight='bold')
ax.grid(True, alpha=0.3)

# Trend annotation
ax.annotate("As followers ↑, engagement tends to ↓",
            xy=(0.55, 0.88), xycoords='axes fraction',
            fontsize=10, color='#d32f2f', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff3f3', edgecolor='#d32f2f', alpha=0.9))

plt.tight_layout()
st.pyplot(fig, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 4. POSTS vs ENGAGEMENT SCATTER  ← replaces "Most Active by Posts"
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="chart-wrap"><div class="chart-container">', unsafe_allow_html=True)
st.markdown("""
    <h3>📝 Posting Frequency vs Engagement Rate</h3>
    <p class="chart-description">
        Does posting more mean better engagement? Each dot is one influencer.
        Colour shows follower count — reveals whether volume or audience size drives engagement.
    </p>
""", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(12, 7))
scatter2 = ax.scatter(df['Posts'], df['Eng Rate'],
                      c=df['Followers']/1_000_000, cmap='plasma',
                      s=180, alpha=0.6, edgecolors='#0d47a1', linewidth=0.7)
ax.set_xlabel("Number of Posts", fontsize=11, fontweight='bold')
ax.set_ylabel("Engagement Rate (%)", fontsize=11, fontweight='bold')
cbar2 = plt.colorbar(scatter2, ax=ax)
cbar2.set_label("Followers (Millions)", fontweight='bold')
ax.grid(True, alpha=0.3)

ax.annotate("Posting more does NOT guarantee higher engagement",
            xy=(0.3, 0.90), xycoords='axes fraction',
            fontsize=10, color='#d32f2f', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff3f3', edgecolor='#d32f2f', alpha=0.9))

plt.tight_layout()
st.pyplot(fig, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5. CATEGORY DISTRIBUTION — PIE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="chart-wrap"><div class="chart-container">', unsafe_allow_html=True)
st.markdown("""
    <h3>🥧 Influencers by Category</h3>
    <p class="chart-description">Distribution of top creators across different content categories — hover to see details.</p>
""", unsafe_allow_html=True)

category_counts = df[df['Category'].notna()]['Category'].value_counts().head(10)

fig_pie = go.Figure(data=[go.Pie(
    labels=category_counts.index,
    values=category_counts.values,
    hole=0.4,
    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
    textposition='outside',
    textinfo='label+percent',
    textfont=dict(size=12, color='#0d47a1', family='Arial'),
    marker=dict(
        colors=['#1565c0','#1976d2','#1e88e5','#42a5f5','#00bcd4','#00acc1','#0097a7','#00838f','#006064','#004d73'],
        line=dict(color='white', width=2)
    ),
    pull=[0.04 if i == 0 else 0 for i in range(len(category_counts))],
    automargin=True
)])

fig_pie.update_layout(
    height=580,
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=12, color='#0d47a1'),
    margin=dict(l=100, r=100, t=50, b=50)
)

st.plotly_chart(fig_pie, use_container_width=True)

# Category stats table
category_stats_df = pd.DataFrame({
    'Category':   category_counts.index,
    'Count':      category_counts.values,
    'Percentage': (category_counts.values / category_counts.sum() * 100).round(1)
})

st.markdown('<div class="category-stats"><h4>Category Breakdown</h4>', unsafe_allow_html=True)
st.markdown("""
<table style="width:100%; border-collapse:collapse; font-size:0.92rem;">
    <thead>
        <tr style="background: linear-gradient(135deg,#0d47a1 0%,#1976d2 100%); color:white;">
            <th style="padding:1rem 1.2rem; text-align:left; font-weight:700;">Category</th>
            <th style="padding:1rem 1.2rem; text-align:center; font-weight:700;">Count</th>
            <th style="padding:1rem 1.2rem; text-align:center; font-weight:700;">Share</th>
        </tr>
    </thead><tbody>
""", unsafe_allow_html=True)

for i, row in category_stats_df.iterrows():
    bg = 'rgba(0,188,212,0.05)' if i % 2 == 0 else 'white'
    pw = (row['Percentage'] / category_stats_df['Percentage'].max()) * 100
    st.markdown(f"""
        <tr style="background:{bg};">
            <td style="padding:1rem 1.2rem; font-weight:600; color:#0d47a1; border-bottom:1px solid rgba(0,188,212,0.1);">{row['Category']}</td>
            <td style="padding:1rem; text-align:center; font-weight:700; color:#1976d2; border-bottom:1px solid rgba(0,188,212,0.1);">{int(row['Count'])}</td>
            <td style="padding:1rem; text-align:center; border-bottom:1px solid rgba(0,188,212,0.1);">
                <div style="display:flex; align-items:center; justify-content:center; gap:8px;">
                    <div style="width:60px; height:6px; background:#e0e0e0; border-radius:3px; overflow:hidden;">
                        <div style="width:{pw}%; height:100%; background:linear-gradient(90deg,#00bcd4,#0097a7); border-radius:3px;"></div>
                    </div>
                    <span style="font-weight:700; color:#0d47a1;">{row['Percentage']:.1f}%</span>
                </div>
            </td>
        </tr>
    """, unsafe_allow_html=True)

st.markdown('</tbody></table></div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 6. AVG ENGAGEMENT BY CATEGORY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="chart-wrap"><div class="chart-container">', unsafe_allow_html=True)
st.markdown("""
    <h3>📊 Average Engagement Rate by Category</h3>
    <p class="chart-description">Which content categories drive the most engaged audiences? This directly answers <em>who influences more effectively</em>.</p>
""", unsafe_allow_html=True)

category_eng = df[df['Category'].notna()].groupby('Category')['Eng Rate'].mean().sort_values(ascending=False).head(12)
best_cat  = category_eng.index[0]
worst_cat = category_eng.index[-1]
ratio     = category_eng.iloc[0] / category_eng.iloc[-1]

fig_bar = go.Figure(data=[go.Bar(
    x=category_eng.index,
    y=category_eng.values,
    marker=dict(color=category_eng.values, colorscale='Viridis', showscale=True,
                colorbar=dict(title="Eng %", thickness=16, len=0.6),
                line=dict(color='#0d47a1', width=1.5)),
    hovertemplate='<b>%{x}</b><br>Avg Engagement: %{y:.2f}%<extra></extra>',
    text=[f'{v:.2f}%' for v in category_eng.values],
    textposition='outside',
    textfont=dict(size=10, color='#0d47a1', family='Arial')
)])

fig_bar.update_layout(
    xaxis_title="Category", yaxis_title="Avg Engagement Rate (%)",
    height=480, hovermode='x unified',
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=11, color='#0d47a1'),
    xaxis=dict(tickangle=-40, tickfont=dict(size=10)),
    margin=dict(b=110, t=50, l=60, r=80),
    annotations=[dict(
        text=f"📌 {best_cat} gets {ratio:.1f}x more engagement than {worst_cat}",
        xref="paper", yref="paper", x=0.5, y=1.06,
        showarrow=False, font=dict(size=11, color='#d32f2f'), bgcolor='#fff3f3',
        bordercolor='#d32f2f', borderwidth=1, borderpad=6
    )]
)

st.plotly_chart(fig_bar, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 7. CHANNEL TYPE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="chart-wrap"><div class="chart-container">', unsafe_allow_html=True)
st.markdown("""
    <h3>📡 Influencers by Channel Type</h3>
    <p class="chart-description">Breakdown of creators: Brands vs Individual influencers — does account type affect influence?</p>
""", unsafe_allow_html=True)

channel_counts = df['channel_Info'].value_counts()

fig_ch = go.Figure(data=[go.Bar(
    x=channel_counts.index,
    y=channel_counts.values,
    marker=dict(color=['#0d47a1','#1976d2','#00bcd4'], line=dict(color='white', width=3)),
    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
    text=channel_counts.values,
    textposition='outside',
    textfont=dict(size=12, color='#0d47a1', family='Arial')
)])

fig_ch.update_layout(
    xaxis_title="Channel Type", yaxis_title="Number of Influencers",
    height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=11, color='#0d47a1'),
    margin=dict(t=50, b=60, l=60, r=40)
)

st.plotly_chart(fig_ch, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div style="margin-top:3rem;"></div>', unsafe_allow_html=True)