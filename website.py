
import pandas as pd
import flask
from flask import request, jsonify, render_template
import sqlite3
import json
import numpy as np
import time
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/ranked_items', methods = ['GET'])
def get_ranked_items_page():
    ranked_items = get_ranked_items()
    return render_template('ranked_items.html', ranked_items = eval(ranked_items))



@app.route('/api/v1/items/ranked', methods = ['GET'])
def get_ranked_items():

    query_parameters = request.args

    emphasized = query_parameters.get('emphasized')
    history_region_id = query_parameters.get('history_region_id')

    if emphasized:
        emphasized = emphasized.split(',')
    else:
        emphasized = []

    #print(emphasized)

    conn = sqlite3.connect('EveFinder.db')
    sql = '''select jita_prices.item_id, jita_prices.item_name, item_details.item_type,
             item_details.item_volume, jita_prices.buy_price, {0}.avg,
             {0}.num_days, {0}.total_volume, popular_fits.count
             from jita_prices  left join {0} on
             {0}.item_id = jita_prices.item_id left join
             item_details on item_details.item_id = jita_prices.item_id
             left join popular_fits on popular_fits.item_id = jita_prices.item_id;
          '''

    df = pd.read_sql(sql.format(history_region_id), conn)

    df['cost'] = df['item_volume'].astype(float) * 800

    df['profit'] = df['avg'] - df['buy_price'] - df['cost']
    df['profit_percent'] = df['profit']/df['buy_price']

    df['profit_percent'] = df['profit_percent'] * 100

    df['vol_per_day'] = df['total_volume'] / 10.0
    #print(df)

    df = df[['item_id', 'item_name', 'item_type', 'buy_price', 'avg', 'profit', 'profit_percent', 'total_volume', 'num_days', 'item_volume', 'vol_per_day', 'cost', 'count']]

    new = df['item_type'].str.split(',', n = 1, expand = True)
    df['item_type'] = new[0]

    df['profit rank'] = df['profit'].rank() * (1,3)['profit' in emphasized]
    df['profit percent rank'] = df['profit_percent'].rank() * (1,3)['profit_percent' in emphasized]
    df['total volume rank'] = df['total_volume'].rank() * (1,3)['total_volume' in emphasized]
    df['num days rank'] = df['num_days'].rank() * (1,3)['num_days' in emphasized]
    #df['cost rank'] = df['num_days'].rank(ascending=False) * (1,3)['cost' in emphasized]
    df['fit count rank'] = df['count'].rank() * (1,3)['count' in emphasized]
    df['vol_per_day_rank'] = df['vol_per_day'].rank() * (1,3)['vol_per_day' in emphasized]

    df['total rank'] = df['profit rank'] * 2 + df['profit percent rank'] + \
                       df['total volume rank'] + df['num days rank']
                       #df['fit count rank'] #+ df['cost rank']
    df['total rank'] = df['total rank'].rank(ascending=False)

    #del df['profit rank']
    #del df['profit percent rank']
    #del df['total volume rank']
    #del df['num days rank']
    #del df['fit count rank']



    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    df = df[df['profit']>4000000]
    df['buy_price'] = round(df['buy_price'])
    df['profit'] = round(df['profit'])

    df['buy_price'] = df.apply(lambda x: "{:,}".format(x['buy_price']), axis=1)
    df['profit'] = df.apply(lambda x: "{:,}".format(x['profit']), axis=1)
    '''
    for key, row in df.iterrows():


        if row['buy_price']>1000000000:
            buy_price = str(round(row['buy_price'] / 1000000000.0,0))+'b isk'
        elif row['buy_price']>1000000:
            buy_price = str(round(row['buy_price'] / 1000000.0,0))+'m isk'
        elif row['buy_price']>1000:
            buy_price = str(round(row['buy_price'] / 1000.0,0))+'k isk'

        else:
            buy_price = str(round(row['buy_price'],0))

        df.loc[key,'buy_price'] = buy_price


        if row['profit']>1000000000:
            profit = str(round(row['profit'] / 1000000000.0,0))+'b isk'
        elif row['profit']>1000000:
            profit = str(round(row['profit'] / 1000000.0,0))+'m isk'
        elif row['profit']>1000:
            profit = str(round(row['profit'] / 1000.0,0))+'k isk'

        else:
            profit = str(round(row['profit'],0))

        df.loc[key,'profit'] = profit

    '''
    int_cols = ['total rank', 'profit_percent', 'total_volume', 'num_days']
    df[int_cols] = df[int_cols].applymap(np.int64)


    df = df.sort_values(by=['total rank'])
    #print(df)
    df = df.head(100)

    return df.to_json(orient='records')

app.run(host='0.0.0.0')
