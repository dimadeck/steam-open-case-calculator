import re

import requests


class SteamInfo:
    URL = 'https://steamcommunity.com/profiles/{}'
    re_username = r'<span class="actual_persona_name">(?P<username>.*)<\/span>'
    re_avatar_block = r'<div class="playerAvatarAutoSizeInner">(.*\n*)*?<\/div>'
    re_avatar_image = r'<img src="(.*.jpg)">'

    def __init__(self, profile_id):
        self._profile_id = profile_id

    def get_info(self):
        answer = requests.get(self.URL.format(self._profile_id))
        html = answer.text
        data = {
            'profile_id': self._profile_id,
            'username': None,
            'image_url': None
        }
        if found := re.search(self.re_username, html):
            data['username'] = found.group('username')
        if found := re.search(self.re_avatar_block, html):
            if image_url := re.search(self.re_avatar_image, found.group()):
                data['image_url'] = image_url.group(1)
        return data
