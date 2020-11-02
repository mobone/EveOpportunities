import requests_toolbelt
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from requests_toolbelt.threaded import pool
import pandas as pd
#import cloudscraper
url = 'https://zkillboard.com/alliance/99006125/losses/'

'''
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
dr = webdriver.Chrome(executable_path='C:\\Users\\nbrei\\Documents\\GitHub\\OptimalEve\\chromedriver.exe', options=options)
dr.get(url)
time.sleep(7)



scraper = cloudscraper.create_scraper()
page = scraper.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
print(soup.find_all("a", href=re.compile("kill")))
print(page.text)
'''

all_fits_url = 'https://www.eveworkbench.com/rest/fitting/search/'
payload = {
            'Query': '',
            'ShipClass': '',
            'Ships[]': '',
            'Page': 1,
            'MaxResults': 3757, #3757
            'SortField': 'date',
            'SortOrder': 'desc',
            'State': 'both'
           }

session = requests.Session()
json_fits = session.post(all_fits_url, data=payload)
fits = json_fits.json()['results']

urls = []
for fit in fits:
    fit_url = 'https://www.eveworkbench.com' + fit['url']
    urls.append(fit_url)

    #page = requests.get(fit_url)
p = pool.Pool.from_urls(urls)
p.join_all()

items = []
for response in p.responses():
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        ship_url = soup.find("a", href=re.compile("database")).get('href')
        ship_url = ship_url.split('=')
        ship_name = ship_url[1].split('&')[0]
        ship_item_number = ship_url[2]

        items.append([ship_item_number, ship_name])
    except:
        pass
    for item in soup.find_all("a", href=re.compile("market")):
        try:
            item_number = item.get('href').split('/')[3]
            item_name = item.find('img').get('title')
            if ' x ' in item_name:
                item_name = item_name.split(' x ')[0]
            print(item_number, item_name)
            items.append([item_number, item_name])
        except:
            pass
df = pd.DataFrame(items, columns = ['item_id', 'item_name'])

print(df)
items = []
dfs = df.groupby(by='item_id')
for key, df in dfs:
    items.append([df['item_name'].head(1).values[0], key, len(df)])

df = pd.DataFrame(items, columns = ['item_name', 'item_id', 'count'])
df.to_csv('popular_fits.csv')
