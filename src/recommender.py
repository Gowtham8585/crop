import pandas as pd
import numpy as np
import joblib
import os
from .api_integration import WeatherService, MarketService
from .fertilizer_engine import FertilizerEngine

class RecommenderSystem:
    def __init__(self, model_path='models/crop_recommendation_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.weather_service = WeatherService(mock=True)
        self.market_service = MarketService(mock=True)
        self.fertilizer_engine = FertilizerEngine()
        self.load_model()
        
    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print("Model loaded successfully.")
        else:
            print(f"Model not found at {self.model_path}. Please train first.")
            
    def get_recommendation(self, district, n, p, k, ph=6.5, soil_type="Loamy"):
        if not self.model:
            return {"error": "Model not loaded"}

        # 1. Get Environmental Data
        weather = self.weather_service.get_weather(district)
        if not weather:
            weather = {'temperature': 30, 'humidity': 80, 'rainfall': 200} # Fallback
            
        # 2. Prepare Input for ML Model
        # Features: N, P, K, temperature, humidity, ph, rainfall
        input_data = pd.DataFrame([[n, p, k, weather['temperature'], weather['humidity'], ph, weather['rainfall']]], 
                                  columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
        
        # 3. Predict Crop Probabilities
        probs = self.model.predict_proba(input_data)[0]
        classes = self.model.classes_
        
        # Get top 3 crops
        top_indices = np.argsort(probs)[-3:][::-1]
        top_crops = []
        
        for idx in top_indices:
            crop_name = classes[idx]
            confidence = probs[idx]
            
            # 4. Check Market Potential
            market_info = self.market_service.get_price_prediction(crop_name, district)
            
            # 5. Calculate Weighted Score
            # Score = (Confidence * 0.7) + (Profitability/100 * 0.3)
            profit_score = market_info['profitability_score']
            final_score = (confidence * 0.7) + ((profit_score / 100) * 0.3)
            
            top_crops.append({
                'crop': crop_name,
                'confidence': round(confidence * 100, 2),
                'market_price': market_info['current_price'],
                'price_trend': market_info['trend'],
                'market_score': profit_score,
                'final_score': round(final_score * 100, 2)
            })
            
        # Sort by final score
        top_crops.sort(key=lambda x: x['final_score'], reverse=True)
        best_choice = top_crops[0]
        
        # 6. Get Fertilizer Recommendation for Best Crop
        fert_rec = self.fertilizer_engine.recommend(best_choice['crop'], {'N': n, 'P': p, 'K': k})
        
        return {
            'inputs': {
                'district': district,
                'soil': {'N': n, 'P': p, 'K': k, 'pH': ph}
            },
            'weather_context': weather,
            'top_recommendations': top_crops,
            'best_crop': best_choice['crop'],
            'fertilizer_plan': fert_rec,
            'analysis': f"Based on {district}'s weather (Temp: {weather['temperature']:.1f}C) and soil health, {best_choice['crop']} is the best option with a market score of {best_choice['market_score']}/100."
        }
