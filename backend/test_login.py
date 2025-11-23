import requests
import json

url = "http://localhost:5000/auth/login"
data = {
    "username": "testdoc_local",
    "password": "password123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
