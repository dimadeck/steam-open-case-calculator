from time import sleep

from log import get_log_channel
from workers.redis_pub_sub import publish
from .helpers.api import OpenCaseAPI
from .last_item_info import LastItemInfo
from config import settings_app

_log = get_log_channel('Observer')


class Observer:
    WAITING_TIME = settings_app.OBSERVER_WAITING_TIME

    def __init__(self, profile_id, last_asset_id, open_case_uuid):
        self._profile_id = profile_id
        self._last_asset_id = last_asset_id
        self._open_case_uuid = open_case_uuid

    def observe(self):
        lii = LastItemInfo(self._profile_id, self._open_case_uuid)
        _log.info(f'Observe is started for profile (open_case_uuid): {self._profile_id} ({self._open_case_uuid})')
        while self._is_watched():
            sleep(self.WAITING_TIME)
            try:
                item_info = lii.get_item_info()
                if item_info['asset_id'] == self._last_asset_id:
                    continue
                self._add_new_item(item_info)
                self._last_asset_id = item_info['asset_id']
            except Exception as e:
                _log.error(e)

        _log.info(f'Observe is finished for profile (open_case_uuid): {self._profile_id} ({self._open_case_uuid})')

    def _is_watched(self):
        return OpenCaseAPI().get_open_case(self._open_case_uuid).get('is_active')

    @staticmethod
    def _add_new_item(item_info):
        _log.info(f'Adding new item: {item_info}')
        item = OpenCaseAPI().add_item(item_info)
        _log.info(f'Sending to redis: {item}')
        publish(item)
        _log.info(f'Sent')
        return item
