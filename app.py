"""
Smart Elevator Predictive Maintenance Dashboard - PRODUCTION READY
Simplified data loading without datetime complications
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import sys

# ==============================================================================
# PAGE CONFIGURATION & CUSTOM CSS
# ==============================================================================

def configure_page():
    """Configure Streamlit page settings and custom styling"""
    st.set_page_config(
        page_title="Smart Elevator Predictive Maintenance",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for glassmorphism and modern design
    st.markdown("""
    <style>
    /* Main container gradient background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3c 50%, #2d1b4e 100%);
    }
    
    /* Glassmorphism cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Custom header styling */
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    /* Section headers */
    .section-header {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    
    /* Warning alert */
    .warning-alert {
        background: linear-gradient(135deg, rgba(255, 87, 87, 0.3), rgba(255, 159, 67, 0.3));
        border-left: 4px solid #ff5757;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    /* Info alert */
    .info-alert {
        background: linear-gradient(135deg, rgba(67, 160, 71, 0.2), rgba(56, 142, 60, 0.2));
        border-left: 4px solid #43a047;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 20px;
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    </style>
    """, unsafe_allow_html=True)


# ==============================================================================
# SIMPLIFIED DATA LOADING
# ==============================================================================

@st.cache_data
def load_data(uploaded_file=None):
    """
    Load elevator sensor data from uploaded file only.
    Simplified version without datetime parsing.
    """
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Dataset loaded successfully!")
            return df
        except Exception as e:
            st.error(f"❌ Error loading uploaded file: {str(e)}")
            return None
    else:
        return None


def generate_sample_data():
    """
    Generate sample data for testing when no dataset is available.
    """
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


# ==============================================================================
# DATA FILTERING
# ==============================================================================

def apply_filters(df, humidity_range, revolutions_range, selected_sensors):
    """
    Apply interactive filters to the dataset
    """
    filtered_df = df.copy()
    
    # Apply humidity filter
    filtered_df = filtered_df[
        (filtered_df['humidity'] >= humidity_range[0]) & 
        (filtered_df['humidity'] <= humidity_range[1])
    ]
    
    # Apply revolutions filter
    filtered_df = filtered_df[
        (filtered_df['revolutions'] >= revolutions_range[0]) & 
        (filtered_df['revolutions'] <= revolutions_range[1])
    ]
    
    return filtered_df


# ==============================================================================
# VISUALIZATION FUNCTIONS
# ==============================================================================

def create_vibration_line_chart(df):
    """
    Create interactive line chart for vibration over time
    """
    fig = go.Figure()
    
    # Add line trace with gradient fill
    fig.add_trace(go.Scatter(
        x=df['ID'],
        y=df['vibration'],
        mode='lines',
        name='Vibration',
        line=dict(
            color='#667eea',
            width=2,
            shape='spline'
        ),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    # Highlight spikes (values above 75th percentile)
    threshold = df['vibration'].quantile(0.75)
    spikes = df[df['vibration'] > threshold]
    
    fig.add_trace(go.Scatter(
        x=spikes['ID'],
        y=spikes['vibration'],
        mode='markers',
        name='High Vibration Spikes',
        marker=dict(
            color='#ff5757',
            size=8,
            symbol='diamond',
            line=dict(color='white', width=2)
        ),
        showlegend=True
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': '📈 Vibration Over Time',
            'font': {'size': 20, 'color': '#ffffff'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Reading ID',
        yaxis_title='Vibration Level',
        template='plotly_dark',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        hovermode='x unified',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_rev_vib_scatter(df):
    """
    Create scatter plot for Revolutions vs Vibration
    """
    fig = px.scatter(
        df,
        x='revolutions',
        y='vibration',
        color='humidity',
        hover_data=['x1', 'x2', 'x3'],
        color_continuous_scale='Viridis',
        title='⚙️ Revolutions vs Vibration Analysis',
        labels={
            'revolutions': 'Revolutions (RPM)',
            'vibration': 'Vibration Level',
            'humidity': 'Humidity (%)'
        }
    )
    
    fig.update_traces(
        marker=dict(
            size=8,
            line=dict(color='white', width=1),
            opacity=0.7
        )
    )
    
    fig.update_layout(
        template='plotly_dark',
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        hovermode='closest',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_humidity_histogram(df):
    """
    Create histogram for humidity distribution
    """
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['humidity'],
        nbinsx=30,
        name='Humidity',
        marker_color='#764ba2',
        opacity=0.8,
        marker_line_color='white',
        marker_line_width=1.5
    ))
    
    # Add mean line
    mean_humidity = df['humidity'].mean()
    fig.add_vline(
        x=mean_humidity,
        line_dash="dash",
        line_color="#667eea",
        line_width=2,
        annotation_text=f"Mean: {mean_humidity:.1f}%",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title={
            'text': '🌧️ Humidity Distribution',
            'font': {'size': 20, 'color': '#ffffff'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Humidity (%)',
        yaxis_title='Frequency',
        template='plotly_dark',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=False
    )
    
    return fig


def create_sensor_boxplot(df):
    """
    Create box plot for sensors x1-x5
    """
    sensor_cols = ['x1', 'x2', 'x3', 'x4', 'x5']
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
    
    fig = go.Figure()
    
    for i, col in enumerate(sensor_cols):
        fig.add_trace(go.Box(
            y=df[col],
            name=f'{col.upper()}',
            marker_color=colors[i],
            boxpoints='outliers',
            jitter=0.3,
            pointpos=-1.8,
            fillcolor=colors[i],
            line=dict(color='white', width=2)
        ))
    
    fig.update_layout(
        title={
            'text': '📊 Sensor Distribution Analysis (x1-x5)',
            'font': {'size': 20, 'color': '#ffffff'},
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title='Sensor Value',
        template='plotly_dark',
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_correlation_heatmap(df):
    """
    Create correlation heatmap
    """
    # Calculate correlation matrix
    corr_matrix = df[['revolutions', 'humidity', 'vibration', 'x1', 'x2', 'x3', 'x4', 'x5']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Plasma',
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title='Correlation'),
        hoverongaps=False
    ))
    
    fig.update_layout(
        title={
            'text': '🔍 Correlation Matrix',
            'font': {'size': 20, 'color': '#ffffff'},
            'x': 0.5,
            'xanchor': 'center'
        },
        template='plotly_dark',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


# ==============================================================================
# METRICS & INSIGHTS
# ==============================================================================

def display_dashboard_metrics(df):
    """
    Display key dashboard metrics
    """
    avg_vibration = df['vibration'].mean()
    max_revolutions = df['revolutions'].max()
    avg_humidity = df['humidity'].mean()
    total_records = len(df)
    
    vib_delta = ((avg_vibration - df['vibration'].median()) / df['vibration'].median()) * 100
    hum_delta = ((avg_humidity - 60) / 60) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Avg Vibration",
            value=f"{avg_vibration:.2f}",
            delta=f"{vib_delta:+.1f}% vs median",
            help="Average vibration level across all readings"
        )
    
    with col2:
        st.metric(
            label="⚡ Max Revolutions",
            value=f"{max_revolutions:.0f}",
            delta="Peak performance",
            help="Maximum revolutions recorded"
        )
    
    with col3:
        st.metric(
            label="🌧️ Avg Humidity",
            value=f"{avg_humidity:.1f}%",
            delta=f"{hum_delta:+.1f}% vs target",
            help="Average humidity percentage"
        )
    
    with col4:
        st.metric(
            label="📊 Total Records",
            value=f"{total_records:,}",
            delta="Data points",
            help="Total number of sensor readings"
        )


def generate_insights(df):
    """
    Generate auto-insights from the data
    """
    insights = []
    
    # Insight 1: Revolutions vs Vibration correlation
    corr_rev_vib = df['revolutions'].corr(df['vibration'])
    if corr_rev_vib > 0.5:
        insights.append({
            'icon': '⚠️',
            'title': 'High Revolutions Increase Vibration',
            'text': f'Strong correlation detected (r={corr_rev_vib:.2f}). Higher revolutions significantly increase vibration levels. Consider reducing speed during high-traffic periods.',
            'type': 'warning' if corr_rev_vib > 0.7 else 'info'
        })
    
    # Insight 2: Humidity correlation
    corr_hum_vib = df['humidity'].corr(df['vibration'])
    if abs(corr_hum_vib) > 0.3:
        correlation_type = "positive" if corr_hum_vib > 0 else "negative"
        insights.append({
            'icon': '🌧️',
            'title': 'Humidity Impact Detected',
            'text': f'Humidity shows {correlation_type} correlation (r={corr_hum_vib:.2f}) with vibration. Maintain optimal humidity levels to reduce wear.',
            'type': 'info'
        })
    
    # Insight 3: Predictive maintenance alert
    high_vib = df[df['vibration'] > df['vibration'].quantile(0.9)]
    if len(high_vib) > 0:
        insights.append({
            'icon': '🚀',
            'title': 'Predictive Maintenance Alert',
            'text': f'{len(high_vib)} high-vibration events detected. Schedule maintenance within the next 48 hours to prevent potential failure.',
            'type': 'warning' if len(high_vib) > 20 else 'info'
        })
    
    return insights


def display_insights(insights):
    """
    Display insights in styled cards
    """
    if insights:
        st.markdown('<div class="section-header">🤖 AI-Generated Insights</div>', unsafe_allow_html=True)
        
        for insight in insights:
            if insight['type'] == 'warning':
                st.markdown(f"""
                <div class="warning-alert">
                    <strong>{insight['icon']} {insight['title']}</strong><br>
                    {insight['text']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="info-alert">
                    <strong>{insight['icon']} {insight['title']}</strong><br>
                    {insight['text']}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("✅ No significant insights detected. System operating normally.")





# ==============================================================================
# MAIN APPLICATION
# ==============================================================================

def main():
    """Main application function"""
    
    # Configure page
    configure_page()
    
    # Configure sidebar first to get uploaded file
    with st.sidebar:
        st.markdown("""
        <div style='padding: 20px; text-align: center;'>
            <h1 style='color: #667eea; margin-bottom: 10px;'>⚙️</h1>
            <h2 style='color: #ffffff; margin: 0;'>Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # File upload section
        st.markdown("### 📁 Data Source")
        uploaded_file = st.file_uploader(
            "Upload Elevator Dataset (CSV)",
            type=['csv'],
            help="Upload your own elevator sensor data"
        )
    
    # Load data from uploaded file
    with st.spinner('🚀 Loading Dashboard...'):
        df = load_data(uploaded_file)
        
        # If no data available, show error
        if df is None:
            st.error("""
            ❌ **No Dataset Uploaded**
            
            Please upload your elevator sensor dataset using the file uploader in the sidebar.
            """)
            st.stop()
    
    # Configure sidebar with filters
    with st.sidebar:
        st.markdown("---")
        
        # Humidity filter
        st.markdown("### 🌧️ Humidity Filter")
        humidity_min = float(df['humidity'].min())
        humidity_max = float(df['humidity'].max())
        humidity_range = st.slider(
            "Humidity Range (%)",
            humidity_min,
            humidity_max,
            (humidity_min, humidity_max),
            step=1.0
        )
        
        # Revolutions filter
        st.markdown("### ⚡ Revolutions Filter")
        rev_min = float(df['revolutions'].min())
        rev_max = float(df['revolutions'].max())
        revolutions_range = st.slider(
            "Revolutions Range (RPM)",
            rev_min,
            rev_max,
            (rev_min, rev_max),
            step=10.0
        )
        
        # Sensor selection
        st.markdown("### 📊 Sensor Selection")
        sensor_cols = ['x1', 'x2', 'x3', 'x4', 'x5']
        selected_sensors = st.multiselect(
            "Select Sensors to Display",
            sensor_cols,
            default=sensor_cols
        )
        
        st.markdown("---")
        
        # Advanced options
        st.markdown("### 🔧 Advanced Options")
        show_heatmap = st.checkbox("Show Correlation Heatmap", value=True)
        show_raw_data = st.checkbox("Show Raw Data", value=False)
        
        st.markdown("---")
        
        # System information
        st.markdown("### ℹ️ System Info")
        st.info(f"""
        **Python Version:** {sys.version.split()[0]}
        
        **Pandas Version:** {pd.__version__}
        
        **Working Directory:** {os.getcwd()[:50]}...
        """)
        
        filters = {
            'humidity_range': humidity_range,
            'revolutions_range': revolutions_range,
            'selected_sensors': selected_sensors,
            'show_heatmap': show_heatmap,
            'show_raw_data': show_raw_data
        }
    
    # Apply filters
    filtered_df = apply_filters(
        df,
        filters['humidity_range'],
        filters['revolutions_range'],
        filters['selected_sensors']
    )
    
    # Custom header
    st.markdown("""
    <div class="header-container">
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🏢 Smart Elevator Movement Visualization</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.2rem;'>
            AI-Driven Predictive Maintenance Dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(100)
    
    # Dashboard metrics
    display_dashboard_metrics(filtered_df)
    
    # Warning alert for high vibration
    if filtered_df['vibration'].max() > 80:
        st.markdown(f"""
        <div class="warning-alert">
            <strong>⚠️ CRITICAL ALERT: High Vibration Detected</strong><br>
            Maximum vibration level of {filtered_df['vibration'].max():.2f} exceeds safety threshold. Immediate inspection required!
        </div>
        """, unsafe_allow_html=True)
    
    # Generate and display insights
    insights = generate_insights(filtered_df)
    display_insights(insights)
    
    # Main visualizations in tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Vibration", "⚙️ Revolutions", "🌧️ Humidity", "📊 Sensors", "🔍 Correlation"])
    
    with tab1:
        st.markdown('<div class="section-header">Vibration Analysis</div>', unsafe_allow_html=True)
        st.plotly_chart(create_vibration_line_chart(filtered_df), use_container_width=True)
    
    with tab2:
        st.markdown('<div class="section-header">Revolutions Analysis</div>', unsafe_allow_html=True)
        st.plotly_chart(create_rev_vib_scatter(filtered_df), use_container_width=True)
    
    with tab3:
        st.markdown('<div class="section-header">Humidity Analysis</div>', unsafe_allow_html=True)
        st.plotly_chart(create_humidity_histogram(filtered_df), use_container_width=True)
    
    with tab4:
        st.markdown('<div class="section-header">Sensor Analysis</div>', unsafe_allow_html=True)
        st.plotly_chart(create_sensor_boxplot(filtered_df), use_container_width=True)
    
    with tab5:
        if filters['show_heatmap']:
            st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
            st.plotly_chart(create_correlation_heatmap(filtered_df), use_container_width=True)
        else:
            st.info("🔍 Enable 'Show Correlation Heatmap' in sidebar to view correlations.")
    
    # Raw data expander
    with st.expander("📋 View Raw Data"):
        if filters['show_raw_data']:
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=300
            )
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=filtered_df.to_csv(index=False),
                file_name="elevator_sensor_data_filtered.csv",
                mime="text/csv"
            )
        else:
            st.info("Enable 'Show Raw Data' in sidebar to view the dataset.")
    
    # Advanced analytics expander
    with st.expander("🔬 Advanced Analytics"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Statistical Summary")
            st.write(filtered_df.describe())
        
        with col2:
            st.markdown("### Data Quality Report")
            st.write(f"- Total Records: {len(filtered_df):,}")
            st.write(f"- Missing Values: {filtered_df.isnull().sum().sum()}")
            st.write(f"- Duplicate Records: {filtered_df.duplicated().sum()}")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: rgba(255,255,255,0.5);'>
        <p>🚀 Smart Elevator Predictive Maintenance Dashboard v2.0 - Production Ready</p>
        <p style='font-size: 0.9rem;'>AI-Powered Analytics for Smart Buildings | Simplified Data Loading</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
