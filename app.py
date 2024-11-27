from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Load API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/respond', methods=['POST'])
def respond():
    user_input = request.json.get('user_input', '')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with your preferred model
            messages=[{"role": "user", "content": user_input}]
        )
        ai_response = response['choices'][0]['message']['content']
    except Exception as e:
        ai_response = f"Error: {str(e)}"
    
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)

