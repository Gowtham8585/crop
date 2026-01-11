class FertilizerEngine:
    def __init__(self):
        # NPK content in common fertilizers
        self.fertilizers = {
            'Urea': {'N': 0.46, 'P': 0, 'K': 0},
            'DAP': {'N': 0.18, 'P': 0.46, 'K': 0},
            'MOP': {'N': 0, 'P': 0, 'K': 0.60},
            'SSP': {'N': 0, 'P': 0.16, 'K': 0},
            'NPK 14-35-14': {'N': 0.14, 'P': 0.35, 'K': 0.14} # Example complex
        }

    def recommend(self, crop, soil_npk):
        """
        soil_npk: {'N': val, 'P': val, 'K': val}
        Returns: List of fertilizer actions
        """
        # Standard requirements (Simplified lookup - real system has a DB)
        # These are 'Target' values for a healthy yield
        # In a real app, this comes from the 'fertilizer_data.csv' or database based on crop & soil test
        
        # Default targets if not found
        target = {'N': 120, 'P': 60, 'K': 60} 
        
        # Adjust targets based on crop (very simple rules)
        if crop in ['Rice', 'Maize', 'Sugarcane']:
            target = {'N': 120, 'P': 60, 'K': 60}
        elif crop in ['Pulses', 'Chickpea', 'Lentil']:
            target = {'N': 20, 'P': 40, 'K': 20} # Legumes need less N
        elif crop in ['Cotton']:
            target = {'N': 90, 'P': 45, 'K': 45}
            
        deficit_n = max(0, target['N'] - soil_npk['N'])
        deficit_p = max(0, target['P'] - soil_npk['P'])
        deficit_k = max(0, target['K'] - soil_npk['K'])
        
        recommendations = []
        
        # Calculate Fertilizer Quantities
        # 1. Phosphorus (P) usually comes from DAP or SSP. Let's prioritize DAP.
        dap_qty = 0
        if deficit_p > 0:
            dap_qty = deficit_p / 0.46 # DAP is 46% P roughly
            recommendations.append({
                'fertilizer': 'DAP',
                'quantity': round(dap_qty, 2),
                'unit': 'kg/acre',
                'reason': 'To supply Phosphorus'
            })
            # DAP also adds N
            supplied_n = dap_qty * 0.18
            deficit_n = max(0, deficit_n - supplied_n)
            
        # 2. Nitrogen (N) from Urea
        if deficit_n > 0:
            urea_qty = deficit_n / 0.46
            recommendations.append({
                'fertilizer': 'Urea',
                'quantity': round(urea_qty, 2),
                'unit': 'kg/acre',
                'reason': 'To supply Nitrogen'
            })
            
        # 3. Potassium (K) from MOP
        if deficit_k > 0:
            mop_qty = deficit_k / 0.60
            recommendations.append({
                'fertilizer': 'MOP (Muriate of Potash)',
                'quantity': round(mop_qty, 2),
                'unit': 'kg/acre',
                'reason': 'To supply Potassium'
            })
            
        if not recommendations:
            recommendations.append({
                'fertilizer': 'General Organic Manure',
                'quantity': 1000,
                'unit': 'kg/acre',
                'reason': 'Soil is rich in NPK, maintenance dose only.'
            })

        # Schedule
        schedule = self.get_schedule(crop)
        
        return {
            'inputs': recommendations,
            'schedule': schedule
        }
        
    def get_schedule(self, crop):
        if crop == 'Rice':
            return [
                "Basal (At planting): 50% Urea, 100% DAP, 100% MOP",
                "Tillering (20-30 days): 25% Urea",
                "Panicle Initiation (50-60 days): 25% Urea"
            ]
        elif crop in ['Maize', 'Cotton']:
            return [
                "Basal: 25% N, 100% P, 100% K",
                "Knee High Stage: 50% N",
                "Tasseling Stage: 25% N"
            ]
        else:
            return ["Basal: 50% N, 100% P, 100% K", "Top Dressing: 50% N after 30-45 days"]
