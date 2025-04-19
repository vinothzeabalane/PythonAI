from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import requests

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ai_answer(prompt):
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2:3b",  # or your preferred local model
            "prompt": prompt,
            "stream": False
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        return result.get("response", "No response from AI.")
    except Exception as e:
        return f"Error contacting Ollama: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question')
    file = request.files.get('file')
    prompt = ""

    if file and allowed_file(file.filename):
        filename = file.filename.lower()
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(file)
                data_snippet = df.head(200).to_string(index=False)
                prompt = f"""Here is a sample dataset from the uploaded CSV file:

{data_snippet}

Now, based on the data above, answer the following question:
{question}"""
            except Exception as e:
                return jsonify({'answer': f"Failed to read CSV: {str(e)}"})
        elif filename.endswith('.txt'):
            try:
                file_content = file.read().decode('utf-8')
                prompt = f"{file_content}\n\n{question}"
            except Exception as e:
                return jsonify({'answer': f"Failed to read TXT: {str(e)}"})
        else:
            prompt = question
    else:
        prompt = question

    if not prompt:
        return jsonify({'answer': "No question or file uploaded."})

    answer = get_ai_answer(prompt)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
