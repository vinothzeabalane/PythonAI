from flask import Flask, render_template, request, jsonify
import os
import json
import pandas as pd
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# Initialize Flask and Groq
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Upload config
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'csv'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# AI response from prompt
def get_ai_answer(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI model: {str(e)}"

# CSV processing
def extract_text_from_csv(file_path, user_question):
    try:
        df = pd.read_csv(file_path)
        data_snippet = df.head(100).to_string(index=False)
        prompt = f"""
Here is a sample dataset from the uploaded CSV file:

{data_snippet}

Now, based on the data above, answer the following question:
{user_question}
"""
        return prompt
    except Exception as e:
        return f"Failed to process CSV: {str(e)}"

# TXT fallback
def extract_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question')
    file = request.files.get('file')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if filename.endswith('.csv'):
            prompt = extract_text_from_csv(file_path, question)
        elif filename.endswith('.txt'):
            file_content = extract_text_from_file(file_path)
            prompt = f"{file_content}\n\n{question}"
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
