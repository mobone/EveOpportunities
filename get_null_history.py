
import pandas as pd
import requests


from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import sqlite3
import datetime
import time

conn = sqlite3.connect("EveFinder.db")
c = conn.cursor()
#sell_region = '10000027' # F9-FUV


def add_to_bad_ids(id, name):
    c.execute('insert into bad_ids values (%s, "%s")' % (id, name.replace("'",'')))
    conn.commit()
    print('\t\t\t\tinserted bad item '+name)

def check_in_bad(type_id, item_name):
    if 'SKIN' in item_name:
        return True
    found_bad_id = pd.read_sql('select * from bad_ids where item_id==%s' % type_id, conn)
    if len(found_bad_id)>=1:
        #print('skipping\t\t\t\t\t', item_name)
        return True

    return False


def parse_data(item):
    s, sell_region, item_name, type_id = item
    #print(item_name)

    if check_in_bad(type_id, item_name) == True:
        return

    while True:
        # F9 market history
        url = 'https://esi.evetech.net/v1/markets/'+str(sell_region)+'/history/?type_id=' + str(type_id)
        market_history = s.get(url)



        if 'exceeded' in market_history.text.lower():
            #print('rate limited exceeded, sleeping')
            time.sleep(30)
            continue
        if 'type not found' in market_history.text.lower():
            add_to_bad_ids(type_id, item_name)
            return []
        if 'error' in market_history.text.lower():
            #print(market_history.text)
            time.sleep(60)
        try:
            item_history_df = pd.DataFrame(market_history.json())
        except:
            #print('json error', type_id)
            return []

        if item_history_df.empty:
            return []

        item_history_df['date'] = pd.to_datetime(item_history_df['date'])
        start_date = datetime.datetime.now() - datetime.timedelta(10)
        item_history_df = item_history_df[item_history_df['date'] >= start_date]

        if item_history_df.empty:
            return []

        total_volume = item_history_df['volume'].sum()
        min_avg = item_history_df['average'].min()
        avg = item_history_df['average'].mean()
        max_avg = item_history_df['average'].max()
        total_order_count = item_history_df['order_count'].sum()
        num_days = len(item_history_df)

        if total_volume == 0:
            return []

        result = [type_id, item_name, min_avg, avg, max_avg, total_order_count, total_volume, num_days]
        #print(sell_region, result)
        return result


if __name__ == '__main__':

    regions_df = pd.read_csv('regions.csv')
    for key, region_row in regions_df.iterrows():

        s = requests.Session()
        print(region_row['Name']+'_'+str(region_row['ID']))
        item_list = []
        items_df = pd.read_csv('all_type_ids.csv')
        for key, row in items_df.iterrows():
            item_list.append((s, region_row['ID'], row['name'].replace('’',"'"), row['typeid']))

        #item_list = [['Capital Core Defense Field Extender I', 31792]]



        with Pool(20) as p:
            results = p.map(parse_data, item_list)


        items = []
        for i in results:
            if i is not None:
                items.append(i)
        df = pd.DataFrame(items, columns = ['item_id', 'item_name', 'min_avg', 'avg', 'max_avg', 'total_orders', 'total_volume', 'num_days'])
        df = df.dropna()
        print(df)
        print()
        df.to_sql(region_row['Name']+'_'+str(region_row['ID']), conn, index=False, if_exists='replace')
