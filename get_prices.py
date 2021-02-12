
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

'''
Example output
{
  "id": 4096,
  "result": {
    "id": 674902,
    "created": "2020-11-25T22:49:38.7129305Z",
    "expires": "2020-12-25T22:49:38.7129305Z",
    "code": "QIDzas",
    "designation": 100,
    "pricing": 200,
    "pricePercentage": 1,
    "comment": "",
    "isCompactized": true,
    "input": "praetor II",
    "failures": "",
    "pricerMarket_id": 2,
    "pricerMarket_name": "Jita",
    "totalVolume": 25,
    "totalBuyPrice": 1620000,
    "totalSplitPrice": 1751000,
    "totalSellPrice": 1882000,
    "items": [
      {
        "id": 3619956,
        "itemType_eid": 2195,
        "amount": 1,
        "buyPriceMin": 1999,
        "buyPriceAverage": 920124.3059839605,
        "buyPriceMedian": 1410000,
        "buyPriceStdDev": 708608.6157313526,
        "buyPriceMax": 1620000,
        "buyPriceAverage5": 1850000,
        "buyPriceAverage30": 1889000,
        "buyPriceMedian5": 1618800,
        "buyPriceMedian30": 1664900,
        "buyOrderCount": 22,
        "buyVolume": 3242,
        "splitPriceMedian5": 1749000,
        "splitPriceMedian30": 1751500,
        "sellPriceMin": 1882000,
        "sellPriceAverage": 3104992.081683684,
        "sellPriceMedian": 2475000,
        "sellPriceStdDev": 1649907.6748393432,
        "sellPriceMax": 22860000,
        "sellPriceAverage5": 1850000,
        "sellPriceAverage30": 1889000,
        "sellPriceMedian5": 1618800,
        "sellPriceMedian30": 1889000,
        "sellOrderCount": 44,
        "sellVolume": 4799,
        "volume": 25,
        "volumeTotal": 25,
        "splitPrice": 1751000,
        "splitPriceAverage5": 1850000,
        "splitPriceAverage30": 1889000,
        "buyPriceTotal": 1620000,
        "splitPriceTotal": 1751000,
        "sellPriceTotal": 1882000,
        "buyPriceAverage30Delta": -0.14240338803599784,
        "splitPriceAverage30Delta": -0.07305452620434094,
        "sellPriceAverage30Delta": -0.0037056643726839367,
        "buyPriceMedian30Delta": -0.02696858670190405,
        "splitPriceMedian30Delta": -0.00028546959748787515,
        "sellPriceMedian30Delta": -0.0037056643726839367,
        "itemType": {
          "eid": 2195,
          "name": "Praetor II",
          "description": "Heavy Attack Drone",
          "volume": 25,
          "packagedVolume": 25
        }
      }
    ]
  }
}
'''
s = requests.Session()

def check_in_bad(type_id, item_name):
    if 'SKIN' in item_name:
        return True
    if 'Blueprint' in item_name:
        return True
    #found_bad_id = pd.read_sql('select * from bad_ids where item_id==%s' % type_id, conn)
    #if len(found_bad_id)>=1:
    #    print('skipping\t\t\t\t\t', item_name)
    #    return True

    return False

def parse_data(item):

    item_name, type_id = item

    if check_in_bad(type_id, item_name) == True:
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
        print(item_name, sell_price)

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

    with Pool(30) as p:
        results = p.map(parse_data, item_list)
    items = []
    for i in results:
        if i is not None:
            items.append(i)
    df = pd.DataFrame(items, columns = ['item_id', 'item_name', 'sell_price', 'buy_price', 'sell_volume', 'buy_volume', 'sell_order_count', 'buy_order_count', 'sell_trend', 'buy_trend'])
    print(df)
    df.to_sql('jita_prices', conn, index=False, if_exists='replace')
