import re

import requests


def make_request(profile_id):
    cookies = {
        '_ga': 'GA1.2.678013631.1655664522',
        '__gads': 'ID=403adc41d6a7dd9e-22022dbfb7cd001a:T=1655664522:RT=1655664522:S=ALNI_MaWjhDTsjIbX4U9OraPnSj_M-LzRg',
        '_gid': 'GA1.2.1313269879.1658785336',
        '_gat_gtag_UA_118288288_1': '1',
        '__gpi': 'UID=0000077ede58a657:T=1655664522:RT=1658785335:S=ALNI_MY4Cii0c7V5JJuswduvl7hBkGbc2A',
    }

    headers = {
        'authority': 'faceitfinder.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    response = requests.get(f'https://faceitfinder.com/profile/{profile_id}', cookies=cookies, headers=headers)
    return response.text


def get_elo(profile_id):
    re_elo = r'<div style="width: 88px;" class="account-faceit-stats-single">ELO: <strong>(?P<elo>.*)<\/strong><\/div>'
    if match := re.search(re_elo, make_request(profile_id)):
        return match.group('elo')


def main():
    PROFILE_ID = 76561199125691575
    elo = get_elo(PROFILE_ID)
    print('ELO:',  elo)



if __name__ == '__main__':
    main()
