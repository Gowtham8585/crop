import React, { useState } from 'react';
import axios from 'axios';
import { districts, tamilCrops } from './constants';
import './Result.css'; // We'll create this to hold the specific result styles

const App = () => {
  const [formData, setFormData] = useState({
    district: districts[0],
    n: '',
    p: '',
    k: '',
    ph: '6.5',
    soil_type: 'Loamy'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/api/recommend', formData);
      setResult(response.data);
    } catch (err) {
      setError(err.message || 'Failed to fetch recommendations');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setResult(null);
    setFormData({
      district: districts[0],
      n: '',
      p: '',
      k: '',
      ph: '6.5',
      soil_type: 'Loamy'
    });
  }

  if (result) {
    return (
      <div className="container result-container">
        <div className="header">
          <h2>AgriAdvisor TN <span style={{ fontSize: '0.7em', opacity: 0.8 }}>| விவசாய ஆலோசகர்</span></h2>
          <button onClick={resetForm} className="back-btn">← New Search / புதிய தேடல்</button>
        </div>

        <div className="dashboard">
          {/* Left Column */}
          <div className="left-col">
            <div className="card">
              <div className="main-rec">
                <span className="badge">Top Recommendation / சிறந்த பரிந்துரை</span>
                <div className="crop-title">
                  🌱 {result.best_crop} <br />
                  <span style={{ fontSize: '0.5em', color: '#f1c40f' }}>
                    {tamilCrops[result.best_crop] || ''}
                  </span>
                </div>
                <p>{result.analysis}</p>

                <div className="score-box">
                  <div className="metric">
                    <span className="metric-val">{result.weather_context.temperature.toFixed(1)}°C</span>
                    <span className="metric-label">Avg Temp / வெப்பநிலை</span>
                  </div>
                  <div className="metric">
                    <span className="metric-val">{result.weather_context.rainfall.toFixed(0)}mm</span>
                    <span className="metric-label">Rainfall / மழை</span>
                  </div>
                  <div className="metric">
                    <span className="metric-val">₹{result.top_recommendations[0].market_price}</span>
                    <span className="metric-label">Est. Price / விலை</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="card">
              <h3>🧪 Fertilizer Plan / உர அட்டவணை</h3>
              <table className="table-custom">
                <thead>
                  <tr>
                    <th>Fertilizer / உரம்</th>
                    <th>Quantity / அளவு</th>
                    <th>Reason / காரணம்</th>
                  </tr>
                </thead>
                <tbody>
                  {result.fertilizer_plan.inputs.map((item, index) => (
                    <tr key={index}>
                      <td>{item.fertilizer}</td>
                      <td>{item.quantity} {item.unit}</td>
                      <td>{item.reason}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <h4 style={{ marginTop: '20px', borderBottom: '1px solid rgba(255,255,255,0.2)', paddingBottom: '5px' }}>
                📅 Application Schedule / இடும் முறை
              </h4>
              <div className="timeline">
                {result.fertilizer_plan.schedule.map((step, index) => (
                  <div key={index} className="timeline-item">
                    {step}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className="right-col">
            <div className="card">
              <h3>📊 Top Candidates / மற்ற பயிர்கள்</h3>
              <table className="table-custom">
                <thead>
                  <tr>
                    <th>Crop / பயிர்</th>
                    <th>Score / மதிப்பெண்</th>
                    <th>Trend / போக்கு</th>
                  </tr>
                </thead>
                <tbody>
                  {result.top_recommendations.map((crop, index) => (
                    <tr key={index}>
                      <td>
                        {crop.crop}<br />
                        <span style={{ fontSize: '0.8em', color: '#bbb' }}>
                          {tamilCrops[crop.crop] || ''}
                        </span>
                      </td>
                      <td>{crop.final_score}</td>
                      <td className={crop.price_trend === 'up' ? 'market-up' : 'market-down'}>
                        {crop.price_trend.toUpperCase()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="card">
              <h3>⚠️ Advisory Note / குறிப்பு</h3>
              <p style={{ fontSize: '0.9em', lineHeight: 1.5, opacity: 0.8 }}>
                Recommendations are based on soil health and current market trends in {result.inputs.district}.
                Please ensure soil moisture is adequate before fertilizer application.
                <br /><br />
                இப்பரிந்துரைகள் மண் வளம் மற்றும் சந்தை நிலவரத்தை அடிப்படையாகக் கொண்டவை. உரமிடுவதற்கு முன் மண்
                ஈரம் இருப்பதை உறுதி செய்யவும்.
              </p>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <h3>Soil Status / மண் நிலை</h3>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '15px' }}>
                <div>
                  <span style={{ display: 'block', fontSize: '1.2em', fontWeight: 'bold', color: '#eebb99' }}>
                    {result.inputs.soil.N}
                  </span>
                  <span style={{ fontSize: '0.8em' }}>N (தழை)</span>
                </div>
                <div>
                  <span style={{ display: 'block', fontSize: '1.2em', fontWeight: 'bold', color: '#aabbaa' }}>
                    {result.inputs.soil.P}
                  </span>
                  <span style={{ fontSize: '0.8em' }}>P (மணி)</span>
                </div>
                <div>
                  <span style={{ display: 'block', fontSize: '1.2em', fontWeight: 'bold', color: '#ccaaee' }}>
                    {result.inputs.soil.K}
                  </span>
                  <span style={{ fontSize: '0.8em' }}>K (சாம்பல்)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="container">
        <h1>🌾 AgriAdvisor TN <br /><span style={{ fontSize: '0.6em', color: '#fff' }}>விவசாய ஆலோசகர்</span></h1>
        <p style={{ textAlign: 'center', color: '#bdc3c7', marginBottom: '30px' }}>
          AI-Powered Crop & Fertilizer Recommendations<br />
          விவசாய பயிர் மற்றும் உர பரிந்துரைகள்
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>District (Tamil Nadu) / மாவட்டம்</label>
            <select name="district" value={formData.district} onChange={handleChange} required>
              {districts.map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>

          <div className="row">
            <div className="col">
              <div className="form-group">
                <label>Nitrogen (N) / தழைச்சத்து</label>
                <input type="number" name="n" placeholder="e.g. 90" value={formData.n} onChange={handleChange} required />
              </div>
            </div>
            <div className="col">
              <div className="form-group">
                <label>Phosphorus (P) / மணிச்சத்து</label>
                <input type="number" name="p" placeholder="e.g. 42" value={formData.p} onChange={handleChange} required />
              </div>
            </div>
            <div className="col">
              <div className="form-group">
                <label>Potassium (K) / சாம்பல் சத்து</label>
                <input type="number" name="k" placeholder="e.g. 43" value={formData.k} onChange={handleChange} required />
              </div>
            </div>
          </div>

          <div className="row">
            <div className="col">
              <div className="form-group">
                <label>Soil pH / மண் pH</label>
                <input type="number" step="0.1" name="ph" value={formData.ph} onChange={handleChange} />
              </div>
            </div>
            <div className="col">
              <div className="form-group">
                <label>Soil Type / மண் வகை</label>
                <select name="soil_type" value={formData.soil_type} onChange={handleChange}>
                  <option value="Loamy">Loamy (களிமண் கலந்த மணல்)</option>
                  <option value="Sandy">Sandy (மணல் பாங்கான)</option>
                  <option value="Clayey">Clayey (களிமண்)</option>
                  <option value="Red">Red (செம்மண்)</option>
                  <option value="Black">Black (கரிசல் மண்)</option>
                </select>
              </div>
            </div>
          </div>

          <button type="submit" className="btn-grad" disabled={loading}>
            {loading ? 'Analyzing...' : 'Get Recommendation / பரிந்துரை பெற'}
          </button>
          {error && <p className="error" style={{ color: 'red', textAlign: 'center', marginTop: '10px' }}>{error}</p>}
        </form>
        <div className="footer">
          Designed for Tamil Nadu Agriculture • Market Aware • Scientific Data
        </div>
      </div>
    </div>
  );
};

export default App;
