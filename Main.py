from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd

def getPage(url):
    link = ('http://127.0.0.1:8000{}'.format(url))
    response = requests.get(link, allow_redirects = True)
    response.raise_for_status()
    html = urlopen(response.url)
    bs = BeautifulSoup(html.read(), 'html.parser')
    return bs

def getCountryInfo(country, country_data):
    #CountryName
    name = country.find('tr', id='places_country__row').find('td', class_='w2p_fw').string
    print("Getting data from:", name)
    #CountryCurrency
    currency = country.find('tr', id='places_currency_code__row').find('td', class_='w2p_fw').string
    #CountryContinent
    continent = country.find('tr', id='places_continent__row').find('td', class_='w2p_fw').string
    #CountryNeighbours
    neighbours = country.find('tr', id='places_neighbours__row').find('td', class_='w2p_fw').find('div')
    neighboursName = []
    for countries in neighbours:
        nPage = getPage(countries.attrs['href'])
        tr = nPage.find('tr', id='places_country__row')
        if not tr:
            break
        neighboursName.append((tr.find('td', class_='w2p_fw').string))
        getCountryInfo(nPage, country_data)
    #Timestamp
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y %H:%M:%S")
    
    df = pd.DataFrame({'name': name,
                       'currency': currency,
                       'continent': continent,
                       'neighbours': neighboursName})
    country_data.append(df)
    return

def getCountries(page: BeautifulSoup):
    table = page.find('table')
    countries = table.find_all('a')
    all_countries_data = []
    for country in countries:
        cPage = getPage(country.attrs['href'])
        getCountryInfo(cPage, all_countries_data)

    all_countries_df = pd.concat(all_countries_data, ignore_index=True)
    all_countries_df.to_csv('data.csv', index=False)

with open('data.csv', mode='w') as file:
    country_data = []
    mp = getPage('/places')
    getCountries(mp)