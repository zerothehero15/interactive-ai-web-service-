from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/respond', methods=['POST'])
def respond():
    user_input = request.json.get('user_input', '')
    response = f"AI Response to: {user_input}"
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
