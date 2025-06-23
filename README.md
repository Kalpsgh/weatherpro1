# 🌤️ Real-Time Weather Pro App

A visually enhanced and feature-rich real-time weather dashboard built with **Streamlit**. This app fetches live weather data, UV index, air quality, and 5-day forecasts using the **OpenWeatherMap API**, with optional automatic location detection.

---

## 🚀 Features

- 📍 **City-based or Auto-detected Weather**
- 🌡️ **Real-Time Temperature, Wind Speed, and Humidity**
- ⚠️ **Extreme Weather Alerts**
- 🌞 **UV Index Indicator with Safety Advice**
- 🪱 **Air Quality Index (AQI) Monitoring**
- 👕 **Clothing Suggestions Based on Conditions**
- 📊 **Interactive 5-Day Temperature Forecast Chart**
- 🗓️ **Expandable Daily Forecast Summary**
- 🌓 **Light / Dark Theme Toggle**

---

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/68422bca-e06c-4f31-bb1b-1dbbe69b9304)
![image](https://github.com/user-attachments/assets/9e8d3aa1-aaec-4961-a6e8-3faecb91a2a7)
![image](https://github.com/user-attachments/assets/0583f342-5500-4205-baa1-f3b8e2dd40cc)
![image](https://github.com/user-attachments/assets/5e64e51c-0362-4533-8bfe-ed1bb711ead9)



---

## 🔧 Setup Instructions

### 1. Clone the Repository

git clone https://github.com/your-username/weather-pro-app.git
cd weather-pro-app

2. Create a Virtual Environment (Optional)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Add Your API Key

Replace the API key placeholder inside main.py:
WEATHER_API_KEY = "your_openweathermap_api_key"

5. Run the App

streamlit run main.py
🌐 APIs Used
OpenWeatherMap – Current Weather, Forecast, UV Index, Air Pollution

ip-api – Auto-location via IP address

📁 File Structure
bash
Copy
Edit
weather-pro-app/
│
├── main.py                # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
✅ To-Do / Future Improvements
Add animated weather icons using Lottie

Dynamic backgrounds based on weather

Add rain probability and sunrise/sunset times

Save recent search history or favorites

Add multilingual support

🙋‍♂️ Author
Kalpesh Patil
https://github.com/Kalpsgh

