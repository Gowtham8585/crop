import requests
import random

class WeatherService:
    def __init__(self, api_key=None, mock=True):
        self.api_key = api_key
        self.mock = mock
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        """
        Returns: {
            'temperature': float (Celsius),
            'humidity': float (%),
            'rainfall': float (mm)
        }
        """
        if self.mock:
            # Indian Meteorological Department (IMD) Historical Averages for TN Districts (Approx)
            tn_weather_normals = {
                'Ariyalur':     {'temp': 32, 'hum': 60, 'rain': 900},
                'Chengalpattu': {'temp': 30, 'hum': 75, 'rain': 1200},
                'Chennai':      {'temp': 32, 'hum': 80, 'rain': 1400},
                'Coimbatore':   {'temp': 29, 'hum': 60, 'rain': 600},
                'Cuddalore':    {'temp': 31, 'hum': 75, 'rain': 1300},
                'Dharmapuri':   {'temp': 28, 'hum': 55, 'rain': 850},
                'Dindigul':     {'temp': 30, 'hum': 55, 'rain': 800},
                'Erode':        {'temp': 33, 'hum': 50, 'rain': 700},
                'Kallakurichi': {'temp': 32, 'hum': 60, 'rain': 950},
                'Kancheepuram': {'temp': 32, 'hum': 70, 'rain': 1100},
                'Karur':        {'temp': 34, 'hum': 50, 'rain': 650},
                'Krishnagiri':  {'temp': 28, 'hum': 60, 'rain': 850},
                'Madurai':      {'temp': 34, 'hum': 50, 'rain': 850},
                'Mayiladuthurai':{'temp': 31, 'hum': 75, 'rain': 1200},
                'Nagapattinam': {'temp': 31, 'hum': 80, 'rain': 1300},
                'Namakkal':     {'temp': 33, 'hum': 55, 'rain': 750},
                'Nilgiris':     {'temp': 18, 'hum': 80, 'rain': 1800}, # Hill station
                'Perambalur':   {'temp': 33, 'hum': 55, 'rain': 900},
                'Pudukkottai':  {'temp': 32, 'hum': 60, 'rain': 900},
                'Ramanathapuram':{'temp': 33, 'hum': 65, 'rain': 800}, # Coastal but dry
                'Ranipet':      {'temp': 33, 'hum': 60, 'rain': 950},
                'Salem':        {'temp': 32, 'hum': 55, 'rain': 900},
                'Sivaganga':    {'temp': 33, 'hum': 55, 'rain': 850},
                'Tenkasi':      {'temp': 30, 'hum': 65, 'rain': 1000},
                'Thanjavur':    {'temp': 31, 'hum': 75, 'rain': 1100},
                'Theni':        {'temp': 30, 'hum': 65, 'rain': 900},
                'Thoothukudi':  {'temp': 31, 'hum': 70, 'rain': 600},
                'Tiruchirappalli':{'temp': 34, 'hum': 50, 'rain': 800},
                'Tirunelveli':  {'temp': 32, 'hum': 65, 'rain': 800},
                'Tirupattur':   {'temp': 30, 'hum': 60, 'rain': 900},
                'Tiruppur':     {'temp': 31, 'hum': 50, 'rain': 600},
                'Tiruvallur':   {'temp': 32, 'hum': 75, 'rain': 1100},
                'Tiruvannamalai':{'temp': 31, 'hum': 60, 'rain': 1000},
                'Tiruvarur':    {'temp': 31, 'hum': 75, 'rain': 1200},
                'Vellore':      {'temp': 33, 'hum': 60, 'rain': 900},
                'Viluppuram':   {'temp': 32, 'hum': 65, 'rain': 1000},
                'Virudhunagar': {'temp': 34, 'hum': 50, 'rain': 750},
            }
            
            defaults = tn_weather_normals.get(city, {'temp': 30, 'hum': 70, 'rain': 900})
            
            # Add slight daily variation
            return {
                'temperature': defaults['temp'] + random.uniform(-2, 2),
                'humidity':    defaults['hum'] + random.uniform(-5, 5),
                'rainfall':    defaults['rain'] + random.uniform(-50, 50) # Seasonal expectation
            }
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                hum = data['main']['humidity']
                
                # IMPORTANT: 'Current Weather' API does NOT give annual rainfall which crops need.
                # We often need a "Climate Forecast" or Historical Data.
                # For this system to be accurate with real APIs, we would need the 'Climate Forecast' endpoint.
                # Fallback to historical normal if specific rain data is missing.
                rain = data.get('rain', {}).get('1h', 0) * 24 * 30 * 4 # Rough projection if raining now
                if rain == 0:
                     # Fallback to a district average if it's a known TN district
                     tn_weather_normals = {'Coimbatore': 600, 'Thanjavur': 1100, 'Chennai': 1400}
                     rain = tn_weather_normals.get(city, 900)
                
                return {
                    'temperature': temp,
                    'humidity': hum,
                    'rainfall': rain
                }
            else:
                print(f"Error fetching weather: {data.get('message')}")
                return None
        except Exception as e:
            print(f"Exception in WeatherService: {e}")
            return None

class MarketService:
    def __init__(self, api_key=None, mock=True):
        self.api_key = api_key
        self.mock = mock
        self.prices_df = None
        # Try to load local realistic database
        try:
            import pandas as pd
            import os
            if os.path.exists('market_prices.csv'):
                self.prices_df = pd.read_csv('market_prices.csv')
        except Exception as e:
            print(f"Could not load market CSV: {e}")

    def get_price_prediction(self, crop, district):
        """
        Returns predicted profitability score (0-100) and price.
        """
        price = 2000 # Default fallback
        
        if self.mock and self.prices_df is not None:
            # Lookup specific district-crop price
            subset = self.prices_df[
                (self.prices_df['District'] == district) & 
                (self.prices_df['Commodity'] == crop)
            ]
            
            if not subset.empty:
                price = int(subset.iloc[0]['Modal_Price'])
            else:
                # Fallback to state average for that crop
                crop_subset = self.prices_df[self.prices_df['Commodity'] == crop]
                if not crop_subset.empty:
                    price = int(crop_subset['Modal_Price'].mean())

        # Determine Mock Trend based on price
        # High price = Up-trend (simplified logic for demo)
        if price > 5000:
            trend = 'up'
            profitability_score = 90
        elif price > 2500:
            trend = 'stable'
            profitability_score = 70
        else:
            trend = 'down'
            profitability_score = 40
            
        # ------------------------------------------------------------------
        # REAL LIVE DATA IMPLEMENTATION (Requires API Key)
        # ------------------------------------------------------------------
        # To get real data, register at: https://agmarknet.gov.in/
        # Endpoint: https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070
        #
        # try:
        #     url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        #     params = {
        #         'api-key': self.api_key or 'YOUR_GOV_DATA_API_KEY',
        #         'format': 'json',
        #         'filters[district]': district,
        #         'filters[commodity]': crop
        #     }
        #     response = requests.get(url, params=params)
        #     data = response.json()
        #     if data['records']:
        #         real_price = int(data['records'][0]['modal_price'])
        #         price = real_price
        # except Exception as e:
        #     print(f"Real API failed: {e}")
        # ------------------------------------------------------------------
            
        return {
            'current_price': price,
            'trend': trend,
            'profitability_score': profitability_score
        }
