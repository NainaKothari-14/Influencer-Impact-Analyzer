import streamlit as st
import pandas as pd

st.set_page_config(page_title="Insights", layout="wide", initial_sidebar_state="collapsed")

# Professional Blue-Cyan CSS Styling
st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #f8f9fa !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        background: #f8f9fa !important;
    }
    
    /* ========== HEADER ========== */
    .header {
        padding: 3.5rem 4rem;
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        color: white;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 188, 212, 0.25);
    }
    
    .header::before {
        content: '';
        position: absolute;
        inset: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(0, 188, 212, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        pointer-events: none;
        animation: floatingLight 15s ease-in-out infinite;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
    }
    
    .header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 0.8rem;
    }
    
    .header p {
        margin: 0;
        font-size: 1.15rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* ========== CONTAINER ========== */
    .container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 4rem;
    }
    
    /* ========== METRIC GRID ========== */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 2rem;
        margin-bottom: 4rem;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 188, 212, 0.2);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-box::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.15) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .metric-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 45px rgba(0, 188, 212, 0.35);
    }
    
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        opacity: 0.95;
        margin-bottom: 0.8rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        position: relative;
        z-index: 1;
    }
    
    /* ========== INSIGHT CARD ========== */
    .insight-card {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 4px 15px rgba(0, 188, 212, 0.08);
        margin-bottom: 2.5rem;
        border: 1px solid rgba(0, 188, 212, 0.1);
        animation: fadeInUp 0.6s ease-out backwards;
    }
    
    .insight-card h3 {
        margin: 0 0 1.5rem 0;
        color: #0d47a1;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* ========== DATA TABLE ========== */
    .data-table {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(0, 188, 212, 0.1);
    }
    
    /* ========== RECOMMENDATION LIST ========== */
    .recommendation-list {
        list-style: none;
        padding: 0;
    }
    
    .recommendation-list li {
        padding: 1.2rem;
        margin-bottom: 1rem;
        background: rgba(0, 188, 212, 0.06);
        border-radius: 8px;
        border-left: 4px solid #00bcd4;
        transition: all 0.3s ease;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #333;
    }
    
    .recommendation-list li:hover {
        background: rgba(0, 188, 212, 0.12);
        transform: translateX(4px);
    }
    
    .recommendation-list strong {
        color: #0d47a1;
        font-weight: 700;
    }
    
    /* ========== RECOMMENDATION CARDS GRID ========== */
    .recommendations-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .recommendation-card {
        background: white;
        border-radius: 14px;
        padding: 2rem;
        border: 1px solid rgba(0, 188, 212, 0.15);
        box-shadow: 0 4px 15px rgba(0, 188, 212, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out backwards;
    }
    
    .recommendation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #00bcd4 0%, #0097a7 100%);
    }
    
    .recommendation-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0, 188, 212, 0.2);
        border-color: rgba(0, 188, 212, 0.3);
    }
    
    .recommendation-card:nth-child(1) { animation-delay: 0.1s; }
    .recommendation-card:nth-child(2) { animation-delay: 0.2s; }
    .recommendation-card:nth-child(3) { animation-delay: 0.3s; }
    .recommendation-card:nth-child(4) { animation-delay: 0.4s; }
    .recommendation-card:nth-child(5) { animation-delay: 0.5s; }
    .recommendation-card:nth-child(6) { animation-delay: 0.6s; }
    
    .rec-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 2px 4px rgba(0, 188, 212, 0.2));
    }
    
    .rec-content h4 {
        margin: 0 0 0.8rem 0;
        color: #0d47a1;
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: -0.3px;
    }
    
    .rec-content p {
        margin: 0;
        color: #555;
        font-size: 0.9rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* ========== STATISTICS ========== */
    .stats-column {
        padding: 1.5rem;
        background: rgba(0, 188, 212, 0.05);
        border-radius: 8px;
        border-left: 3px solid #00bcd4;
    }
    
    .stats-column p {
        margin: 0.8rem 0;
        font-size: 0.95rem;
        color: #333;
        line-height: 1.6;
    }
    
    .stats-column strong {
        color: #0d47a1;
        font-weight: 700;
    }
    
    /* ========== ANIMATIONS ========== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes floatingLight {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(-20px, 20px); }
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 1024px) {
        .header {
            padding: 2.5rem 2rem;
        }
        
        .header h1 {
            font-size: 2.2rem;
        }
        
        .container {
            padding: 0 2rem;
        }
        
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (max-width: 768px) {
        .header {
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        .header h1 {
            font-size: 1.8rem;
        }
        
        .header p {
            font-size: 1rem;
        }
        
        .container {
            padding: 0 1.5rem;
        }
        
        .metrics-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
        
        .insight-card {
            padding: 1.5rem;
        }
    }
    
    /* ========== HIDE STREAMLIT UI ========== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
                }
            });
        }, observerOptions);
        
        document.querySelectorAll('.insight-card').forEach(card => {
            observer.observe(card);
        });
    });
</script>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data_cleaned.csv")

df = load_data()

# Header
st.markdown("""
<div class="header">
    <div class="header-content">
        <h1>Insights & Recommendations</h1>
        <p>Strategic findings and actionable recommendations based on data analysis</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="container">', unsafe_allow_html=True)

# Key Metrics
st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Total Influencers</div>
        <div class="metric-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Avg Engagement</div>
        <div class="metric-value">{df['Eng Rate'].mean():.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Median Followers</div>
        <div class="metric-value">{int(df['Followers'].median()/1_000_000)}M</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    corr = df['Followers'].corr(df['Eng Rate'])
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Correlation</div>
        <div class="metric-value">{corr:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Top Performers
st.markdown('<div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>Top Performers</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    top_eng_idx = df['Eng Rate'].idxmax()
    top_eng = df.loc[top_eng_idx]
    st.markdown(f"""
    **Highest Engagement Rate**
    
    - **Name:** {top_eng['name']}
    - **Rate:** {top_eng['Eng Rate']:.2f}%
    - **Followers:** {int(top_eng['Followers']/1_000_000)}M
    """)

with col2:
    top_followers_idx = df['Followers'].idxmax()
    top_followers = df.loc[top_followers_idx]
    st.markdown(f"""
    **Most Followers**
    
    - **Name:** {top_followers['name']}
    - **Followers:** {int(top_followers['Followers']/1_000_000)}M
    - **Engagement:** {top_followers['Eng Rate']:.2f}%
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Correlation Analysis
st.markdown('<div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>Followers vs Engagement Correlation</h3>', unsafe_allow_html=True)

corr = df['Followers'].corr(df['Eng Rate'])

if corr < 0.3:
    insight_text = f"**WEAK Correlation ({corr:.3f})** - More followers doesn't guarantee higher engagement. Smaller influencers often have better engagement rates."
elif corr < 0.7:
    insight_text = f"**MODERATE Correlation ({corr:.3f})** - There's a reasonable relationship, but many exceptions exist."
else:
    insight_text = f"**STRONG Correlation ({corr:.3f})** - Followers and engagement are closely related."

st.markdown(insight_text)
st.markdown('</div>', unsafe_allow_html=True)

# Category Performance
st.markdown('<div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>Best Performing Categories</h3>', unsafe_allow_html=True)

if df['Category'].notna().sum() > 0:
    category_stats = df[df['Category'].notna()].groupby('Category').agg({
        'Eng Rate': 'mean',
        'name': 'count',
        'Followers': 'mean',
        'Avg. Likes': 'mean'
    }).round(2)
    
    category_stats.columns = ['Avg Engagement %', 'Count', 'Avg Followers', 'Avg Likes']
    category_stats = category_stats.sort_values('Avg Engagement %', ascending=False).head(10)
    
    st.dataframe(category_stats, use_container_width=True)
    
    best_cat = category_stats.index[0]
    best_rate = category_stats['Avg Engagement %'].iloc[0]
    st.markdown(f"**Top Category:** {best_cat} with {best_rate:.2f}% average engagement")

st.markdown('</div>', unsafe_allow_html=True)

# Channel Type Analysis
st.markdown('<div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>Channel Type Breakdown</h3>', unsafe_allow_html=True)

channel_stats = df.groupby('channel_Info').agg({
    'Eng Rate': 'mean',
    'name': 'count',
    'Followers': 'mean'
}).round(2)

channel_stats.columns = ['Avg Engagement %', 'Count', 'Avg Followers']

st.dataframe(channel_stats, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Strategic Recommendations
st.markdown('<div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>Strategic Recommendations</h3>', unsafe_allow_html=True)

recommendations = [
    {
        "title": "Focus on Engagement",
        "description": "High follower counts don't guarantee engagement. Prioritize influencers with strong engagement rates over pure follower count.",
        "icon": "📊"
    },
    {
        "title": "Leverage Category Performance",
        "description": "Different categories show varying engagement rates. Match influencers to categories aligned with your product and brand values.",
        "icon": "🎯"
    },
    {
        "title": "Consider Micro-Influencers",
        "description": "Smaller accounts often have more engaged audiences. Mix mega-influencers (for reach) and micro-influencers (for engagement).",
        "icon": "⭐"
    },
    {
        "title": "Target Demographics",
        "description": "Match influencer audience with your brand's target demographic for better campaign performance and ROI.",
        "icon": "👥"
    },
    {
        "title": "Set Engagement Benchmarks",
        "description": f"Use {df['Eng Rate'].mean():.2f}% as your baseline engagement threshold for partnerships. This ensures quality collaborations.",
        "icon": "✓"
    },
    {
        "title": "Diversify Your Strategy",
        "description": "Don't rely on single influencers. Spread across categories and channel types for maximum reach and impact.",
        "icon": "🔀"
    }
]

st.markdown('<div class="recommendations-grid">', unsafe_allow_html=True)

for rec in recommendations:
    st.markdown(f"""
    <div class="recommendation-card">
        <div class="rec-icon">{rec['icon']}</div>
        <div class="rec-content">
            <h4>{rec['title']}</h4>
            <p>{rec['description']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Dataset Statistics
st.markdown('<div class="insight-card">', unsafe_allow_html=True)
st.markdown('<h3>Dataset Statistics</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="stats-column">
    <p><strong>Followers:</strong><br>
    Min: {int(df['Followers'].min()/1_000_000)}M | Max: {int(df['Followers'].max()/1_000_000)}M | Avg: {int(df['Followers'].mean()/1_000_000)}M</p>
    
    <p><strong>Engagement Rate:</strong><br>
    Min: {df['Eng Rate'].min():.2f}% | Max: {df['Eng Rate'].max():.2f}% | Avg: {df['Eng Rate'].mean():.2f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-column">
    <p><strong>Average Likes:</strong><br>
    Min: {int(df['Avg. Likes'].min()):,} | Max: {int(df['Avg. Likes'].max()):,} | Avg: {int(df['Avg. Likes'].mean()):,}</p>
    
    <p><strong>Posts:</strong><br>
    Min: {int(df['Posts'].min()):,} | Max: {int(df['Posts'].max()):,} | Avg: {int(df['Posts'].mean()):,}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)