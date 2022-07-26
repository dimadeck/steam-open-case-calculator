from core.last_item_info import LastItemInfo
from core.observer import Observer

PROFILE_ID = 76561199125691575
OPEN_CASE_UUID = '7fda08d0-dea1-45ac-9d26-57ca5fba31f3'


def get_last_item_asset_id(profile_id, open_case_uuid):
    # lii = LastItemInfo(profile_id, open_case_uuid)
    # last_asset_id = lii.get_item_info()['asset_id']
    last_asset_id = 0
    return last_asset_id


def observe(profile_id, open_case_uuid):
    last_asset_id = get_last_item_asset_id(profile_id, open_case_uuid)
    Observer(profile_id, last_asset_id, open_case_uuid).observe()


if __name__ == '__main__':
    observe(PROFILE_ID, OPEN_CASE_UUID)
