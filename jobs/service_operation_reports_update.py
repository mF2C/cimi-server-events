import json
from utils.CIMIClient import CIMIClient

def run(cimi_api_url="http://cimi:8201/api", last_run=None):
    cl = CIMIClient(cimi_api_url)
    resource_name = "service-operation-report"
    query = '$orderby=created:desc&$filter=created>"%s"&$last=100&$filter=content/state="UPDATED"' % last_run
    collection = cl.local_get(resource_name, query=query)
    events = collection[resource_name]
    if events:
        last_run = events[0]["created"]
    print(events)
    return events, last_run