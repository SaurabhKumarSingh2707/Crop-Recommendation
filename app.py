from flask import Flask, render_template, request, send_file, jsonify
import joblib
import numpy as np
import re
import warnings
from functools import wraps
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime
import os

# Suppress sklearn version warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

app = Flask(__name__)

# Load model and encoder with error handling
try:
    model_path = os.path.join('model', 'rf_model.pkl')
    encoder_path = os.path.join('model', 'label_encoder.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        raise FileNotFoundError("Model files not found")
    
    model = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)
    print("✅ Models loaded successfully!")
    print(f"Model type: {type(model)}")
    print(f"Available crops: {len(label_encoder.classes_)} classes")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    model = None
    label_encoder = None

# Input validation helper functions
def validate_required_fields(required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for field in required_fields:
                if field not in request.form or not request.form[field].strip():
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def sanitize_numeric_input(value, min_val=None, max_val=None, field_name=""):
    """Sanitize and validate numeric input"""
    try:
        # Remove any non-numeric characters except decimal point and minus
        cleaned = re.sub(r'[^0-9.-]', '', str(value))
        num_value = float(cleaned)
        
        if min_val is not None and num_value < min_val:
            raise ValueError(f"{field_name} must be at least {min_val}")
        if max_val is not None and num_value > max_val:
            raise ValueError(f"{field_name} must be at most {max_val}")
            
        return num_value
    except ValueError as e:
        raise ValueError(f"Invalid {field_name}: {str(e)}")

def sanitize_input(text, max_length=255):
    """Sanitize text input"""
    if not isinstance(text, str):
        return ""
    return text.strip()[:max_length]

@app.route('/')
def home():
    """Main page with input form"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@validate_required_fields(['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
def predict():
    """Handle crop prediction based on soil parameters"""
    # Check if models are loaded
    if model is None or label_encoder is None:
        return jsonify({'error': 'Models not loaded properly. Please check model files.'}), 500
    
    try:
        # Sanitize and validate all numeric inputs with proper ranges
        data = [
            sanitize_numeric_input(request.form['N'], 0, 200, "Nitrogen (N)"),
            sanitize_numeric_input(request.form['P'], 0, 200, "Phosphorus (P)"),
            sanitize_numeric_input(request.form['K'], 0, 200, "Potassium (K)"),
            sanitize_numeric_input(request.form['temperature'], -50, 100, "Temperature"),
            sanitize_numeric_input(request.form['humidity'], 0, 100, "Humidity"),
            sanitize_numeric_input(request.form['ph'], 0, 14, "pH"),
            sanitize_numeric_input(request.form['rainfall'], 0, 1000, "Rainfall")
        ]
        
        # Store input parameters for display
        input_params = {
            'N': f"{data[0]:.1f}",
            'P': f"{data[1]:.1f}",
            'K': f"{data[2]:.1f}",
            'temperature': f"{data[3]:.1f}",
            'humidity': f"{data[4]:.1f}",
            'ph': f"{data[5]:.2f}",
            'rainfall': f"{data[6]:.1f}"
        }
        
        # Make prediction
        prediction_array = np.array(data).reshape(1, -1)
        prediction_num = model.predict(prediction_array)[0]
        prediction_label = label_encoder.inverse_transform([prediction_num])[0]
        
        print(f"✅ Prediction successful: {prediction_label}")
        
        return render_template('result.html', crop=prediction_label, params=input_params)
        
    except ValueError as e:
        print(f"❌ Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Prediction failed. Please try again.'}), 500

@app.route('/download_report', methods=['POST'])
@validate_required_fields(['crop', 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
def download_report():
    """Generate and download PDF report"""
    try:
        # Sanitize inputs
        crop = sanitize_input(request.form['crop'], 100)
        params = {
            'Nitrogen (N)': f"{sanitize_numeric_input(request.form['N'], 0, 200, 'Nitrogen'):.1f} kg/ha",
            'Phosphorus (P)': f"{sanitize_numeric_input(request.form['P'], 0, 200, 'Phosphorus'):.1f} kg/ha",
            'Potassium (K)': f"{sanitize_numeric_input(request.form['K'], 0, 200, 'Potassium'):.1f} kg/ha",
            'Temperature': f"{sanitize_numeric_input(request.form['temperature'], -50, 100, 'Temperature'):.1f}°C",
            'Humidity': f"{sanitize_numeric_input(request.form['humidity'], 0, 100, 'Humidity'):.1f}%",
            'pH Level': f"{sanitize_numeric_input(request.form['ph'], 0, 14, 'pH'):.2f}",
            'Rainfall': f"{sanitize_numeric_input(request.form['rainfall'], 0, 1000, 'Rainfall'):.1f} mm"
        }
        
        # Create PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Header
        p.setFont('Helvetica-Bold', 20)
        p.drawString(50, height - 60, "🌾 Crop Recommendation Report")
        
        # Date & Time
        p.setFont('Helvetica', 11)
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        p.drawString(50, height - 85, f"Generated on: {current_time}")
        
        # Divider line
        p.line(50, height - 100, width - 50, height - 100)
        
        # Input Parameters Section
        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, height - 130, "📊 Input Parameters:")
        
        p.setFont('Helvetica', 12)
        y_position = height - 155
        for param_name, param_value in params.items():
            p.drawString(70, y_position, f"• {param_name}: {param_value}")
            y_position -= 20
            
        # Prediction Result Section
        y_position -= 15
        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, y_position, "🎯 Recommendation Result:")
        
        y_position -= 25
        p.setFont('Helvetica-Bold', 16)
        p.setFillColorRGB(0.2, 0.6, 0.2)  # Green color
        p.drawString(70, y_position, f"Recommended Crop: {crop.upper()}")
        
        # Footer
        p.setFillColorRGB(0, 0, 0)  # Back to black
        p.setFont('Helvetica-Oblique', 10)
        p.drawString(50, 50, "Generated by AgriTech Crop Recommendation System")
        p.drawString(50, 35, "For agricultural guidance and optimal crop selection")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        
        filename = f"crop_recommendation_{crop}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            buffer, 
            as_attachment=True, 
            download_name=filename, 
            mimetype='application/pdf'
        )
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"PDF generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate PDF report'}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': model is not None and label_encoder is not None,
        'timestamp': datetime.datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request - Invalid input data'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Print startup information
    print("🚀 Starting Crop Recommendation System...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🌐 Server will run on: http://127.0.0.1:5000")
    
    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000)