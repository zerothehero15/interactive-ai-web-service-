from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz
import requests
import json

app = Flask(__name__)

# API keys (replace with your actual API keys)
WEATHER_API_KEY = 'dac6cbbf1bca7bbae0e94533effeaafa'
NEWS_API_KEY = '053a3b3c60bc48afbecc8dd9c5d8c040'

# Load the timezones data from the external JSON file
def load_timezones():
    try:
        with open('timezones.json', 'r') as f:
            timezones = json.load(f)
        return timezones
    except Exception as e:
        print(f"Error loading timezones: {e}")
        return {}

# Load the timezones
timezones = load_timezones()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/respond', methods=['POST'])
def respond():
    user_input = request.json.get('user_input', '').lower()
    response = ""

    # Check for weather, news, or time requests
    if "weather" in user_input:
        location = user_input.split("weather in")[-1].strip()
        weather = get_weather(location)
        response = weather if weather else f"Sorry, I couldn't find weather for {location}."
    elif "news" in user_input:
        news = get_news()
        response = news if news else "Sorry, I couldn't fetch the latest news."
    elif "time" in user_input:
        # Extract the city from the input and fetch the correct timezone
        city = user_input.split("time in")[-1].strip()
        timezone = timezones.get(city.lower())
        
        if timezone:
            response = get_time_in_timezone(timezone)
        else:
            response = f"Sorry, I couldn't find the time zone for {city}."

    return jsonify({'response': response})

def get_time_in_timezone(timezone_str):
    try:
        # Get the time for the given timezone
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        return now.strftime(f"The current time in {timezone_str} is %H:%M:%S.")
    except pytz.UnknownTimeZoneError:
        return f"Invalid timezone: {timezone_str}"

# Function to get the current weather
def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    try:
        weather_data = requests.get(url).json()
        if weather_data.get('cod') != 200:
            return None
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        return f"The current weather in {location} is {description} with a temperature of {temp}°C."
    except Exception as e:
        return None

# Function to get the latest news
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        news_data = requests.get(url).json()
        if news_data.get('status') != 'ok':
            return None
        articles = news_data['articles'][:7]
        news_list = [f"{article['title']} - {article['source']['name']}" for article in articles]
        return "Here are the top 5 news headlines:\n" + "\n".join(news_list)
    except Exception as e:
        return None

if __name__ == '__main__':
    app.run(debug=True)
