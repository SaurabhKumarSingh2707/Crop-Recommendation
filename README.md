# 🌾 Crop Recommendation System

A modern, AI-powered web application that recommends optimal crops based on soil conditions and environmental factors.

## ✨ Features

- **Smart Crop Prediction**: Uses Random Forest machine learning algorithm
- **User-Friendly Interface**: Clean, responsive web design
- **Real-time Validation**: Input validation with helpful feedback
- **PDF Reports**: Generate detailed recommendation reports
- **Error Handling**: Robust error handling and user feedback
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this project**
   ```bash
   cd "Crop Recommendation Clean"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to: `http://127.0.0.1:5000`

## 📊 Usage

1. **Enter soil parameters:**
   - Nitrogen content (0-200 kg/ha)
   - Phosphorus content (0-200 kg/ha)
   - Potassium content (0-200 kg/ha)
   - Temperature (-50 to 100°C)
   - Humidity (0-100%)
   - pH level (0-14)
   - Rainfall (0-1000mm)

2. **Get instant prediction:**
   - AI analyzes your soil conditions
   - Receives optimal crop recommendation
   - View detailed parameter analysis

3. **Download PDF report:**
   - Comprehensive recommendation report
   - All input parameters included
   - Professional formatting

## 🏗️ Project Structure

```
Crop Recommendation Clean/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── model/
│   ├── rf_model.pkl      # Trained Random Forest model
│   └── label_encoder.pkl # Label encoder for crop names
├── templates/
│   ├── index.html        # Main input form
│   └── result.html       # Results display page
└── static/
    └── style.css         # CSS styles
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Machine Learning**: scikit-learn, Random Forest Classifier
- **PDF Generation**: ReportLab
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: NumPy, Joblib

## 🔧 API Endpoints

- `GET /` - Main application page
- `POST /predict` - Crop prediction endpoint
- `POST /download_report` - PDF report generation
- `GET /health` - Health check endpoint

## 🎯 Supported Crops

The model can predict the following crops:
- Apple, Banana, Blackgram, Chickpea, Coconut
- Coffee, Cotton, Grapes, Jute, Kidneybeans
- Lentil, Maize, Mango, Mothbeans, Mungbean
- Muskmelon, Orange, Papaya, Pigeonpeas, Pomegranate
- Rice, Watermelon, and more...

## 🔍 Model Information

- **Algorithm**: Random Forest Classifier
- **Features**: 7 input parameters (N, P, K, Temperature, Humidity, pH, Rainfall)
- **Accuracy**: High accuracy on agricultural datasets
- **Training**: Trained on comprehensive crop-soil datasets

## 🚨 Error Handling

The application includes comprehensive error handling:
- Input validation with range checking
- Model loading verification
- Graceful error messages
- Fallback responses for edge cases

## 🌟 Key Improvements

This clean version includes:
- ✅ Fixed form submission routing (`/predict` endpoint)
- ✅ Enhanced error handling and validation
- ✅ Improved user interface and experience
- ✅ Better code organization and documentation
- ✅ Comprehensive input validation
- ✅ Professional PDF report generation
- ✅ Responsive design for all devices
- ✅ Loading states and user feedback

## 📝 Development Notes

- Models trained with scikit-learn 1.5.1, compatible with newer versions
- Version warnings are suppressed for better user experience
- All file paths use os.path.join for cross-platform compatibility
- Input sanitization prevents XSS and injection attacks

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Farming! 🌱**