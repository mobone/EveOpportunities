
import pandas as pd
import requests


from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import sqlite3

conn = sqlite3.connect("EveFinder.db")


sell_region = '10000027' # F9-FUV

jita_item_url = 'https://janice.e-351.com/api/rpc/v1?m=Appraisal.create'
request_json = '''
                {
                  "id": 4097,
                  "method": "Appraisal.create",
                  "params": {
                    "marketId": 2,
                    "designation": 100,
                    "pricing": 200,
                    "pricePercentage": 1,
                    "input": "item_name",
                    "comment": "",
                    "compactize": true
                  }
                }
                '''
s = requests.Session()

def check_in_bad(type_id):
    if 'SKIN' in item_name:
        return True
    found_bad_id = pd.read_sql('select * from bad_ids where item_id==%s' % type_id, conn)
    if len(found_bad_id)>=1:
        print('skipping\t\t\t\t\t', item_name)
        return True

    return False

def parse_data(item):

    item_name, type_id = item

    if check_in_bad == True:
        return

    try:
        response = s.post(url=jita_item_url, data = {'~request~': request_json.replace('item_name', item_name)})

        if response.status_code != 200:
            print("error getting jita prices from janice", response.status_code)

        jita_json = response.json()
        jita_items_data = jita_json['result']['items'][0]

        sell_price = jita_items_data['sellPriceMin']
        buy_price = jita_items_data['buyPriceMax']
        sell_volume = jita_items_data['sellVolume']
        buy_volume = jita_items_data['buyVolume']
        sell_order_count = jita_items_data['sellOrderCount']
        buy_order_count = jita_items_data['buyOrderCount']
        sell_trend = jita_items_data['sellPriceMedian30Delta']
        buy_trend = jita_items_data['buyPriceMedian30Delta']

        return [type_id, item_name, sell_price, buy_price, sell_volume, buy_volume, sell_order_count, buy_order_count, sell_trend, buy_trend]
        # sellPriceMin,volume,buyPriceMax
    except Exception as e:
        #print()
        #print('e1', e)
        #print()
        pass


if __name__ == '__main__':

    item_list = []
    items_df = pd.read_csv('all_type_ids.csv')
    for key, row in items_df.iterrows():
        item_list.append((row['name'].replace('’',"'"), row['typeid']))

    with Pool(60) as p:
        results = p.map(parse_data, item_list)
    items = []
    for i in results:
        if i is not None:
            items.append(i)
    df = pd.DataFrame(items, columns = ['item_id', 'item_name', 'sell_price', 'buy_price', 'sell_volume', 'buy_volume', 'sell_order_count', 'buy_order_count', 'sell_trend', 'buy_trend'])
    print(df)
    df.to_sql('jita_prices', conn, index=False, if_exists='replace')
