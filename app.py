import openai
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure API key is set
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Make sure it's set in the .env file.")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

@app.route('/api/ask_openai', methods=['POST'])
def ask_openai():
    """
    Handles user queries and returns AI-generated responses.
    Expects a JSON payload with a 'user_input' key.
    """
    try:
        # Extract user input from JSON payload
        data = request.get_json()
        user_input = data.get('user_input')

        if not user_input:
            return jsonify({'error': 'user_input is required'}), 400

        # Call OpenAI API
        response = openai.ChatCompletion.create(
    model="GPT-4",  # Switch to this if GPT-4 isn't available
    messages=[{"role": "user", "content": user_input}]
)

        # Extract the response content
        ai_response = response['choices'][0]['message']['content']
        return jsonify({'response': ai_response})

    except openai.error.OpenAIError as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/')
def home():
    """
    Renders the homepage.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
