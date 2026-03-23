# ⚡ Influencer Impact Analyzer

> **Beyond follower counts — measuring real influence.**

A data-driven web application that analyzes the top 200 Instagram influencers using a custom **Impact Score** metric, proving that audience engagement matters more than raw follower numbers.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://influencer-impact-analyzer.streamlit.app/)

---

## 🔍 The Problem

Most people (and brands) judge influencer value by **follower count alone**. But our data reveals the truth:

> A creator with **500K followers & 8% engagement** has more real influence than one with **50M followers & 0.3% engagement**.

This project quantifies that gap.

---

## ⚡ The Impact Score Formula

```
Impact Score = Engagement Rate × log₁₀(Followers)
```

This formula balances **reach** (followers) and **quality** (engagement) into a single comparable metric — inspired by real-world influence measurement research.

---

## 📸 App Preview

| Page | Description |
|------|-------------|
| 🏠 Home | Top influencers with category-based visuals |
| 📊 Dashboard | Search, filter & sort by Impact Score |
| 📈 Analysis | 7 interactive charts & trend visualizations |
| 💡 Insights | Key findings, paradox proof & recommendations |

---

## 🔑 Key Findings

### The Influence Paradox
The bottom 25% of influencers by follower count consistently generate **significantly higher engagement** than the top 25% — proving follower count is a misleading metric.

### Weak Followers↔Engagement Correlation
Our correlation analysis shows a **weak negative correlation** between followers and engagement rate — the more followers, the lower the engagement tends to be.

### Category Matters
Engagement rates vary dramatically across categories. The best-performing category outperforms the worst by over **3x** — meaning niche selection is as important as influencer selection.

### Posting Frequency ≠ Better Engagement
Influencers who post the most don't top the engagement charts — quality beats quantity here too.

---

## 🛠️ Tech Stack

| Technology | Usage |
|-----------|-------|
| **Streamlit** | Web app framework & UI |
| **Pandas** | Data manipulation & filtering |
| **NumPy** | Impact Score calculation |
| **Plotly** | Interactive charts (pie, bar, scatter) |
| **Matplotlib + Seaborn** | Static visualizations |
| **Python 3.9+** | Core language |

---

## 📁 Project Structure

```
Influencer-Impact-Analyzer/
│
├── Home.py                  # Landing page — top 8 by Impact Score
├── data_cleaned.csv         # Dataset — 200 top Instagram influencers
│
└── pages/
    ├── 1_Dashboard.py       # Search, filter, sort + Influence Paradox
    ├── 2_Analysis.py        # 7 charts & visual analysis
    └── 3_Insights.py        # Findings, stats & recommendations
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/NainaKothari-14/Influencer-Impact-Analyzer.git
cd Influencer-Impact-Analyzer
```

**2. Install dependencies**
```bash
pip install streamlit pandas numpy plotly matplotlib seaborn
```

**3. Run the app**
```bash
streamlit run Home.py
```

**4. Open in browser**
```
http://localhost:8501
```

---

## 📊 Dataset

- **200** top Instagram influencers
- **Columns:** `rank`, `name`, `Category`, `Followers`, `Avg. Likes`, `Eng Rate`, `Posts`, `channel_Info`
- **Derived column:** `Impact Score` — calculated at runtime

---

## 📄 Pages Breakdown

### 🏠 Home
- Hero section with project branding
- Top 8 influencers ranked by Impact Score
- Category-matched thematic photos for each card
- Key dataset metrics

### 📊 Dashboard
- Real-time search by influencer name
- Filter by category
- Sort by Impact Score, Engagement Rate, Followers, Posts, Avg Likes
- **Influence Paradox Banner** — live calculated from data
- Full sortable table with Impact Score column

### 📈 Analysis
1. Top 15 by Impact Score
2. Top 15 by Engagement Rate *(comparison with above)*
3. Followers vs Engagement Rate scatter — trend annotation
4. Posts vs Engagement Rate scatter — frequency vs quality
5. Category distribution donut chart
6. Avg Engagement Rate by Category — with data-driven annotation
7. Channel type breakdown (Brand vs Individual)

### 💡 Insights
- Impact Score methodology explanation
- 5 key metric cards including correlation value
- Influence Paradox — 3-stat proof with multiplier
- Top Performers grid (Impact, Engagement, Followers, Best Category)
- Correlation badge with interpretation
- Category performance table with Impact Score column
- 6 data-driven strategic recommendations
- Full dataset statistics

---

## 👩‍💻 Team

Built as part of a data analysis project.

---

## 📝 License

This project is for educational purposes.

---

<div align="center">
  <strong>⚡ Impact Score = Engagement Rate × log₁₀(Followers)</strong><br>
  <em>Because quality of influence matters more than quantity.</em>
</div>
