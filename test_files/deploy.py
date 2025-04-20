import requests

url = "http://localhost:5000/webhook"

payload = {
    "action": "deploy",
    "amount": 1000   # You can change this to any amount you want
}

response = requests.post(url, json=payload)

print("Status:", response.status_code)
print("Response:")
print(response.json())
