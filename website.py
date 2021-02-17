
import pandas as pd
import flask
from flask import request, jsonify, render_template
import sqlite3
import json
import numpy as np
import time
from flask_cors import CORS, cross_origin



app = flask.Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/ranked_items', methods = ['GET'])
def get_ranked_items_page():
    ranked_items = get_ranked_items()
    return render_template('ranked_items.html', ranked_items = eval(ranked_items))

@app.route('/api/v1/items/trade_hub', methods = ['GET'])
def get_trade_hub_items():
    sql = '''select * from {0} left join {0} on {0}.item_id == '''

@app.route('/api/v1/items/ranked', methods = ['GET','POST'])
def get_ranked_items():

    query_parameters = request.args

    emphasize = query_parameters.get('emphasize')
    region = query_parameters.get('region')
    hub = query_parameters.get('hub')

    min_profit = query_parameters.get('min_profit')

    if emphasize:
        emphasize = emphasize.split(',')
    else:
        emphasize = []

    regions_df = pd.read_csv("regions.csv")
    regions_df = regions_df[regions_df['Name']==region.replace(" ","_")]

    history_region_id = str(regions_df['Name'].values[0])+'_'+str(regions_df['ID'].values[0])
    print('got region id of: ', history_region_id)

    #print(emphasize)

    conn = sqlite3.connect('EveFinder.db')
    sql = '''select jita_prices.item_id, jita_prices.item_name, item_details.item_type,
             item_details.item_volume, jita_prices.buy_price, {0}.min_avg,
             {0}.num_days, {0}.total_volume, popular_fits.count
             from jita_prices  left join {0} on
             {0}.item_id = jita_prices.item_id left join
             item_details on item_details.item_id = jita_prices.item_id
             left join popular_fits on popular_fits.item_id = jita_prices.item_id;
          '''

    df = pd.read_sql(sql.format(history_region_id), conn)

    df['cost'] = df['item_volume'].astype(float) * 800

    df['profit'] = df['min_avg'] - df['buy_price'] - df['cost']
    df['profit_percent'] = df['profit']/df['buy_price']

    #df = df[df['profit_percent']>.07]
    df['profit_percent'] = df['profit_percent'] * 100

    df['vol_per_day'] = df['total_volume'] / 30.0
    #print(df)

    df = df[['item_id', 'item_name', 'item_type', 'buy_price', 'min_avg', 'profit', 'profit_percent', 'total_volume', 'num_days', 'item_volume', 'vol_per_day', 'cost']]

    new = df['item_type'].str.split(',', n = 1, expand = True)
    df['item_type'] = new[0]



    df['profit rank'] = df['profit'].rank() * (1,3)['profit' in emphasize]
    df['profit percent rank'] = df['profit_percent'].rank() * (1,3)['profit_percent' in emphasize]
    df['total volume rank'] = df['total_volume'].rank() * (1,3)['total_volume' in emphasize]
    df['num days rank'] = df['num_days'].rank() * (1,3)['num_days' in emphasize]
    #df['cost rank'] = df['num_days'].rank(ascending=False) * (1,3)['cost' in emphasize]
    #df['fit count rank'] = df['count'].rank() * (1,3)['count' in emphasize]
    df['vol_per_day_rank'] = df['vol_per_day'].rank() * (1,3)['vol_per_day' in emphasize]

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
    df = df.round(2)

    df = df[df['profit']>float(min_profit)]
    #df = df[df['item_type']=='Pilots Services']




    df['buy_price'] = round(df['buy_price'])
    df['profit'] = round(df['profit'])

    df['buy_price'] = df.apply(lambda x: "{:,}".format(x['buy_price']), axis=1)
    df['min_avg'] = df.apply(lambda x: "{:,}".format(x['min_avg']), axis=1)
    df['profit'] = df.apply(lambda x: "{:,}".format(x['profit']), axis=1)
    df['avg'] = df['min_avg']
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

    df = df.head(200)

    return df.to_json(orient='records')

app.run(host='0.0.0.0')
