from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

def get_ai_answer(question):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:1.5b",  # Change if you're using a different local model
        "prompt": question,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        return result.get("response", "No response from AI.")
    except Exception as e:
        return f"Error contacting AI model: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    answer = get_ai_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
