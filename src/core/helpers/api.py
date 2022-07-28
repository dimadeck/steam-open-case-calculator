import requests

from config import settings_app


class OpenCaseAPI:
    TOKEN = settings_app.BACKEND_TOKEN
    BACKEND_URL = settings_app.BACKEND_URL

    def _make_request(self, url, method='GET', json=None):
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        answer = requests.request(method, url, json=json, headers=headers)
        return answer.json()

    def _construct_route(self, path):
        return f'{self.BACKEND_URL}/{path}'

    def get_open_case(self, open_case_uuid):
        path = f'open_case?open_case_uuid={open_case_uuid}'
        return self._make_request(self._construct_route(path))

    def add_item(self, item_info):
        path = 'item'
        return self._make_request(self._construct_route(path), method='POST', json=item_info)
