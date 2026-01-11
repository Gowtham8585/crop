# Assisted Crop & Fertilizer Recommendation System (Tamil Nadu)

A Machine Learning-based advisor for crop and fertilizer recommendations, considering soil health, weather, and market prices.

## ⚠️ Important: Data Source Info
**Current Status**: The system is running on **Realistic Synthetic Data**.
- **Market Prices**: Derived from 2024-2025 Agmarknet averages for Tamil Nadu.
- **Weather**: Derived from IMD Historical Climate Normals (e.g., Seasonal Rainfall for Coimbatore, Thanjavur).
- **Crops**: Based on standard TNAU Agritech Portal crop requirements.

**Why?** Real-time Government APIs vary by availability and require personal API Keys.

### 🔗 Where to get REAL Data?
To connect to live Government data, obtain free API keys from:

1.  **Market Prices**: [Govt. of India Open Data (Agmarknet)](https://data.gov.in/)
    *   *Endpoint*: `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070`
    *   *Action*: Uncomment the code in `src/api_integration.py` (Lines 150+).

2.  **Weather**: [OpenWeatherMap API](https://openweathermap.org/api)
    *   *Endpoint*: `https://api.openweathermap.org/data/2.5/weather`
    *   *Action*: Pass your API Key to `WeatherService` in `src/recommender.py`.

## Prerequisities
- Python 3.8+
- Libraries: `pandas`, `numpy`, `scikit-learn`, `flask`, `requests`

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Regenerate Synthetic Data:
   ```bash
   python generate_synthetic_data.py
   ```

3. Train the Model:
   ```bash
   python src/model_training.py
   ```

## Running the Application
1. Start the Flask App:
   ```bash
   python app.py
   ```
2. Open your browser at `http://localhost:5000`.

## Architecture
- **src/model_training.py**: Trains a Random Forest model on `crop_recommendation.csv`.
- **src/recommender.py**: Hybrid engine combining ML Score (70%) + Market Profitability (30%).
- **src/fertilizer_engine.py**: Logic to calculate precise fertilizer quantities (Urea, DAP, MOP) based on soil deficit.
- **src/api_integration.py**: Mock services for Weather (OpenWeatherMap) and Market (Agmarknet).

## Features
- **Market Aware**: Recommendations are boosted if the market trend is 'UP'.
- **Scientific**: Fertilizer quantities are calculated based on atomic NPK deficits.
- **Top-Tier UI**: Modern Glassmorphism design with all 38 TN Districts.
