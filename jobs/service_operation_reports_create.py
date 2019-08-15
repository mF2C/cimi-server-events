import json
from utils.CIMIClient import CIMIClient


def run(cimi_api_url="http://cimi:8201/api", last_run=None):
    cl = CIMIClient(cimi_api_url)
    resource_name = "service-operation-report"
    collection_name = "serviceOperationReports"
    query = '$orderby=created:desc&$filter=created>"%s"&$last=100' % last_run
    events = []
    try:
        collection = cl.local_get(resource_name, query=query)
        events = collection[collection_name]
        if events:
            last_run = events[0]["created"]
    except KeyError:
        print("{} doesn't exist in CIMI output".format(collection_name))
    except IndexError:
        print("No resources were found in CIMI")
    except:
        print("Unknown error")
    print(events)
    return events, last_run
