import json
from utils.CIMIClient import CIMIClient

def run(cimi_api_url="https://nuv.la/api", last_run=None):
    """ This demo reacts when a new user is added """
    cl = CIMIClient(cimi_api_url)

    # --- Specific to this job
    resource_name = "user"
    query = '$orderby=created:desc&$filter=created>"%s"&$last=100' % last_run
    # --- //

    collection = cl.local_get(resource_name, query=query)
    collection_name = resource_name + "s"

    events = collection[collection_name]
    if events:
        # This means the collection is NOT empty
        # Since these are ordered desc, the first entry is the newest one
        last_run = events[0]["created"]

    print(events)
    return events, last_run