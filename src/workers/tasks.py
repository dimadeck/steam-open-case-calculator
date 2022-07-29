from celery import Celery
from config import settings_app
from core.last_item_info import LastItemInfo
from core.observer import Observer

app = Celery(__name__)
app.conf.broker_url = settings_app.CELERY_BROKER_URL
app.conf.result_backend = settings_app.CELERY_RESULT_BACKEND


@app.task(name="launch_observer")
def launch_observer(profile_id, open_case_uuid):
    lii = LastItemInfo(profile_id, open_case_uuid)
    last_asset_id = lii.get_item_info()['asset_id']
    Observer(profile_id=profile_id, last_asset_id=last_asset_id, open_case_uuid=open_case_uuid).observe()
    return True
