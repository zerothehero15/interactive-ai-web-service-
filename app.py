import openai
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Initialize Flask app and load environment variables
app = Flask(__name__)
load_dotenv()  # This loads the environment variables from the .env file

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

@app.route('/api/ask_openai', methods=['POST'])
def ask_openai():
    user_input = request.json.get('user_input')

    try:
        # Call OpenAI's GPT-4 model to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use GPT-4 model (or another model you want)
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({'response': response['choices'][0]['message']['content']})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
