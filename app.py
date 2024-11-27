from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key (preferably set via environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY', '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')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/respond', methods=['POST'])
def respond():
    user_input = request.json.get('user_input', '')
    try:
        # Query OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an advanced AI assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        ai_response = response['choices'][0]['message']['content']
    except Exception as e:
        ai_response = f"Error: {str(e)}"
    
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
