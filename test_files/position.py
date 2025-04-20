import requests

url = "http://localhost:5000/webhook"

# Example payload: Start Monitoring
payload = {
  "action": "get_position"
}




# You can swap this payload to any command above

response = requests.post(url, json=payload)

print("Status:", response.status_code)
print("Response:", response.json())
