import streamlit as st
import pandas as pd

st.set_page_config(page_title="Influencer Impact Analyzer", layout="wide", initial_sidebar_state="collapsed")

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
    
    /* ========== TOP PADDING FOR NAVBAR ========== */
    .st-emotion-cache-6qob1r {
        padding-top: 100px !important;
    }
    
    /* ========== HERO WITH BACKGROUND IMAGE ========== */
    .hero {
        padding-top: 60px;
        padding-bottom: 5rem;
        padding-left: 4rem;
        padding-right: 4rem;
        background: linear-gradient(135deg, rgba(13, 71, 161, 0.92) 0%, rgba(25, 118, 210, 0.88) 50%, rgba(0, 188, 212, 0.35) 100%), 
                    url('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1400&h=700&fit=crop') center/cover;
        background-blend-mode: overlay;
        background-attachment: fixed;
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(0, 188, 212, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(13, 71, 161, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 0%, rgba(0, 188, 212, 0.08) 0%, transparent 60%);
        pointer-events: none;
        animation: floatingLight 15s ease-in-out infinite;
    }
    
    .hero::after {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0, 188, 212, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        top: -100px;
        right: -100px;
        animation: floatParticle 20s ease-in-out infinite;
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero h1 {
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        letter-spacing: -2px;
        animation: slideInDown 0.8s ease-out;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .hero p {
        font-size: 1.3rem;
        font-weight: 400;
        animation: slideInUp 0.8s ease-out 0.2s both;
        text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
        max-width: 700px;
        line-height: 1.6;
    }
    
    /* ========== CONTAINER ========== */
    .container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 5rem 2rem;
    }
    
    .card {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(13, 71, 161, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(0, 188, 212, 0.1);
        animation: fadeInUp 0.6s ease-out backwards;
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    
    .card:nth-child(1) { animation-delay: 0.1s; }
    .card:nth-child(2) { animation-delay: 0.2s; }
    .card:nth-child(3) { animation-delay: 0.3s; }
    
    .card:hover {
        transform: translateY(-12px);
        box-shadow: 0 20px 50px rgba(0, 188, 212, 0.35);
        border-color: rgba(0, 188, 212, 0.5);
    }
    
    .card:hover .card-image {
        filter: brightness(1.1);
    }
    
    .card-image {
        background-size: cover;
        background-position: center;
        background-blend-mode: overlay;
        height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .card-image::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(13, 71, 161, 0.65) 0%, rgba(25, 118, 210, 0.6) 50%, rgba(0, 188, 212, 0.5) 100%);
        pointer-events: none;
        z-index: 1;
    }
    
    .card-image::after {
        content: '';
        position: absolute;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(0, 188, 212, 0.25) 0%, transparent 70%);
        border-radius: 50%;
        top: -50px;
        right: -50px;
        animation: floatIcon 6s ease-in-out infinite;
        z-index: 1;
    }
    
    .card-icon {
        position: relative;
        z-index: 2;
        filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.4));
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .card-content {
        padding: 2rem;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        justify-content: space-between;
    }
    
    .card-name {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0d47a1;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
        line-height: 1.3;
    }
    
    .card-stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        width: 100%;
    }
    
    .stat {
        display: flex;
        flex-direction: column;
        padding: 1rem;
        background: rgba(0, 188, 212, 0.08);
        border-radius: 8px;
        border-left: 3px solid #00bcd4;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stat:hover {
        background: rgba(0, 188, 212, 0.15);
        transform: translateX(4px);
    }
    
    .stat-content {
        display: flex;
        flex-direction: column;
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: #1976d2;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    
    .stat-value {
        font-size: 1.15rem;
        font-weight: 900;
        color: #0d47a1;
    }
    
    /* ========== SECTION DIVIDER ========== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 188, 212, 0.2), transparent);
        margin: 6rem 0;
    }
    
    /* ========== METRICS ========== */
    .metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 2rem;
        margin: 5rem 0 6rem 0;
        padding: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 10px 35px rgba(0, 188, 212, 0.2);
        animation: fadeInUp 0.6s ease-out backwards;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .metric-card:nth-child(1) { animation-delay: 0s; }
    .metric-card:nth-child(2) { animation-delay: 0.1s; }
    .metric-card:nth-child(3) { animation-delay: 0.2s; }
    .metric-card:nth-child(4) { animation-delay: 0.3s; }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 60px rgba(0, 188, 212, 0.35);
    }
    
    .metric-number {
        font-size: 2.8rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        display: block;
        position: relative;
        z-index: 1;
    }
    
    .metric-text {
        font-size: 0.95rem;
        font-weight: 600;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }
    
    /* ========== CTA ========== */
    .cta {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #00bcd4 30%);
        padding: 5rem 4rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 4rem 0;
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 50px rgba(0, 188, 212, 0.25);
    }
    
    .cta::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 50%, rgba(0, 188, 212, 0.2) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .cta h2 {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .cta p {
        font-size: 1.15rem;
        opacity: 0.95;
        margin-bottom: 2.5rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* ========== BUTTON ========== */
    .stButton > button {
        background: linear-gradient(135deg, #00bcd4 0%, #0097a7 100%) !important;
        color: white !important;
        padding: 1rem 3rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 50px !important;
        box-shadow: 0 10px 30px rgba(0, 188, 212, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 18px 55px rgba(0, 188, 212, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* ========== FOOTER ========== */
    .footer {
        text-align: center;
        padding: 3rem;
        color: #999;
        font-size: 0.9rem;
        border-top: 1px solid rgba(0, 188, 212, 0.1);
        margin-top: 5rem;
    }
    
    /* ========== ANIMATIONS ========== */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
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
    
    @keyframes floatIcon {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(10px, -10px); }
    }
    
    @keyframes floatingLight {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(-20px, 20px); }
    }
    
    @keyframes floatParticle {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(30px, -30px) scale(1.1); }
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 1400px) {
        .cards-grid {
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
        }
    }
    
    @media (max-width: 1024px) {
        .cards-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 1.8rem;
        }
        
        .card-image {
            height: 200px;
        }
        
        .card-name {
            font-size: 1.1rem;
        }
        
        .hero h1 {
            font-size: 2.8rem;
        }
        
        .hero p {
            font-size: 1.1rem;
        }
    }
    
    @media (max-width: 768px) {
        .hero {
            padding: 80px 2rem 4rem 2rem;
            min-height: 400px;
        }
        
        .card-image {
            height: 160px;
            font-size: 2rem;
        }
        
        .card-content {
            padding: 1.2rem;
        }
        
        .card-stats {
            grid-template-columns: 1fr;
            gap: 0.6rem;
        }
        
        .stat {
            padding: 0.6rem;
        }
        
        .card-name {
            font-size: 1rem;
            margin-bottom: 0.8rem;
        }
        
        .stat-label {
            font-size: 0.65rem;
        }
        
        .stat-value {
            font-size: 0.95rem;
        }
        
        .hero h1 {
            font-size: 2rem;
        }
        
        .hero p {
            font-size: 1rem;
        }
        
        .container {
            padding: 3rem 1.5rem;
        }
        
        .cta {
            padding: 3rem 2rem;
        }
        
        .cta h2 {
            font-size: 1.8rem;
        }
        
        .metrics {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (max-width: 480px) {
        .hero {
            padding: 80px 1.5rem 3rem 1.5rem;
            min-height: 350px;
        }
        
        .hero h1 {
            font-size: 1.5rem;
        }
        
        .hero p {
            font-size: 0.95rem;
        }
        
        .card-image {
            height: 140px;
            font-size: 1.8rem;
        }
        
        .card-name {
            font-size: 0.95rem;
            margin-bottom: 0.6rem;
        }
        
        .card-stats {
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }
        
        .stat {
            padding: 0.5rem;
        }
        
        .card-content {
            padding: 1rem;
        }
        
        .metrics {
            grid-template-columns: 1fr;
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
        
        document.querySelectorAll('.card, .metric-card').forEach(card => {
            observer.observe(card);
        });
    });
</script>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data_cleaned.csv")

df = load_data()

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>Influencer Impact</h1>
        <p>Discover & Analyze the Top 200 Instagram Influencers. Find engagement rates, followers, and the perfect creators for your brand.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Container
st.markdown('<div class="container">', unsafe_allow_html=True)

# Top 8 influencers
top_8 = df.nlargest(8, 'Eng Rate')

# Background images for variety
bg_images = [
    'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1511379938547-c1f69b13d835?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1542838132-92c53300491e?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1516321318423-f06f70259b51?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop',
    'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=600&h=400&fit=crop',
]

emojis = ['👸', '🎤', '⚽', '💪', '✨', '🎬', '🏆', '🌟']

# Display cards
cols = st.columns(3, gap="large")

for idx, (_, row_data) in enumerate(top_8.iterrows()):
    col = cols[idx % 3]
    
    emoji = emojis[idx % len(emojis)]
    followers = int(row_data['Followers'] / 1_000_000)
    engagement = f"{row_data['Eng Rate']:.1f}%"
    category = str(row_data['Category'])[:20] if pd.notna(row_data['Category']) else "Creator"
    likes = int(row_data['Avg. Likes'])
    bg_image = bg_images[idx % len(bg_images)]
    
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="card-image" style="background-image: url('{bg_image}');">
                <div class="card-icon">{emoji}</div>
            </div>
            <div class="card-content">
                <div>
                    <h3 class="card-name">{row_data['name']}</h3>
                </div>
                <div class="card-stats">
                    <div class="stat">
                        <div class="stat-content">
                            <span class="stat-label">Followers</span>
                            <span class="stat-value">{followers}M</span>
                        </div>
                    </div>
                    <div class="stat">
                        <div class="stat-content">
                            <span class="stat-label">Engagement</span>
                            <span class="stat-value">{engagement}</span>
                        </div>
                    </div>
                    <div class="stat">
                        <div class="stat-content">
                            <span class="stat-label">Avg Likes</span>
                            <span class="stat-value">{likes:,}</span>
                        </div>
                    </div>
                    <div class="stat">
                        <div class="stat-content">
                            <span class="stat-label">Category</span>
                            <span class="stat-value" style="font-size: 0.9rem;">{category}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Metrics Section
st.markdown("""
<div class="section-divider"></div>
""", unsafe_allow_html=True)

st.markdown('<div class="metrics">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-number">{len(df)}</span>
        <span class="metric-text">Total Influencers</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-number">{int(df['Followers'].mean()/1_000_000)}M</span>
        <span class="metric-text">Avg Followers</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-number">{int(df['Avg. Likes'].mean()):,}</span>
        <span class="metric-text">Avg Likes Per Post</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-number">{df['Eng Rate'].mean():.2f}%</span>
        <span class="metric-text">Avg Engagement</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# CTA
st.markdown(f"""
<div class="cta">
    <h2>Ready to Find Your Perfect Influencer?</h2>
    <p>Explore detailed analytics, advanced search filters, and strategic insights for your brand</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button(" Go to Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p> Built with Streamlit | Data-Driven Intelligence | 200+ Top Influencers Analyzed</p>
</div>
""", unsafe_allow_html=True)