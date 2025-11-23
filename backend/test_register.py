import requests
import json

url = "http://localhost:5000/auth/register-doctor"
data = {
    "username": "testdoc_local",
    "email": "testdoc_local@example.com",
    "password": "password123",
    "specialization": "Cardiology"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
