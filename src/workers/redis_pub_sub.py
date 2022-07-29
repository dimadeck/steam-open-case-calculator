import json

import redis

from config import settings_app

redis_connect = redis.StrictRedis(host=settings_app.REDIS_PUB_SUB_URL, port=6379, db=0)
subscriber = redis_connect.pubsub()
subscriber.subscribe(settings_app.REDIS_NEW_ITEM_CHANNEL)

subscriber.get_message()


def publish(data: dict):
    redis_connect.publish(settings_app.REDIS_NEW_ITEM_CHANNEL, json.dumps(data))
