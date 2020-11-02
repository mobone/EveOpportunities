
import pandas as pd
import requests


from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import sqlite3
import datetime
import time




conn = sqlite3.connect("EveFinder.db")


s = requests.Session()

def parse_data(item):

    item_name, type_id = item

    try:
        # item type list
        everef_response = s.get('https://everef.net/type/' + str(type_id))
        if everef_response.status_code != 200:
            print('error getting everef page', everef_response.status_code)
        soup = BeautifulSoup(everef_response.text, 'html.parser')
        try:
            type_list = soup.select_one('li:contains("Market Groups")').parent.find_all('span') #find_all('li', {'class': 'breadcrumb-item'}).find_all('span')
        except:
            return
        parsed_type_list = []
        for type in type_list:
            parsed_type_list.append(type.text)

        parsed_type_list = list(dict.fromkeys(parsed_type_list))
        del parsed_type_list[0]
        item_type = str(parsed_type_list)[1:-1].replace("'","")

        x = soup.select_one('tr:contains("Repackage")') #can get repacked volume
        if x is None:
            x = soup.select_one('tr:contains("Volume")')
        item_volume = x.find('span', {'itemprop': 'value'}).text
        print([type_id, item_name, item_type, item_volume])
        return [type_id, item_name, item_type, item_volume]
    except Exception as e:
        print('exception\t\t', e, item_name, type_id)

        time.sleep(50)



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
    df = pd.DataFrame(items, columns = ['item_id', 'item_name', 'item_type', 'item_volume'])
    df = df.dropna()
    print(df)
    df.to_sql('item_details', conn, index=False, if_exists='replace')
