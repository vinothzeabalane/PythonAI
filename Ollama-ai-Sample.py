import requests

# Test Ollama API connection to the base URL
response = requests.get("http://10.74.134.8:11434/")  # Testing the base URL

# Check if the connection is successful
if response.status_code == 200:
    print("Connection Successful!")
    print("Response:", response.text)  # Display the response text
else:
    print(f"Error: {response.status_code} - {response.text}")
