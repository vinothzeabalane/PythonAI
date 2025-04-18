import openai
import os

from dotenv import load_dotenv

openai.api_key = os.environ.get("OPENAI_API_KEY")

load_dotenv()

try:
    models = openai.models.list()
    print("✅ Success:", models)
except Exception as e:
    print("❌ Error:", e)

from openai import OpenAI
client = OpenAI()

client.models.list()





