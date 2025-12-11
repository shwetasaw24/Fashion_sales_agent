from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)

payload = {
    "session_id": "debug_session",
    "customer_id": "debug_customer",
    "channel": "web",
    "message": "hello from debug client"
}

print("Sending request to /api/sales-agent/message")
resp = client.post('/api/sales-agent/message', json=payload)
print('STATUS:', resp.status_code)
try:
    print('RESPONSE JSON:', json.dumps(resp.json(), indent=2))
except Exception:
    print('RESPONSE TEXT:', resp.text)

# Print server logs in response headers if available
print('HEADERS:')
for k,v in resp.headers.items():
    print(k+':', v)
