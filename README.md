# 1000409-Mohammed-Saif_Elevator
🚀 Smart Elevator Predictive Maintenance Dashboard

📋 Overview

A professional, highly interactive Streamlit web application for AI-driven predictive maintenance of smart building elevators. This dashboard analyzes sensor data to detect anomalies, predict maintenance needs, and provide actionable insights.

screen shots link:https://www.canva.com/design/DAHBvAfPAsU/vC2KfeNVr3K0S4Qks_ELSA/view?utm_content=DAHBvAfPAsU&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h7709f8df95 

✨ Features

🎨 Professional UI/UX

- Modern gradient background (dark blue to purple)

- Glassmorphism design cards

- Animated sidebar with smooth transitions

- Custom CSS styling throughout

- Responsive layout for all screen sizes
APP LINK:https://1000409-mohammed-saifelevator-bdhxoggshduhz9mep8jmpc.streamlit.app/ 

📊 Interactive Visualizations

- Line Chart: Vibration over time with gradient fill and spike highlighting

- Scatter Plot: Revolutions vs Vibration with humidity color-coding

- Histogram: Humidity distribution with interactive hover

- Box Plot: Multi-sensor analysis (x1-x5) with outlier detection

- Correlation Heatmap: Vibrant plasma color scale with annotations

🔧 Advanced Filtering

- Humidity range slider

- Revolutions range slider

- Multi-select sensor columns

- Toggle for correlation heatmap

- Raw data display option

🤖 AI-Generated Insights

- Automatic detection of high-vibration events

- Correlation analysis between sensors

- Predictive maintenance alerts

- Sensor anomaly detection

- Real-time system status updates

📈 Dashboard Metrics

- Average Vibration with delta indicators

- Maximum Revolutions

- Average Humidity

- Total Records count

🚀 Bonus Features

- Animated loading spinner

- Progress bar during analysis

- Download filtered dataset (CSV)

- Dark mode (default)

- Critical alerts for threshold violations

- Data quality report

🛠️ Installation

Prerequisites

- Python 3.8 or higher

- pip package manager

Setup Instructions

- Clone or download the project files

-
Install required dependencies:

pip install -r requirements.txt

-
Generate sample dataset (optional - if not using your own data):

python generate_data.py

-
Run the application:

streamlit run app.py

- Open your browser: The dashboard will automatically open at http://localhost:8501

📁 Project Structure

smart-elevator-dashboard/
│
├── app.py                      # Main Streamlit application
├── generate_data.py            # Sample data generator
├── requirements.txt            # Python dependencies
├── elevator_sensor_data.csv    # Sensor dataset (auto-generated)
├── README.md                   # This file
└── todo.md                     # Development checklist

📊 Dataset Format

The dashboard expects a CSV file with the following columns:

 Column Type Description

 datetime datetime Timestamp of reading

 ID int Unique identifier

 revolutions float Motor revolutions (RPM)

 humidity float Humidity percentage (%)

 vibration float Vibration level (target variable)

 x1, x2, x3, x4, x5 float Additional sensor readings

Sample Data Structure

datetime,ID,revolutions,humidity,vibration,x1,x2,x3,x4,x5
2024-01-21 04:24:27,1,1649.01,65.23,70.04,52.3,78.5,31.2,92.1,38.7

🎯 Usage Guide

1. Navigation

- Use the sidebar to apply filters and configure options

- Tabs at the top to switch between different visualizations

- Expanders for raw data view and advanced analytics

2. Filtering Data

- Adjust Humidity Range slider to filter by humidity levels

- Adjust Revolutions Range slider to filter by motor speed

- Select specific Sensors to display in analysis

- Toggle Correlation Heatmap for relationship analysis

3. Interpreting Visualizations

- Line Chart: Look for spikes indicating potential issues

- Scatter Plot: Color indicates humidity, size shows vibration intensity

- Box Plot: Identify outliers across different sensors

- Heatmap: Strong correlations indicate important relationships

4. Understanding Insights

- ⚠️ Warning alerts: Require immediate attention

- ℹ️ Info alerts: Provide operational recommendations

- 🚀 Predictive alerts: Suggest maintenance scheduling

5. Exporting Data

- Enable "Show Raw Data" in sidebar

- Click "Download Filtered Data" to export CSV

🔍 Key Metrics Explained

Vibration Levels

- Normal: < 50

- Elevated: 50-75

- High: 75-85

- Critical: > 85

Humidity Impact

- Optimal: 45-65%

- Acceptable: 30-45% or 65-75%

- Concern: < 30% or > 75%

Revolutions

- Low Speed: < 1200 RPM

- Normal Speed: 1200-1800 RPM

- High Speed: > 1800 RPM

🎨 Customization

Changing Colors

Edit the custom CSS in app.py under the configure_page() function:

# Modify gradient colors
background: linear-gradient(135deg, #0a0e27 0%, #1a1f3c 50%, #2d1b4e 100%);

# Change accent colors
accent-color: #667eea;
secondary-color: #764ba2;

Adjusting Thresholds

Modify alert thresholds in the generate_insights() function:

# Change vibration threshold
if df['vibration'].max() > 80:  # Adjust this value

Adding New Visualizations

- Create a new visualization function following the pattern

- Add a new tab in the main application

- Update the sidebar if needed

🚀 Deployment

Local Deployment

streamlit run app.py

Cloud Deployment Options

- Streamlit Cloud (Recommended)

- Push code to GitHub

- Connect Streamlit Cloud to repository

- Deploy automatically

- AWS/Azure/GCP

- Use containerized deployment

- Set up load balancer

- Configure SSL certificates

📈 Performance Optimization

- Data caching enabled with @st.cache_data

- Efficient filtering with pandas operations

- Lazy loading for large datasets

- Optimized Plotly charts for smooth rendering

🔒 Security Considerations

- No sensitive data is transmitted

- All processing happens client-side

- No external API calls required

- Dataset can be filtered before export

🐛 Troubleshooting

Common Issues

-
Module not found error

pip install -r requirements.txt

- Data loading error

- Ensure elevator_sensor_data.csv exists in the same directory

- Check CSV format matches expected structure

- Visualization not displaying

- Clear browser cache

- Restart the Streamlit server

- Memory issues with large datasets

- Use filtering in sidebar to reduce data size

- Process data in chunks

📞 Support & Contributing

Getting Help

- Check the documentation above

- Review inline code comments

- Test with sample dataset first

Contributing

Feel free to enhance the dashboard with:

- Additional sensor types

- Machine learning models

- Real-time data streaming

- Mobile-responsive improvements

- Internationalization support

📄 License

This project is provided as-is for educational and commercial use.

🎯 Future Enhancements

-  Real-time data streaming integration

-  Machine learning predictive models

-  Multi-elevator comparison

-  Historical trend analysis

-  Mobile app version

-  Integration with building management systems

-  Email/SMS alert notifications

-  Custom report generation

-  User authentication and roles

-  API endpoints for external access

🏆 Credits:

Class: Artificial Intelligence: Mathematics in AI-I – Year 1

Mentor: Syed Ali Beema.S

School: Jain Vidyalaya IB world school, Madurai



Built with:

- Streamlit - Web application framework

- Plotly - Interactive visualizations

- Pandas - Data manipulation

- NumPy - Numerical computing

- Seaborn - Statistical graphics

Version: 1.0
Last Updated: 2024
Status: Production Ready ✅

🚀 Elevate Your Maintenance Strategy with AI! 🚀
