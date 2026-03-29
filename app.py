import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Superstore Sales Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #F0F4F0; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1B5E20;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #C8E6C9 !important;
        font-weight: 600;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF !important;
        border-left: 5px solid #1B5E20 !important;
        border-top: 1px solid #A5D6A7 !important;
        border-right: 1px solid #A5D6A7 !important;
        border-bottom: 1px solid #A5D6A7 !important;
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 4px 12px rgba(27,94,32,0.15);
    }
    div[data-testid="metric-container"] label {
        color: #1B5E20 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #1B5E20 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        color: #388E3C !important;
    }

    /* Headers */
    h1, h2, h3 { color: #1B5E20 !important; }

    /* Chart containers */
    .chart-container {
        background: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #A5D6A7;
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Page header */
    .page-header {
        background: linear-gradient(135deg, #1B5E20, #2E7D32);
        color: white;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(27,94,32,0.3);
    }
    .page-header h1 {
        color: white !important;
        margin: 0;
        font-size: 26px;
    }
    .page-header p {
        color: #C8E6C9;
        margin: 5px 0 0 0;
        font-size: 14px;
    }

    /* Divider */
    hr { border-color: #A5D6A7; }

    /* Insight boxes */
    .insight-box {
        background: #E8F5E9;
        border-left: 4px solid #2E7D32;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 10px 0;
        color: #1B5E20;
        font-size: 14px;
    }
    .warning-box {
        background: #FFEBEE;
        border-left: 4px solid #C62828;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 10px 0;
        color: #B71C1C;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('superstore_clean.csv', encoding='utf-8')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=True)
    df['Ship Date']  = pd.to_datetime(df['Ship Date'],  format='mixed', dayfirst=True)
    return df

df = load_data()

# ─── Matplotlib Styling ───────────────────────────────────────────────────────
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor']   = 'white'
plt.rcParams['axes.grid']        = True
plt.rcParams['grid.color']       = '#E8F5E9'
plt.rcParams['grid.linewidth']   = 0.8
plt.rcParams['font.family']      = 'DejaVu Sans'
plt.rcParams['axes.spines.top']  = False
plt.rcParams['axes.spines.right']= False

GREEN_PALETTE = ['#1B5E20','#2E7D32','#388E3C','#43A047','#66BB6A','#81C784','#A5D6A7','#C8E6C9']
RED_GREEN     = ['#C62828','#E53935','#EF5350','#A5D6A7','#66BB6A','#2E7D32','#1B5E20']

# ─── Custom KPI Card Function ─────────────────────────────────────────────────
def kpi_card(col, icon, label, value, sub="", color="#1B5E20"):
    with col:
        st.markdown(f"""
        <div style="background:#FFFFFF; border-radius:12px;
                    border-left: 6px solid {color};
                    border-top: 1px solid #C8E6C9;
                    border-right: 1px solid #C8E6C9;
                    border-bottom: 1px solid #C8E6C9;
                    padding: 16px 18px;
                    box-shadow: 2px 4px 12px rgba(27,94,32,0.12);">
            <div style="color:#388E3C; font-size:12px; font-weight:700;
                        text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">
                {icon} {label}
            </div>
            <div style="color:#1B5E20; font-size:26px; font-weight:800; line-height:1.1;">
                {value}
            </div>
            <div style="color:#66BB6A; font-size:11px; margin-top:4px;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 5px 0;">
        <div style="font-size:28px;">🛒</div>
        <div style="color:#FFFFFF; font-size:16px; font-weight:700; margin-top:4px;">E-Commerce Superstore</div>
        <div style="color:#A5D6A7; font-size:12px; margin-top:2px;">Sales Analysis Dashboard</div>
        <div style="color:#81C784; font-size:11px; margin-top:2px;">2014 – 2017</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = st.selectbox(
        "📄 Navigate To",
        ["🏠 Overview", "📦 Product Analysis", "🗺️ Regional Analysis", "💰 Profitability Analysis"]
    )

    st.markdown("---")
    st.markdown("### 🔍 Filters")

    # Year filter
    years = sorted(df['Order_Year'].unique())
    selected_years = st.multiselect("📅 Year", years, default=years)

    # Category filter
    categories = sorted(df['Category'].unique())
    selected_cats = st.multiselect("📦 Category", categories, default=categories)

    # Region filter
    regions = sorted(df['Region'].unique())
    selected_regions = st.multiselect("🗺️ Region", regions, default=regions)

    # Segment filter
    segments = sorted(df['Segment'].unique())
    selected_segs = st.multiselect("👥 Segment", segments, default=segments)

    st.markdown("---")
    st.markdown("### 📊 Dataset Info")
    st.markdown(f"**Rows:** {len(df):,}")
    st.markdown(f"**Columns:** {df.shape[1]}")
    st.markdown(f"**Period:** 2014–2017")

# ─── Apply Filters ────────────────────────────────────────────────────────────
filtered = df[
    (df['Order_Year'].isin(selected_years)) &
    (df['Category'].isin(selected_cats)) &
    (df['Region'].isin(selected_regions)) &
    (df['Segment'].isin(selected_segs))
]

if filtered.empty:
    st.warning("⚠️ No data matches current filters. Please adjust filters.")
    st.stop()

# ─── Top Project Banner ───────────────────────────────────────────────────────
st.markdown("""
<div style="background: #1B5E20; border-radius: 12px; padding: 16px 24px;
            margin-bottom: 20px; display: flex; align-items: center;
            justify-content: space-between;">
    <div>
        <div style="color: #FFFFFF; font-size: 22px; font-weight: 700; margin-bottom: 2px;">
            🛒 E-Commerce Superstore Sales Analysis
        </div>
        <div style="color: #A5D6A7; font-size: 13px;">
            End-to-End Data Analysis | Python • PostgreSQL • Streamlit | Period: 2014–2017
        </div>
    </div>
    <div style="text-align: right;">
        <div style="color: #C8E6C9; font-size: 12px;">Total Records</div>
        <div style="color: #FFFFFF; font-size: 20px; font-weight: 700;">9,994</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    st.markdown("""
    <div class="page-header">
        <h1>🏠 Overview Dashboard</h1>
        <p>High-level KPIs and sales trends across all dimensions</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpi_card(k1, "💰", "Total Revenue",    f"${filtered['Sales'].sum():,.0f}",  "Total 4 Years")
    kpi_card(k2, "📈", "Total Profit",     f"${filtered['Profit'].sum():,.0f}", "Net Earnings")
    kpi_card(k3, "🛒", "Total Orders",     f"{filtered['Order ID'].nunique():,}","Unique Orders")
    kpi_card(k4, "📊", "Avg Profit Margin",f"{filtered['Profit_Margin_%'].mean():.2f}%", "Overall Margin")

    st.markdown("---")

    # ── Row 2: Category Donut + Region Bar ────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        cat_sales = filtered.groupby('Category')['Sales'].sum()
        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(
            cat_sales.values,
            labels=cat_sales.index,
            autopct='%1.1f%%',
            colors=['#1B5E20','#66BB6A','#C8E6C9'],
            startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=2),
            pctdistance=0.75
        )
        for at in autotexts:
            at.set_fontsize(10)
            at.set_fontweight('bold')
            at.set_color('white')
        centre = plt.Circle((0,0), 0.50, fc='white')
        ax.add_patch(centre)
        ax.set_title('Sales by Category', fontsize=13, fontweight='bold', color='#1B5E20', pad=15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        reg = filtered.groupby('Region').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
        reg = reg.sort_values('Sales', ascending=True)
        fig, ax = plt.subplots(figsize=(6, 4))
        x = np.arange(len(reg))
        w = 0.4
        ax.barh(x - w/2, reg['Sales'], w, label='Sales',  color='#2E7D32', edgecolor='white')
        ax.barh(x + w/2, reg['Profit'], w, label='Profit', color='#81C784', edgecolor='white')
        ax.set_yticks(x)
        ax.set_yticklabels(reg['Region'], fontsize=10)
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))
        ax.set_title('Sales & Profit by Region', fontsize=13, fontweight='bold', color='#1B5E20')
        ax.legend(fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3: Monthly Sales Trend ─────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    monthly = filtered.groupby('Year_Month').agg(
        Sales=('Sales','sum'), Profit=('Profit','sum')
    ).reset_index().sort_values('Year_Month')

    fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=True)

    axes[0].fill_between(range(len(monthly)), monthly['Sales'], alpha=0.3, color='#2E7D32')
    axes[0].plot(range(len(monthly)), monthly['Sales'], color='#1B5E20', linewidth=2, marker='o', markersize=3)
    axes[0].set_title('Monthly Sales Trend (2014–2017)', fontsize=13, fontweight='bold', color='#1B5E20')
    axes[0].set_ylabel('Sales ($)')
    axes[0].yaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))

    axes[1].fill_between(range(len(monthly)), monthly['Profit'],
                         where=(monthly['Profit'] >= 0), alpha=0.3, color='#4CAF50', label='Profit')
    axes[1].fill_between(range(len(monthly)), monthly['Profit'],
                         where=(monthly['Profit'] < 0),  alpha=0.3, color='#F44336', label='Loss')
    axes[1].plot(range(len(monthly)), monthly['Profit'], color='#388E3C', linewidth=2, marker='o', markersize=3)
    axes[1].axhline(0, color='#C62828', linewidth=1, linestyle='--')
    axes[1].set_title('Monthly Profit Trend', fontsize=13, fontweight='bold', color='#1B5E20')
    axes[1].set_ylabel('Profit ($)')
    axes[1].yaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))
    axes[1].legend()

    step = max(1, len(monthly)//12)
    axes[1].set_xticks(range(0, len(monthly), step))
    axes[1].set_xticklabels(monthly['Year_Month'].iloc[::step], rotation=45, ha='right', fontsize=8)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Insights ──────────────────────────────────────────────────────────────
    st.markdown("### 💡 Key Insights")
    i1, i2 = st.columns(2)
    with i1:
        st.markdown('<div class="insight-box">📈 <b>Technology</b> leads in both Sales ($836K) and Profit ($145K) — best performing category!</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-box">🌍 <b>West region</b> contributes 37.9% of total profit despite 31.6% of sales — highest efficiency!</div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div class="warning-box">⚠️ <b>18.7% orders</b> are loss-making — discount strategy needs revision!</div>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">⚠️ <b>Furniture</b> is 2nd in sales but last in profit — only 2.5% margin!</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📦 Product Analysis":

    st.markdown("""
    <div class="page-header">
        <h1>📦 Product Analysis</h1>
        <p>Category, Sub-Category and Product level performance</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    best_cat  = filtered.groupby('Category')['Profit'].sum().idxmax()
    worst_sub = filtered.groupby('Sub-Category')['Profit'].sum().idxmin()
    kpi_card(k1, "📦", "Total Products",    f"{filtered['Product ID'].nunique():,}", "Unique Products")
    kpi_card(k2, "🏆", "Best Category",     best_cat,                               "Highest Profit")
    kpi_card(k3, "⚠️", "Loss Sub-Category", worst_sub,                              "Needs Attention", color="#C62828")
    kpi_card(k4, "📊", "Avg Revenue/Unit",  f"${filtered['Revenue_Per_Unit'].mean():,.2f}", "Per Item")

    st.markdown("---")

    # ── Row 2: Sub-Category Profit + Category Sales ───────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        sub_profit = filtered.groupby('Sub-Category')['Profit'].sum().sort_values()
        colors = ['#C62828' if v < 0 else '#2E7D32' for v in sub_profit.values]
        fig, ax = plt.subplots(figsize=(6, 7))
        ax.barh(sub_profit.index, sub_profit.values, color=colors, edgecolor='white')
        ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
        ax.set_title('Profit by Sub-Category', fontsize=13, fontweight='bold', color='#1B5E20')
        ax.set_xlabel('Total Profit ($)')
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        sub_sales = filtered.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 7))
        ax.barh(sub_sales.index[::-1], sub_sales.values[::-1], color='#2E7D32', edgecolor='white')
        ax.set_title('Sales by Sub-Category', fontsize=13, fontweight='bold', color='#1B5E20')
        ax.set_xlabel('Total Sales ($)')
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3: Category × Year Heatmap ────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    pivot = filtered.pivot_table(
        values='Sales', index='Category',
        columns='Order_Year', aggfunc='sum'
    ).fillna(0)

    fig, ax = plt.subplots(figsize=(10, 3))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='Greens',
                linewidths=0.5, ax=ax,
                annot_kws={'size': 11, 'weight': 'bold'})
    ax.set_title('Category Sales by Year ($)', fontsize=13, fontweight='bold', color='#1B5E20', pad=15)
    ax.set_xlabel('Year')
    ax.set_ylabel('Category')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 4: Top 10 Products ─────────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    top_products = filtered.groupby('Product Name')[['Sales','Profit']].sum().nlargest(10, 'Sales')
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(top_products))
    w = 0.4
    ax.bar(x - w/2, top_products['Sales'],  w, label='Sales',  color='#2E7D32', edgecolor='white')
    ax.bar(x + w/2, top_products['Profit'], w, label='Profit', color='#81C784', edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels([name[:30]+'...' if len(name)>30 else name
                        for name in top_products.index], rotation=30, ha='right', fontsize=8)
    ax.set_title('Top 10 Products by Sales', fontsize=13, fontweight='bold', color='#1B5E20')
    ax.set_ylabel('Amount ($)')
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Insights ──────────────────────────────────────────────────────────────
    st.markdown("### 💡 Key Insights")
    i1, i2 = st.columns(2)
    with i1:
        st.markdown('<div class="insight-box">🏆 <b>Copiers</b> — low sales but highest profit! Premium pricing with minimal discounts.</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-box">📈 <b>Phones</b> — #1 in sales AND #2 in profit — best volume+margin combination!</div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div class="warning-box">⚠️ <b>Tables</b> — decent sales but biggest loss maker (-$18K). Heavy discounting issue!</div>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">⚠️ <b>Bookcases</b> — 228 orders but -$12K profit — pricing review needed!</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REGIONAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Regional Analysis":

    st.markdown("""
    <div class="page-header">
        <h1>🗺️ Regional Analysis</h1>
        <p>State-wise and Region-wise sales and profit performance</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    best_region  = filtered.groupby('Region')['Profit'].sum().idxmax()
    worst_state  = filtered.groupby('State')['Profit'].sum().idxmin()
    best_state   = filtered.groupby('State')['Profit'].sum().idxmax()
    total_states = filtered['State'].nunique()
    kpi_card(k1, "🏆", "Best Region",  best_region,         "Highest Profit")
    kpi_card(k2, "🌟", "Best State",   best_state,          "Top Performer")
    kpi_card(k3, "⚠️", "Loss State",   worst_state,         "Needs Fix", color="#C62828")
    kpi_card(k4, "📍", "Total States", f"{total_states}",   "Covered")

    st.markdown("---")

    # ── Row 2: Region Pie Charts ───────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    reg_data = filtered.groupby('Region').agg(
        Sales=('Sales','sum'),
        Profit=('Profit','sum'),
        Orders=('Order ID','nunique')
    )
    pie_colors = ['#1B5E20','#43A047','#81C784','#C8E6C9']

    for col, metric, title in zip([c1,c2,c3],
                                   ['Sales','Profit','Orders'],
                                   ['Sales Share','Profit Share','Order Count']):
        with col:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(reg_data[metric], labels=reg_data.index,
                   autopct='%1.1f%%', colors=pie_colors,
                   startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2))
            ax.set_title(f'{title} by Region', fontsize=11, fontweight='bold', color='#1B5E20')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3: Top & Bottom States ────────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        top_states = filtered.groupby('State')[['Sales','Profit']].sum().nlargest(10,'Sales')
        fig, ax = plt.subplots(figsize=(6, 5))
        x = np.arange(len(top_states))
        w = 0.4
        ax.bar(x - w/2, top_states['Sales'],  w, label='Sales',  color='#2E7D32', edgecolor='white')
        ax.bar(x + w/2, top_states['Profit'], w, label='Profit',
               color=['#C62828' if v < 0 else '#81C784' for v in top_states['Profit']],
               edgecolor='white')
        ax.set_xticks(x)
        ax.set_xticklabels(top_states.index, rotation=30, ha='right', fontsize=8)
        ax.set_title('Top 10 States by Sales', fontsize=12, fontweight='bold', color='#1B5E20')
        ax.set_ylabel('Amount ($)')
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))
        ax.axhline(0, color='black', linewidth=0.5)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        loss_states = filtered.groupby('State')['Profit'].sum()
        loss_states = loss_states[loss_states < 0].sort_values()
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.barh(loss_states.index, loss_states.values, color='#C62828', edgecolor='white')
        ax.axvline(0, color='black', linewidth=0.8)
        ax.set_title('States with Negative Profit', fontsize=12, fontweight='bold', color='#C62828')
        ax.set_xlabel('Total Profit ($)')
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 4: Segment × Region ───────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    seg_reg = filtered.groupby(['Region','Segment'])['Sales'].sum().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 4))
    seg_reg.plot(kind='bar', ax=ax, color=['#1B5E20','#66BB6A','#C8E6C9'], edgecolor='white', width=0.7)
    ax.set_title('Sales by Region & Customer Segment', fontsize=13, fontweight='bold', color='#1B5E20')
    ax.set_ylabel('Sales ($)')
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v,_: f'${v/1000:.0f}K'))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=10)
    ax.legend(title='Segment', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Insights ──────────────────────────────────────────────────────────────
    st.markdown("### 💡 Key Insights")
    i1, i2 = st.columns(2)
    with i1:
        st.markdown('<div class="insight-box">🌍 <b>West</b> — 31.6% sales but 37.9% profit — best profit efficiency of all regions!</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-box">🌟 <b>California & New York</b> — top 2 states, both profitable with strong margins!</div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div class="warning-box">⚠️ <b>Central region</b> — 21.8% sales but only 13.9% profit — heavy discounting!</div>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">⚠️ <b>Texas</b> — 3rd in sales but making losses! Discount policy needs urgent fix!</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — PROFITABILITY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰 Profitability Analysis":

    st.markdown("""
    <div class="page-header">
        <h1>💰 Profitability Analysis</h1>
        <p>Discount impact, profit distribution and loss analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    loss_orders   = (filtered['Profit'] < 0).sum()
    loss_pct      = loss_orders / len(filtered) * 100
    total_loss    = filtered[filtered['Profit'] < 0]['Profit'].sum()
    high_disc_pct = (filtered['Is_High_Discount'] == 1).mean() * 100
    potential     = filtered['Profit'].sum() + abs(total_loss)
    kpi_card(k1, "🔴", "Loss Orders",      f"{loss_orders:,} ({loss_pct:.1f}%)", "Need Attention",   color="#C62828")
    kpi_card(k2, "💸", "Total Loss Amount", f"${abs(total_loss):,.0f}",          "Recoverable",       color="#C62828")
    kpi_card(k3, "🎯", "High Discount %",  f"{high_disc_pct:.1f}%",             "Orders >30% off",   color="#E65100")
    kpi_card(k4, "🚀", "Profit Potential", f"${potential:,.0f}",                "If Losses Fixed")

    st.markdown("---")

    # ── Row 2: Discount vs Profit Scatter + Discount Tier Bar ─────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        sample = filtered.sample(min(2000, len(filtered)), random_state=42)
        fig, ax = plt.subplots(figsize=(6, 4))
        sc = ax.scatter(sample['Discount'], sample['Profit'],
                        c=sample['Sales'], cmap='Greens', alpha=0.5, s=15)
        plt.colorbar(sc, ax=ax, label='Sales ($)')
        ax.axhline(0, color='#C62828', linewidth=1.5, linestyle='--', label='Break-Even')
        ax.axvline(0.2, color='#FF9800', linewidth=1.5, linestyle=':', label='20% Tipping Point')
        ax.set_title('Discount vs Profit', fontsize=13, fontweight='bold', color='#1B5E20')
        ax.set_xlabel('Discount Rate')
        ax.set_ylabel('Profit ($)')
        ax.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        disc_profit = filtered.groupby('Discount_Tier')['Profit'].mean()
        order_map   = ['No Discount','Low (0–20%)','Medium (20–40%)','High (40–80%)']
        disc_profit = disc_profit.reindex([x for x in order_map if x in disc_profit.index])
        bar_colors  = ['#2E7D32' if v > 0 else '#C62828' for v in disc_profit.values]
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(range(len(disc_profit)), disc_profit.values, color=bar_colors, edgecolor='white', width=0.6)
        ax.set_xticks(range(len(disc_profit)))
        ax.set_xticklabels(disc_profit.index, rotation=15, ha='right', fontsize=9)
        ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
        ax.set_title('Avg Profit by Discount Tier', fontsize=13, fontweight='bold', color='#1B5E20')
        ax.set_ylabel('Avg Profit ($)')
        for bar, val in zip(bars, disc_profit.values):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + (2 if val > 0 else -8),
                    f'${val:.0f}', ha='center', fontsize=9, fontweight='bold',
                    color='#1B5E20' if val > 0 else '#C62828')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3: Profit Category Distribution ───────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        pc = filtered['Profit_Category'].value_counts()
        colors_map = {'High Profit':'#1B5E20','Low Profit':'#66BB6A',
                      'Break-Even':'#FFC107','Loss':'#C62828'}
        bar_cols = [colors_map.get(c,'#888') for c in pc.index]
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(pc.index, pc.values, color=bar_cols, edgecolor='white', width=0.6)
        ax.set_title('Transaction Count by Profit Category', fontsize=12, fontweight='bold', color='#1B5E20')
        ax.set_ylabel('Count')
        for bar, val in zip(bars, pc.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                    f'{val:,}\n({val/len(filtered)*100:.1f}%)',
                    ha='center', fontsize=8, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        quarterly = filtered.pivot_table(
            values='Profit', index='Order_Year',
            columns='Order_Quarter', aggfunc='sum'
        ).fillna(0)
        quarterly.columns = [f'Q{c}' for c in quarterly.columns]
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(quarterly, annot=True, fmt='.0f', cmap='RdYlGn',
                    center=0, linewidths=0.5, ax=ax,
                    annot_kws={'size': 10, 'weight': 'bold'})
        ax.set_title('Quarterly Profit Heatmap', fontsize=12, fontweight='bold', color='#1B5E20', pad=10)
        ax.set_xlabel('Quarter')
        ax.set_ylabel('Year')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 4: Shipping Mode Profit ────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    ship = filtered.groupby('Ship Mode').agg(
        Avg_Profit=('Profit','mean'),
        Total_Orders=('Order ID','count'),
        Avg_Discount=('Discount','mean')
    ).reset_index().sort_values('Avg_Profit', ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    axes[0].bar(ship['Ship Mode'], ship['Avg_Profit'],
                color=['#1B5E20','#43A047','#81C784','#C8E6C9'], edgecolor='white')
    axes[0].set_title('Avg Profit by Ship Mode', fontsize=11, fontweight='bold', color='#1B5E20')
    axes[0].set_ylabel('Avg Profit ($)')
    axes[0].tick_params(axis='x', rotation=15)

    axes[1].bar(ship['Ship Mode'], ship['Total_Orders'],
                color=['#1B5E20','#43A047','#81C784','#C8E6C9'], edgecolor='white')
    axes[1].set_title('Order Count by Ship Mode', fontsize=11, fontweight='bold', color='#1B5E20')
    axes[1].set_ylabel('Number of Orders')
    axes[1].tick_params(axis='x', rotation=15)

    axes[2].bar(ship['Ship Mode'], ship['Avg_Discount']*100,
                color=['#1B5E20','#43A047','#81C784','#C8E6C9'], edgecolor='white')
    axes[2].set_title('Avg Discount% by Ship Mode', fontsize=11, fontweight='bold', color='#1B5E20')
    axes[2].set_ylabel('Avg Discount (%)')
    axes[2].tick_params(axis='x', rotation=15)

    plt.suptitle('Shipping Mode Analysis', fontsize=13, fontweight='bold', color='#1B5E20', y=1.02)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Insights ──────────────────────────────────────────────────────────────
    st.markdown("### 💡 Key Insights")
    i1, i2 = st.columns(2)
    with i1:
        st.markdown('<div class="insight-box">🎯 <b>20% discount = tipping point!</b> Above 20% discount, average profit turns negative!</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-box">🚀 <b>Fixing loss orders</b> could increase profit by 54% — from $286K to $442K!</div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div class="warning-box">⚠️ <b>High discount (40–80%)</b> orders average -$100 profit per transaction!</div>', unsafe_allow_html=True)
        st.markdown('<div class="warning-box">⚠️ <b>Medium discount (20–40%)</b> still causes -$78 avg loss — needs immediate fix!</div>', unsafe_allow_html=True)

    # ── Summary Table ──────────────────────────────────────────────────────────
    st.markdown("### 📋 Profitability Summary Table")
    summary = filtered.groupby('Category').agg(
        Total_Sales   = ('Sales','sum'),
        Total_Profit  = ('Profit','sum'),
        Avg_Margin    = ('Profit_Margin_%','mean'),
        Loss_Orders   = ('Profit', lambda x: (x < 0).sum()),
        Avg_Discount  = ('Discount','mean')
    ).round(2).reset_index()
    summary['Total_Sales']  = summary['Total_Sales'].apply(lambda x: f"${x:,.0f}")
    summary['Total_Profit'] = summary['Total_Profit'].apply(lambda x: f"${x:,.0f}")
    summary['Avg_Margin']   = summary['Avg_Margin'].apply(lambda x: f"{x:.2f}%")
    summary['Avg_Discount'] = summary['Avg_Discount'].apply(lambda x: f"{x*100:.1f}%")
    st.dataframe(summary, use_container_width=True)
