from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
import time
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ai_answer(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Change to your required model
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI model: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    start_time = time.time()  # Start measuring time

    question = request.form.get('question')
    file = request.files.get('file')
    prompt = ""

    if file and allowed_file(file.filename):
        filename = file.filename.lower()
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
                data_snippet = df.head(100).to_string(index=False)
                prompt = f"""Here is a sample dataset from the uploaded CSV file:

{data_snippet}

Now, based on the data above, answer the following question:
{question}"""
            elif filename.endswith('.txt'):
                file_content = file.read().decode('utf-8')
                prompt = f"{file_content}\n\n{question}"
        except Exception as e:
            return jsonify({'answer': f"Failed to read file: {str(e)}", 'time': "0:00:000"})
    else:
        prompt = question

    if not prompt.strip():
        return jsonify({'answer': "No question or file uploaded.", 'time': "0:00:000"})

    # Get the AI answer
    answer = get_ai_answer(prompt)

    # End measuring time
    end_time = time.time()
    duration_seconds = end_time - start_time
    duration = timedelta(seconds=duration_seconds)

    # Extract minutes, seconds, and milliseconds
    minutes = duration.seconds // 60
    seconds = duration.seconds % 60
    milliseconds = duration.microseconds // 1000  # Convert microseconds to milliseconds

    # Format time as min:sec:ms
    formatted_duration = f"{minutes}:{seconds:02}:{milliseconds:03}"

    return jsonify({'answer': answer, 'time': formatted_duration})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6070, debug=True)
