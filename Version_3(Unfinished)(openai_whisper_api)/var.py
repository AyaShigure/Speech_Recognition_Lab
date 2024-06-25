import os

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print(f"API Key found: {api_key}")
else:
    print("API Key not found")
