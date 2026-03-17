import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="collapsed")

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
        padding: 3rem 4rem;
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        color: white;
        border-radius: 0;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 188, 212, 0.2);
    }
    
    .header::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(0, 188, 212, 0.2) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .header p {
        margin: 0.8rem 0 0 0;
        opacity: 0.95;
        font-size: 1.1rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* ========== CONTAINER ========== */
    .container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 4rem;
    }
    
    /* ========== FILTER SECTION ========== */
    .filter-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 188, 212, 0.08);
        margin-bottom: 3rem;
        border: 1px solid rgba(0, 188, 212, 0.1);
    }
    
    .filter-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0d47a1;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* ========== TOP PERFORMER ========== */
    .top-performer {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        padding: 3rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 10px 40px rgba(0, 188, 212, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .top-performer::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(0, 188, 212, 0.2) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .top-performer h2 {
        margin: 0 0 2rem 0;
        font-size: 1.8rem;
        font-weight: 800;
        position: relative;
        z-index: 1;
    }
    
    .top-performer-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 2rem;
    }
    
    .perf-metric {
        background: rgba(255, 255, 255, 0.12);
        padding: 1.5rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        z-index: 1;
    }
    
    .perf-metric-label {
        font-size: 0.85rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .perf-metric-value {
        font-size: 1.8rem;
        font-weight: 900;
    }
    
    /* ========== DATA SECTION ========== */
    .data-section {
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 188, 212, 0.08);
        margin-bottom: 3rem;
        border: 1px solid rgba(0, 188, 212, 0.1);
    }
    
    .data-section h2 {
        margin: 0 0 2rem 0;
        color: #0d47a1;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* ========== STYE STREAMLIT ELEMENTS ========== */
    .stTextInput > div > div > input {
        border: 1.5px solid rgba(0, 188, 212, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00bcd4 !important;
        box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.1) !important;
    }
    
    .stSelectbox > div > div > select {
        border: 1.5px solid rgba(0, 188, 212, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-size: 0.95rem !important;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #00bcd4 !important;
    }
    
    /* ========== METRICS ROW ========== */
    .stMetric {
        background: linear-gradient(135deg, rgba(0, 188, 212, 0.08) 0%, rgba(0, 188, 212, 0.04) 100%);
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border-left: 4px solid #00bcd4 !important;
    }
    
    .stMetric [data-testid="metricDelta"] {
        color: #00bcd4 !important;
    }
    
    /* ========== DATA TABLE ========== */
    [data-testid="stDataFrame"] {
        font-size: 0.95rem !important;
    }
    
    [data-testid="stDataFrame"] th {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stDataFrame"] td {
        padding: 1rem !important;
        border-bottom: 1px solid rgba(0, 188, 212, 0.1) !important;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background: rgba(0, 188, 212, 0.05) !important;
    }
    
    /* ========== NO RESULTS ========== */
    .no-results {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.08) 0%, rgba(244, 67, 54, 0.04) 100%);
        padding: 3rem;
        border-radius: 16px;
        text-align: center;
        color: #d32f2f;
        border: 1px solid rgba(244, 67, 54, 0.2);
        margin-bottom: 2rem;
    }
    
    .no-results h3 {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .header {
            padding: 2rem;
        }
        
        .header h1 {
            font-size: 2rem;
        }
        
        .header p {
            font-size: 0.95rem;
        }
        
        .filter-section {
            padding: 1.5rem;
        }
        
        .top-performer {
            padding: 2rem;
        }
        
        .top-performer h2 {
            font-size: 1.4rem;
        }
        
        .top-performer-metrics {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    
    /* ========== HIDE STREAMLIT UI ========== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data_cleaned.csv")

df = load_data()

# Header
st.markdown("""
<div class="header">
    <h1> Dashboard</h1>
    <p>Search, filter, and analyze influencers in real-time</p>
</div>
""", unsafe_allow_html=True)

# Container
st.markdown('<div class="container">', unsafe_allow_html=True)

# Search & Filter Section
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('<div class="filter-title">🔍 Search & Filter</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    search_name = st.text_input("Search by name", placeholder="e.g., instagram, cristiano...", label_visibility="collapsed")

with col2:
    category_filter = st.selectbox("Filter by category", ["All"] + sorted(df['Category'].dropna().unique().tolist()), label_visibility="collapsed")

with col3:
    sort_by = st.selectbox("Sort by", ["Engagement Rate", "Followers", "Posts", "Avg Likes"], label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# Filter data
filtered_df = df.copy()

if search_name:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df['Category'] == category_filter]

# Sort
sort_columns = {
    "Engagement Rate": "Eng Rate",
    "Followers": "Followers",
    "Posts": "Posts",
    "Avg Likes": "Avg. Likes"
}
filtered_df = filtered_df.sort_values(sort_columns[sort_by], ascending=False)

# Top Influencer
if len(filtered_df) > 0:
    st.markdown('<div class="top-performer">', unsafe_allow_html=True)
    st.markdown('<h2> Top Performer</h2>', unsafe_allow_html=True)
    
    top = filtered_df.iloc[0]
    
    st.markdown('<div class="top-performer-metrics">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-label">Name</div>
            <div class="perf-metric-value">{top['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-label">Followers</div>
            <div class="perf-metric-value">{int(top['Followers']/1_000_000)}M</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-label">Avg Likes</div>
            <div class="perf-metric-value">{int(top['Avg. Likes']):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-label">Engagement</div>
            <div class="perf-metric-value">{top['Eng Rate']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# Data Table Section
st.markdown('<div class="data-section">', unsafe_allow_html=True)

if len(filtered_df) > 0:
    st.markdown(f'<h2> Results ({len(filtered_df)} found)</h2>', unsafe_allow_html=True)
    
    display_cols = ['rank', 'name', 'Category', 'Followers', 'Avg. Likes', 'Eng Rate']
    
    # Prepare data for display
    display_df = filtered_df[display_cols].copy()
    display_df['Followers'] = (display_df['Followers']/1_000_000).round(1).astype(str) + 'M'
    display_df = display_df.rename(columns={
        'rank': 'Rank',
        'name': 'Name',
        'Category': 'Category',
        'Followers': 'Followers',
        'Avg. Likes': 'Avg Likes',
        'Eng Rate': 'Engagement %'
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.markdown("""
    <div class="no-results">
        <h3>😕 No Results Found</h3>
        <p>Try adjusting your search filters or category selection</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer spacing
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)