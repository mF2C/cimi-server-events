import logging
import requests
from slipstream.api import Api

class CIMIClient:
    HEADERS = {
        "content-type": "application/json",
        "slipstream-authn-info": "internal ADMIN"
    }
    def __init__(self, cimi_api_url="https://nuv.la/api"):
        self.url = cimi_api_url
        self.api = Api(endpoint='https://{}'.format(cimi_api_url), insecure=True, reauthenticate=True)

    @staticmethod
    def logger(log_level=logging.INFO, log_file="/var/log/cimiclient.log"):
        logging.basicConfig(level=log_level)
        root_logger = logging.getLogger()

        file_handler = logging.FileHandler(log_file)
        root_logger.addHandler(file_handler)

        return root_logger

    def authenticate(self, username, password):
        self.api.login_internal(username, password)

    def local_get(self, resource_name, query=None):
        full_url = "{}/{}".format(self.url, resource_name)
        if query:
            full_url += "?{}".format(query)

        return requests.get(full_url, headers=self.HEADERS).json()