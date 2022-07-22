from core.last_item_info import LastItemInfo
from core.observer import Observer

PROFILE_ID = 76561199125691575


def observe(profile_id):
    lii = LastItemInfo(profile_id)
    #last_asset_id = lii.get_item_info()['asset_id']
    last_asset_id = 0
    Observer(profile_id, last_asset_id).observe()


if __name__ == '__main__':
    observe(PROFILE_ID)
