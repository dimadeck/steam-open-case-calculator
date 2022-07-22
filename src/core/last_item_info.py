import requests


class LastItemInfo:
    INVENTORY_URL = 'https://steamcommunity.com/inventory/{}/730/2?l=russian&count=1'
    PRICE_URL = 'https://steamcommunity.com/market/priceoverview/?country=RU&currency=5&appid=730&market_hash_name={}'
    IMAGE_URL = 'https://steamcommunity-a.akamaihd.net/economy/image/{}'

    def __init__(self, profile_id):
        self._profile_id = profile_id

    def _get_item_info(self):
        answer = requests.get(self.INVENTORY_URL.format(self._profile_id))
        return answer.json()

    def get_item_info(self):
        raw_data = self._get_item_info()
        asset = raw_data['assets'][0]
        description = raw_data['descriptions'][0]
        item_info = {
            'profile_id': self._profile_id,
            'asset_id': asset['assetid'],
            'class_id': asset['classid'],
            'instance_id': asset['instanceid'],
            'name': description['name'],
            'item_type': None,
            'weapon': None,
            'exterior': None,
            'rarity': None,
            'rarity_color': None,
            'image_url': self.IMAGE_URL.format(description.get('icon_url'))
        }
        for tag in description['tags']:
            category = tag['category']
            if category == 'Type':
                item_info['type'] = tag['localized_tag_name']
            if category == 'Weapon':
                item_info['weapon'] = tag['localized_tag_name']
            if category == 'Rarity':
                item_info['rarity'] = tag['localized_tag_name']
                item_info['rarity_color'] = tag['color']
            if category == 'Exterior':
                item_info['exterior'] = tag['localized_tag_name']
        item_info.update(
            {
                'price': self._get_item_price(description['market_hash_name']),
                'float': '?'
            }
        )
        return item_info

    def _get_item_price(self, item_hash_name):
        try:
            answer = requests.get(self.PRICE_URL.format(item_hash_name))
            data = answer.json()
            price = float(data['lowest_price'].replace(' pуб.', '').replace(',', '.'))
            return price
        except Exception as e:
            return 0