from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd

def getUrl(href):
    link = ('http://127.0.0.1:8000{}'.format(href))
    response = requests.get(link, allow_redirects = True)
    response.raise_for_status()
    return response.url

def getPage(href):
    html = urlopen(getUrl(href))
    bs = BeautifulSoup(html.read(), 'html.parser')
    return bs

def getCountryInfo(country_href, countries_data, countryPage):
    if getUrl(country_href) in visited:
        return
    visited.append(getUrl(country_href))
    print(country_href)
    if countryPage is None:
        country = getPage(country_href)
    else:
        country = countryPage
    #CountryName
    name = country.find('tr', id='places_country__row').find('td', class_='w2p_fw').string
    print(f'Getting data from: {name}')
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
        getCountryInfo(countries.attrs['href'], countries_data, nPage)
    #Timestamp
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y %H:%M:%S")
    
    df = pd.DataFrame({'Country': [name], 'Currency': [currency], 'Continent': [continent], 'Neighbours': [neighboursName], 'Updated at': [timestamp]})
    countries_data.append(df)
    return


def getCountries(page: BeautifulSoup, data):
    countries_data = data
    table = page.find('table')
    countries = table.find_all('a')
    for country in countries:
        getCountryInfo(country.attrs['href'], countries_data, None)

    nextPage = page.find('div', id='pagination',).find('a', string='Next >')
    if nextPage and 'href' in nextPage.attrs:
        getCountries(getPage(nextPage.attrs['href']), countries_data)

    return countries_data

with open('data.csv', mode='w') as file:
    visited = []
    country_data = []
    mp = getPage('/places')
    all_country_data = getCountries(mp, country_data)
    all_countries_df = pd.concat(all_country_data, ignore_index=True)
    # Save the DataFrame to a CSV file
    all_countries_df.sort_values(by='Country', inplace=True)
    all_countries_df.to_csv("data.csv", index=False)