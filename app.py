"""
Smart Elevator Predictive Maintenance Dashboard - PRODUCTION READY v4.0
Directly loads 'Elevator predictive-maintenance-dataset.csv' from the local directory.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import sys

# ==============================================================================
# PAGE CONFIGURATION & CUSTOM CSS
# ==============================================================================

def configure_page():
    st.set_page_config(
        page_title="Smart Elevator Predictive Maintenance",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3c 50%, #2d1b4e 100%); }
    .metric-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
    .header-container { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3); }
    .section-header { color: #ffffff; font-size: 1.8rem; font-weight: 600; margin: 30px 0 20px 0; padding-bottom: 10px; border-bottom: 3px solid #667eea; }
    .warning-alert { background: linear-gradient(135deg, rgba(255, 87, 87, 0.3), rgba(255, 159, 67, 0.3)); border-left: 4px solid #ff5757; padding: 20px; border-radius: 10px; margin: 15px 0; }
    .info-alert { background: linear-gradient(135deg, rgba(67, 160, 71, 0.2), rgba(56, 142, 60, 0.2)); border-left: 4px solid #43a047; padding: 15px; border-radius: 10px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# DATA LOADING
# ==============================================================================

@st.cache_data
def load_data():
    file_path = "Elevator predictive-maintenance-dataset.csv"
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            st.error(f"❌ Error reading '{file_path}': {str(e)}")
            return None
    else:
        st.warning(f"⚠️ Could not find '{file_path}'. Using sample data.")
        return None

def generate_sample_data():
    np.random.seed(42)
    data = {
        'ID': range(1, 1001),
        'revolutions': np.random.normal(1500, 200, 1000),
        'humidity': np.random.normal(60, 10, 1000),
        'vibration': np.random.normal(50, 15, 1000),
        'x1': np.random.normal(25, 5, 1000),
        'x2': np.random.normal(30, 8, 1000),
        'x3': np.random.normal(35, 10, 1000),
        'x4': np.random.normal(40, 12, 1000),
        'x5': np.random.normal(45, 15, 1000)
    }
    return pd.DataFrame(data)

def apply_filters(df, humidity_range, revolutions_range):
    filtered_df = df[
        (df['humidity'] >= humidity_range[0]) &
        (df['humidity'] <= humidity_range[1]) &
        (df['revolutions'] >= revolutions_range[0]) &
        (df['revolutions'] <= revolutions_range[1])
    ]
    return filtered_df

# ==============================================================================
# FEATURE CALCULATIONS
# ==============================================================================

def calculate_health_score(df):
    base_score = 100
    avg_vib = df['vibration'].mean()

    if avg_vib > 65:
        base_score -= 15
    elif avg_vib > 55:
        base_score -= 5

    high_revs = len(df[df['revolutions'] > 180])
    penalty = min((high_revs / max(len(df), 1)) * 100, 20)
    base_score -= penalty

    return max(0, min(100, round(base_score, 1)))

def calculate_maintenance_days(health_score):
    if health_score >= 90: return 180
    elif health_score >= 75: return 90
    elif health_score >= 60: return 30
    else: return 7

# ==============================================================================
# VISUALIZATIONS
# ==============================================================================

def create_3d_scatter(df):
    fig = px.scatter_3d(
        df,
        x='revolutions',
        y='vibration',
        z='humidity',
        color='vibration',
        color_continuous_scale='Plasma',
        title='🌐 3D Multi-Variate Sensor Analysis',
        opacity=0.7
    )
    fig.update_layout(template='plotly_dark', height=600)
    return fig

def create_vibration_line_chart(df):
    df_sorted = df.sort_values(by='ID')
    fig = px.line(df_sorted, x='ID', y='vibration', title='📈 Vibration Over Time')
    fig.update_layout(template='plotly_dark', height=400)
    return fig

def create_correlation_heatmap(df):
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Plasma'
    ))
    fig.update_layout(title='🔍 Correlation Matrix', template='plotly_dark', height=500)
    return fig

# NEW VISUALIZATIONS

def create_humidity_distribution(df):
    fig = px.histogram(df, x='humidity', nbins=30, title='💧 Humidity Distribution')
    fig.update_layout(template='plotly_dark', height=400)
    return fig

def create_revolutions_distribution(df):
    fig = px.histogram(df, x='revolutions', nbins=30, title='⚙️ Revolutions Distribution')
    fig.update_layout(template='plotly_dark', height=400)
    return fig

def create_revolution_vs_vibration(df):
    fig = px.scatter(
        df,
        x='revolutions',
        y='vibration',
        trendline="ols",
        title='📊 Revolutions vs Vibration'
    )
    fig.update_layout(template='plotly_dark', height=500)
    return fig

# ==============================================================================
# MAIN APP
# ==============================================================================

def main():
    configure_page()

    df = load_data()
    if df is None:
        df = generate_sample_data()

    health_score = calculate_health_score(df)
    maint_days = calculate_maintenance_days(health_score)

    with st.sidebar:
        humidity_range = st.slider(
            "Humidity Range (%)",
            float(df['humidity'].min()),
            float(df['humidity'].max()),
            (float(df['humidity'].min()), float(df['humidity'].max()))
        )

        revolutions_range = st.slider(
            "Revolutions Range (RPM)",
            float(df['revolutions'].min()),
            float(df['revolutions'].max()),
            (float(df['revolutions'].min()), float(df['revolutions'].max()))
        )

    filtered_df = apply_filters(df, humidity_range, revolutions_range)

    st.title("🏢 Smart Elevator Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("System Health", f"{health_score}%")
    col2.metric("Avg Vibration", f"{filtered_df['vibration'].mean():.2f}")
    col3.metric("Max Revolutions", f"{filtered_df['revolutions'].max():.2f}")
    col4.metric("Avg Humidity", f"{filtered_df['humidity'].mean():.1f}%")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🌐 3D View", "📈 Time Series", "🔍 Correlations", "📊 Distributions & Analysis"]
    )

    with tab1:
        st.plotly_chart(create_3d_scatter(filtered_df), use_container_width=True)

    with tab2:
        st.plotly_chart(create_vibration_line_chart(filtered_df), use_container_width=True)

    with tab3:
        st.plotly_chart(create_correlation_heatmap(filtered_df), use_container_width=True)

    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_humidity_distribution(filtered_df), use_container_width=True)
            st.plotly_chart(create_revolutions_distribution(filtered_df), use_container_width=True)
        with col2:
            st.plotly_chart(create_revolution_vs_vibration(filtered_df), use_container_width=True)

    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
