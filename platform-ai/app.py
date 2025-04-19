from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import requests
import time

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ai_answer(prompt):
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2:3b",  # or whichever model you're using in Ollama
            "prompt": prompt,
            "stream": False
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            return f"Ollama error: {response.text}"
        result = response.json()
        return result.get("response", "No response from AI.")
    except Exception as e:
        return f"Error contacting Ollama: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    start_time = time.time()

    question = request.form.get('question')
    file = request.files.get('file')
    prompt = ""

    if file and allowed_file(file.filename):
        filename = file.filename.lower()
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
                data_snippet = df.head(200).to_string(index=False)
                prompt = f"""Here is a sample dataset from the uploaded CSV file:

{data_snippet}

Now, based on the data above, answer the following question:
{question}"""
            elif filename.endswith('.txt'):
                file_content = file.read().decode('utf-8')
                prompt = f"{file_content}\n\n{question}"
        except Exception as e:
            return jsonify({'answer': f"Failed to read file: {str(e)}", 'time': 0})
    else:
        prompt = question

    if not prompt.strip():
        return jsonify({'answer': "No question or file uploaded.", 'time': 0})

    answer = get_ai_answer(prompt)
    end_time = time.time()
    duration = round(end_time - start_time, 2)

    return jsonify({'answer': answer, 'time': duration})

if __name__ == '__main__':
    app.run(debug=True)
