import bs4
import requests
from bs4 import BeautifulSoup

url_tm = 'https://market.csgo.com/api/v2/prices/USD.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}


def get_html(url, params=None):
    r = requests.get(url, headers=headers, params=params)
    return r


def get_link(url):
    URL = url
    html = get_html(URL)
    if url == url_tm:
        return html.json()
    return html.text


csgotm = {kn['market_hash_name'].replace('|', ''): float(kn['price']) for kn in get_link(url_tm)['items'] if
          'Knife' in kn['market_hash_name'] and 'StatTrak' not in kn['market_hash_name']}
knife_list = []
for key, value in csgotm.items():
    knife_list.append(str(key)+' '+str(value))
    # print(f'{key} {value}')
# for i in knife_list:
#     print(i)
