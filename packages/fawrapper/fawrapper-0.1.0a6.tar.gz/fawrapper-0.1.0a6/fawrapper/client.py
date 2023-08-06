from fawrapper.models import Users, Items, Jobs, Tasks, Changes
from fawrapper.requestmaker import RequestMaker
import os


class FieldawareAPIClient:
    def __init__(self, api_key=None, host="api.fieldaware.net"):
        self.api_key = api_key or os.environ['FIELDAWARE_TOKEN']
        self.host = host

        self.raw_request = RequestMaker(self.host, self.api_key)
        self.requester = RequestMaker(self.host, self.api_key)
        self._init_resources()


    def _init_resources(self):
        self.users = Users(self.raw_request)
        self.items = Items(self.raw_request)
        self.jobs = Jobs(self.raw_request)
        self.tasks = Tasks(self.raw_request)
        self.changes = Changes(self.raw_request)

