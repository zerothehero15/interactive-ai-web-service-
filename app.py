from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime  # Importing datetime

app = Flask(__name__)

# API keys (replace with your actual API keys)
WEATHER_API_KEY = 'dac6cbbf1bca7bbae0e94533effeaafa'
NEWS_API_KEY = '053a3b3c60bc48afbecc8dd9c5d8c040'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/respond', methods=['POST'])
def respond():
    user_input = request.json.get('user_input', '').lower()

    if "weather" in user_input:
        location = user_input.split("weather in")[-1].strip()
        weather = get_weather(location)
        response = weather if weather else f"Sorry, I couldn't find weather for {location}."
    elif "news" in user_input:
        news = get_news()
        response = news if news else "Sorry, I couldn't fetch the latest news."
    elif "time" in user_input:
        response = get_current_time()
    else:
        response = f"AI Response to: {user_input}"

    return jsonify({'response': response})

def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    try:
        weather_data = requests.get(url).json()
        if weather_data.get('cod') != 200:
            return None
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        return f"The current weather in {location} is {description} with a temperature of {temp}°C."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

def get_current_time():
    now = datetime.now()
    return now.strftime("The current time is %H:%M:%S.")

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        news_data = requests.get(url).json()
        if news_data.get('status') != 'ok':
            return None
        articles = news_data['articles'][:5]
        news_list = [f"{article['title']} - {article['source']['name']}" for article in articles]
        return "Here are the top 5 news headlines:\n" + "\n".join(news_list)
    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"

if __name__ == '__main__':
    app.run(debug=True)
