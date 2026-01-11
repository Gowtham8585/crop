from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from src.recommender import RecommenderSystem

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)
recommender = RecommenderSystem()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        district = request.form.get('district')
        n = float(request.form.get('n'))
        p = float(request.form.get('p'))
        k = float(request.form.get('k'))
        soil_type = request.form.get('soil_type')
        
        # Optional inputs
        ph = float(request.form.get('ph', 6.5))
        
        result = recommender.get_recommendation(district, n, p, k, ph, soil_type)
        
        # Tamil Translation Mapping
        tamil_crops = {
            'Rice': 'நெல் (Nel)',
            'Maize': 'மக்காச்சோளம்',
            'Cotton': 'பருத்தி',
            'Sugarcane': 'கரும்பு',
            'Groundnut': 'நிலக்கடலை',
            'Blackgram': 'உளுந்து',
            'Coconut': 'தென்னை',
            'Banana': 'வாழை',
            'Turmeric': 'மஞ்சள்',
            'Tapioca': 'மரவள்ளி',
            'Chickpea': 'கொண்டைக்கடலை',
            'Kidneybeans': 'காராமணி',
            'Pigeonpeas': 'துவரை',
            'Mothbeans': 'நரிப்பயறு',
            'Mungbean': 'பாசிப்பயறு',
            'Mango': 'மாம்பழம்',
            'Grapes': 'திராட்சை',
            'Watermelon': 'தர்பூசணி',
            'Muskmelon': 'முலாம்பழம்',
            'Apple': 'ஆப்பிள்',
            'Orange': 'ஆரஞ்சு',
            'Papaya': 'பப்பாளி',
            'Coffee': 'காபி',
            'Jute': 'சணல்',
            'Lentil': 'மைசூர் பருப்பு'
        }
        
        return render_template('result.html', result=result, tamil_crops=tamil_crops)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    data = request.json
    result = recommender.get_recommendation(
        data['district'], 
        data['n'], 
        data['p'], 
        data['k'], 
        data.get('ph', 6.5), 
        data.get('soil_type', 'Loamy')
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
