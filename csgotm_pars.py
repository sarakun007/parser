import requests
from bs4 import BeautifulSoup
import collections
import time

start_time = time.time()

URL_market = 'https://market.csgo.com/api/v2/prices/USD.json'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'accept': '*/*'}
URL_steam = 'https://steamcommunity.com/market/search/render/?query=&start=10&count=100&search_descriptions=0&sort_column=price&sort_dir=asc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Knife'


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_json(url):
    html = get_html(url)
    return html.json()


def get_text(url):
    html = get_html(url)
    return html.text


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def get_csgo_market_prices():
    csgotm = {kn['market_hash_name']: float(kn['price']) for kn in get_json(URL_market)['items'] if
              'Knife' in kn['market_hash_name']}
    return csgotm


def get_steam_prices():
    knife_steam_list, price_steam_list = [], []
    for i in range(10, 211, 100):
        url = URL_steam[:62] + str(i) + URL_steam[64:]
        soup = BeautifulSoup(get_text(url), 'html.parser')
        price_steam = soup.findAll('span', class_='\\"normal_price\\"')
        knife_steam = soup.findAll('span', class_='\\"market_listing_item_name\\"')
        price_steam_list.append([float(i.text[1:i.text.find(' ')].replace(',', '')) for i in price_steam])
        knife_steam_list.append([i.text[:i.text.find('<')] for i in knife_steam])
    ready_knife_steam_list = [j for i in knife_steam_list for j in i]
    ready_price_steam_list = [j for i in price_steam_list for j in i]
    steam_dict = dict(zip(ready_knife_steam_list, ready_price_steam_list))
    return steam_dict


def compare_prices(coefficient):
    steam_dict = get_steam_prices()
    csgotm = get_csgo_market_prices()
    tgbot_price = []
    count = 0
    for item in steam_dict.keys():
        if item in csgotm and csgotm[item] / steam_dict[item] > coefficient:
            count += 1
            tgbot_price.append(
                f'{count} {item} csgotm: {csgotm[item]}   steam: {steam_dict[item]}')
    return tgbot_price


tgbot_prices = compare_prices(0)
price_str = '\n'.join(tgbot_prices)
print(price_str)

print("--- %s seconds ---" % (time.time() - start_time))

