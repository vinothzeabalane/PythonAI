import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Get list of available models
models = client.models.list()

# Print model IDs
for model in models.data:
    print(model.id)
