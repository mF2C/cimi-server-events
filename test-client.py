import json
import pprint
import sseclient
import requests

url = 'http://localhost:8000/stream?channel=demo'
response = requests.get(url, stream=True)
client = sseclient.SSEClient(response)
for event in client.events():
    pprint.pprint(json.loads(event.data))
