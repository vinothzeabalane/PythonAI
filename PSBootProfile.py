import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

# Load your CSV data
# df = pd.read_csv("/home/remlab/ps-bpt/PythonAI/sample.csv")
df = pd.read_csv("/home/remlab/ps-bpt/PythonAI/lm-302-04-s2-2TB-EB0-2025-04-17.csv")

# Convert part of the dataset to text (limit rows if large)
data_snippet = df.head(100).to_string(index=False)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Build your prompt
prompt = f"""
Here is a sample dataset:

{data_snippet}

Please analyze the data and tell me:
1. Get high value of each Boot Entry?
"""

# Create chat completion request
response = client.chat.completions.create(
    model="llama3-70b-8192",  # Best for structured reasoning
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Print the AI's response
print(response.choices[0].message.content)
