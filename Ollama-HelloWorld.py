import requests
import json

url = "http://localhost:11434/api/generate"
payload = {
    "model": "deepseek-r1:1.5b",
    "prompt": "describe about India?",
    "stream": False  # <--- important to get full response in one go
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
result = response.json()
print(result["response"])
