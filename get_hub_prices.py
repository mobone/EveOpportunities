import requests as r
import pandas as pd
from requests_toolbelt.threaded import pool
import sqlite3


conn = sqlite3.connect("EveFinder.db")

items_df = pd.read_csv('all_type_ids.csv')
item_urls = []
for key, row in items_df.iterrows():
    #item_list.append((row['name'].replace('’',"'"), row['typeid']))
    item_urls.append('https://evemarketer.com/api/v1/markets/types/'+str(row['typeid'])+'?language=en')




p = pool.Pool.from_urls(item_urls, session = r.Session)
p.join_all()
dataframes = []
for response in p.responses():

    sell_df = pd.DataFrame.from_records(response.json()['sell'])
    buy_df = pd.DataFrame.from_records(response.json()['buy'])

    if sell_df.empty == False:
        sell_df['region'] = sell_df['region'].astype(str)
        sell_df['station'] = sell_df['station'].astype(str)
        del sell_df['issued_at']
        del sell_df['range']
        del sell_df['duration']
        dataframes.append(sell_df)

    if buy_df.empty == False:
        buy_df['station'] = buy_df['station'].astype(str)
        buy_df['region'] = buy_df['region'].astype(str)
        del buy_df['issued_at']
        del buy_df['range']
        del buy_df['duration']
        dataframes.append(buy_df)




final_df = pd.concat(dataframes)
print(final_df)
final_df.to_sql("all_buy_and_sells", conn, index=False, if_exists='replace')
