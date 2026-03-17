import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Analysis", layout="wide", initial_sidebar_state="collapsed")

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
    
    /* ========== CHART CONTAINER ========== */
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 4px 15px rgba(0, 188, 212, 0.08);
        margin-bottom: 3rem;
        border: 1px solid rgba(0, 188, 212, 0.1);
    }
    
    .chart-container h3 {
        margin: 0 0 2rem 0;
        color: #0d47a1;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .chart-description {
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* ========== CATEGORY TABLE ========== */
    .category-stats {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid rgba(0, 188, 212, 0.2);
        box-shadow: 0 2px 8px rgba(0, 188, 212, 0.05);
    }
    
    .category-stats h4 {
        color: #0d47a1;
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    .category-stats table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .category-stats th {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%);
        color: white;
        padding: 1.2rem;
        text-align: left;
        font-weight: 800;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .category-stats th:nth-child(2),
    .category-stats th:nth-child(3) {
        text-align: center;
    }
    
    .category-stats td {
        padding: 1.2rem;
        border-bottom: 1px solid rgba(0, 188, 212, 0.1);
        color: #333;
        font-weight: 500;
    }
    
    .category-stats tr:nth-child(even) {
        background-color: rgba(0, 188, 212, 0.03);
    }
    
    .category-stats tr:hover {
        background-color: rgba(0, 188, 212, 0.08) !important;
        transition: all 0.3s ease;
    }
    
    .category-stats tr:last-child td {
        border-bottom: none;
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
        
        .container {
            padding: 0 1.5rem;
        }
        
        .chart-container {
            padding: 1.5rem;
        }
    }
    
    /* ========== HIDE STREAMLIT UI ========== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# Set style for matplotlib with better colors
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data_cleaned.csv")

df = load_data()

# Header
st.markdown("""
<div class="header">
    <h1> Analysis</h1>
    <p>Visual insights and comprehensive data trends</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="container">', unsafe_allow_html=True)

# 1. Top 15 by Engagement Rate
st.markdown("""
<div class="chart-container">
    <h3> Top 15 Influencers by Engagement Rate</h3>
    <p class="chart-description">The highest performing creators ranked by engagement percentage</p>
""", unsafe_allow_html=True)

top15 = df.nlargest(15, 'Eng Rate')

fig, ax = plt.subplots(figsize=(12, 7))
colors = plt.cm.viridis(range(len(top15)))
bars = ax.barh(range(len(top15)), top15['Eng Rate'].values, color=colors, edgecolor='black', linewidth=1)
ax.set_yticks(range(len(top15)))
ax.set_yticklabels(top15['name'].values, fontsize=10, fontweight='500')
ax.set_xlabel("Engagement Rate (%)", fontsize=11, fontweight='bold')
ax.set_xlim(0, top15['Eng Rate'].max() * 1.15)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, top15['Eng Rate'].values)):
    ax.text(val + 0.2, i, f"{val:.2f}%", va='center', fontweight='bold', fontsize=9, color='#0d47a1')

plt.tight_layout()
st.pyplot(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 2. Followers vs Engagement Scatter
st.markdown("""
<div class="chart-container">
    <h3> Followers vs Engagement Rate</h3>
    <p class="chart-description">Understanding the relationship between follower count and audience engagement</p>
""", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(12, 7))
scatter = ax.scatter(df['Followers']/1_000_000, df['Eng Rate'], 
                     c=df['Avg. Likes']/1_000, cmap='viridis', s=200, alpha=0.65, 
                     edgecolors='#0d47a1', linewidth=0.8)
ax.set_xlabel("Followers (Millions)", fontsize=11, fontweight='bold')
ax.set_ylabel("Engagement Rate (%)", fontsize=11, fontweight='bold')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label("Avg Likes (Thousands)", fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 3. Category Distribution - INTERACTIVE PIE CHART
st.markdown("""
<div class="chart-container">
    <h3> Influencers by Category</h3>
    <p class="chart-description">Distribution of top creators across different content categories - Hover to see details!</p>
""", unsafe_allow_html=True)

category_counts = df[df['Category'].notna()]['Category'].value_counts().head(10)

# Create interactive pie chart using plotly
fig = go.Figure(data=[go.Pie(
    labels=category_counts.index,
    values=category_counts.values,
    hole=0.35,  # Donut chart for better readability
    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
    textposition='auto',
    textinfo='label+percent',
    textfont=dict(
        size=13,
        color='#fff',
        family='Arial Black'
    ),
    marker=dict(
        colors=['#0d47a1', '#1976d2', '#00bcd4', '#00acc1', '#0097a7', '#00838f', '#006064', '#1a237e', '#004d73', '#00334e'],
        line=dict(color='white', width=3)
    ),
    pull=[0.05 if i == 0 else 0 for i in range(len(category_counts))]  # Pull out first slice
)])

fig.update_layout(
    height=600,
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255, 255, 255, 0.95)",
        bordercolor="#0d47a1",
        borderwidth=2,
        font=dict(
            size=12,
            family='Arial',
            color='#0d47a1',
            weight='bold'
        )
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=11, color='#0d47a1'),
    margin=dict(l=0, r=300, t=20, b=20),
    title=dict(
        text='',
        x=0.5,
        xanchor='center'
    )
)

st.plotly_chart(fig, use_container_width=True)

# Add detailed statistics table
st.markdown("""
<div class="category-stats">
    <h4 style="color: #0d47a1; margin-bottom: 1.5rem; font-size: 1.2rem; font-weight: bold;">Category Statistics</h4>
    <table style="width: 100%; border-collapse: collapse; font-size: 0.95rem;">
        <thead>
            <tr style="background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%); color: white;">
                <th style="padding: 1.2rem; text-align: left; font-weight: bold; border-radius: 8px 0 0 0;">Category</th>
                <th style="padding: 1.2rem; text-align: center; font-weight: bold;">Count</th>
                <th style="padding: 1.2rem; text-align: center; font-weight: bold; border-radius: 0 8px 0 0;">Percentage</th>
            </tr>
        </thead>
        <tbody>
""", unsafe_allow_html=True)

category_stats_df = pd.DataFrame({
    'Category': category_counts.index,
    'Count': category_counts.values,
    'Percentage': (category_counts.values / category_counts.sum() * 100).round(1)
})

# Generate table rows
for idx, row in category_stats_df.iterrows():
    bg_color = 'rgba(0, 188, 212, 0.08)' if idx % 2 == 0 else 'white'
    progress_width = (row['Percentage'] / category_stats_df['Percentage'].max()) * 100
    
    st.markdown(f"""
            <tr style="background-color: {bg_color}; transition: all 0.3s ease;">
                <td style="padding: 1.2rem; font-weight: 600; color: #0d47a1; border-bottom: 1px solid rgba(0, 188, 212, 0.1);">
                    {row['Category']}
                </td>
                <td style="padding: 1.2rem; text-align: center; font-weight: bold; color: #1976d2; border-bottom: 1px solid rgba(0, 188, 212, 0.1);">
                    {int(row['Count'])}
                </td>
                <td style="padding: 1.2rem; text-align: center; border-bottom: 1px solid rgba(0, 188, 212, 0.1);">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                        <div style="width: 60px; height: 6px; background: #e0e0e0; border-radius: 3px; overflow: hidden;">
                            <div style="width: {progress_width}%; height: 100%; background: linear-gradient(90deg, #00bcd4, #0097a7); border-radius: 3px;"></div>
                        </div>
                        <span style="font-weight: bold; color: #0d47a1; min-width: 50px;">{row['Percentage']:.1f}%</span>
                    </div>
                </td>
            </tr>
    """, unsafe_allow_html=True)

st.markdown("""
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 4. Average Engagement by Category
st.markdown("""
<div class="chart-container">
    <h3> Average Engagement Rate by Category</h3>
    <p class="chart-description">Which content categories have the most engaged audiences?</p>
""", unsafe_allow_html=True)

category_eng = df[df['Category'].notna()].groupby('Category')['Eng Rate'].mean().sort_values(ascending=False).head(12)

fig = go.Figure(data=[
    go.Bar(
        x=category_eng.index,
        y=category_eng.values,
        marker=dict(
            color=category_eng.values,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title="Engagement %",
                thickness=20,
                len=0.7
            ),
            line=dict(color='#0d47a1', width=2)
        ),
        hovertemplate='<b>%{x}</b><br>Avg Engagement: %{y:.2f}%<extra></extra>',
        text=[f'{val:.2f}%' for val in category_eng.values],
        textposition='outside',
        textfont=dict(size=11, color='#0d47a1', family='Arial', weight='bold')
    )
])

fig.update_layout(
    xaxis_title="Category",
    yaxis_title="Average Engagement Rate (%)",
    height=500,
    hovermode='x unified',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=11, color='#0d47a1'),
    xaxis=dict(
        tickangle=-45,
        tickfont=dict(size=10, weight='bold')
    ),
    yaxis=dict(
        tickfont=dict(size=10, weight='bold')
    ),
    margin=dict(b=120, t=50, l=60, r=80)
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. Channel Type Distribution
st.markdown("""
<div class="chart-container">
    <h3> Influencers by Channel Type</h3>
    <p class="chart-description">Breakdown of creators: Brands vs Individual influencers</p>
""", unsafe_allow_html=True)

channel_counts = df['channel_Info'].value_counts()

fig = go.Figure(data=[
    go.Bar(
        x=channel_counts.index,
        y=channel_counts.values,
        marker=dict(
            color=['#0d47a1', '#1976d2', '#00bcd4'],
            line=dict(color='white', width=3)
        ),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
        text=channel_counts.values,
        textposition='outside',
        textfont=dict(size=12, color='#0d47a1', family='Arial', weight='bold')
    )
])

fig.update_layout(
    xaxis_title="Channel Type",
    yaxis_title="Number of Influencers",
    height=500,
    hovermode='x',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=11, color='#0d47a1'),
    xaxis=dict(
        tickfont=dict(size=11, weight='bold')
    ),
    yaxis=dict(
        tickfont=dict(size=10, weight='bold')
    ),
    margin=dict(t=50, b=60, l=60, r=40)
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. Top Posts
st.markdown("""
<div class="chart-container">
    <h3> Most Active Influencers (by Posts)</h3>
    <p class="chart-description">Creators with the highest posting frequency</p>
""", unsafe_allow_html=True)

top_posts = df.nlargest(12, 'Posts')

fig = go.Figure(data=[
    go.Bar(
        y=top_posts['name'],
        x=top_posts['Posts'],
        orientation='h',
        marker=dict(
            color=top_posts['Posts'],
            colorscale='Spectral',
            showscale=False,
            line=dict(color='#0d47a1', width=2)
        ),
        hovertemplate='<b>%{y}</b><br>Posts: %{x:,.0f}<extra></extra>',
        text=[f'{int(val):,.0f}' for val in top_posts['Posts']],
        textposition='outside',
        textfont=dict(size=10, color='#0d47a1', family='Arial', weight='bold')
    )
])

fig.update_layout(
    xaxis_title="Number of Posts",
    yaxis_title="Influencer",
    height=600,
    hovermode='y unified',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial', size=11, color='#0d47a1'),
    xaxis=dict(
        tickfont=dict(size=10, weight='bold')
    ),
    yaxis=dict(
        tickfont=dict(size=10, weight='bold', family='Arial')
    ),
    margin=dict(l=150, r=100, t=50, b=60)
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer spacing
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)