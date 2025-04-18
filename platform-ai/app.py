from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf'}

# Make sure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

def extract_text_from_file(file_path):
    """Extract text from the file. This is a simplified function for .txt files."""
    with open(file_path, 'r') as file:
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

        # Process the file, here it's assumed to be a .txt file for simplicity
        if filename.endswith('.txt'):
            file_text = extract_text_from_file(file_path)
            question = file_text  # You can process the file contents further if needed

    if not question:
        return jsonify({'answer': "No question or file uploaded."})

    # Get AI answer using the question or file contents
    answer = get_ai_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
