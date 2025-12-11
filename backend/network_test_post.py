import http.client, json, sys

HOST = 'localhost'
PORT = 8000
PATH = '/api/sales-agent/message'

payload = json.dumps({
    'session_id': 'net_test_session',
    'customer_id': 'net_test_customer',
    'channel': 'web',
    'message': 'hello from network test'
})

headers = {'Content-Type': 'application/json'}

print(f"Posting to http://{HOST}:{PORT}{PATH}")
try:
    print('Using client timeout 120s')
    conn = http.client.HTTPConnection(HOST, PORT, timeout=120)
    conn.request('POST', PATH, payload, headers)
    res = conn.getresponse()
    body = res.read().decode('utf-8')
    print('STATUS:', res.status, res.reason)
    print('\nHEADERS:')
    for k, v in res.getheaders():
        print(f'{k}: {v}')
    print('\nBODY:\n', body)
except Exception as e:
    print('EXCEPTION:', repr(e))
    sys.exit(2)
finally:
    try:
        conn.close()
    except:
        pass
