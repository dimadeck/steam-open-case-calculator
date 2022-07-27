from time import sleep

import requests

from log import get_log_channel
from .last_item_info import LastItemInfo
from config import settings_app

_log = get_log_channel('TEST')


class Observer:
    WAITING_TIME = 1
    ADD_ITEM_URL = f'{settings_app.BACKEND_URL}/item'

    def __init__(self, profile_id, last_asset_id, open_case_uuid):
        self._profile_id = profile_id
        self._last_asset_id = last_asset_id
        self._open_case_uuid = open_case_uuid

    def observe(self):
        lii = LastItemInfo(self._profile_id, self._open_case_uuid)
        while self._is_watched():
            try:
                item_info = lii.get_item_info()
                if item_info['asset_id'] == self._last_asset_id:
                    continue
                self._add_new_item(item_info)
                self._last_asset_id = item_info['asset_id']
            except Exception as e:
                _log.error(e)
            sleep(self.WAITING_TIME)

    def _is_watched(self):
        return True

    def _add_new_item(self, item_info):
        print(item_info)
        answer = requests.post(self.ADD_ITEM_URL, json=item_info)
        data = answer.text
        print(data)
        return data
