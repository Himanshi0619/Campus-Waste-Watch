# Campus-Waste-Watch
A campus waste management dashboard using data analysis and machine learning to estimate overflow risk.

📌 **About the Project**

Campus Waste Watch is a data-driven waste management prototype designed to monitor bin fill levels, analyse waste patterns and estimate overflow risk before the next scheduled collection. It uses data analytics and machine learning to help identify bins that may require attention, supporting better collection planning and cleaner campus surroundings.

🎯 **Key Features**

- **Waste Monitoring**: Maintains bin-level records across different campus locations.
- **Data Analysis**: Analyses fill levels, waste types, locations and collection patterns.
- **Overflow Risk Estimation**: Uses a Random Forest classification model to demonstrate overflow-risk estimation.
- **Interactive Dashboard**: Displays key metrics, visualisations, observations and analytical insights through Streamlit.

📊 **Dataset**

The prototype uses an illustrative dataset containing:

- 420 observation records
- 10 waste bins across 10 locations
- 14 days of sample observations
- 3 observation timings per day

Note: The dataset is illustrative, not based on verified campus measurements. Model performance requires validation using actual observations.

🛠️ **Technology Stack**

- Python
- Pandas and NumPy
- Scikit-learn
- Streamlit
- Plotly
- Excel

🔄 **Working Process**

Record → Analyse → Predict → Prioritise

Bin observations are recorded, analysed to identify patterns, processed through a machine learning model for overflow-risk estimation, and presented through an interactive dashboard to support collection planning.

📁 **Project Files**

- "app.py" – Streamlit dashboard
- "model.py" – Machine learning model
- "data_analysis.py" – Data analysis functions
- "Campus_Waste_Watch.xlsx" – Dataset
- "requirements.txt" – Project dependencies
- "waste_model.pkl" – Saved trained model

🔮 **Future Scope**

- Integration of real campus waste data.
- Improved model training and validation.
- IoT-based real-time bin monitoring.
- Automated overflow alerts.
- Smarter waste collection scheduling.

🌱 **Project Goal**
To explore how data analytics and machine learning can support smarter, more efficient and sustainable waste management across campus spaces.
