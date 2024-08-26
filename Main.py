from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv

def getPage(url):
    link = ('http://127.0.0.1:8000{}'.format(url))
    response = requests.get(link, allow_redirects = True)
    response.raise_for_status()
    html = urlopen(response.url)
    bs = BeautifulSoup(html.read(), 'html.parser')
    return bs

def getCountryInfo(country):
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
    #Timestamp
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y %H:%M:%S")
    
    dataRow = [name, currency, continent, neighboursName, timestamp]
    return dataRow

def getCountries(page: BeautifulSoup):
    table = page.find('table')
    countries = table.find_all('a')
    country_data = []
    for country in countries:
        cPage = getPage(country.attrs['href'])
        country_data.append(getCountryInfo(cPage))

    nextPage = page.find('div', id='pagination',).find('a', string='Next >')
    if nextPage and 'href' in nextPage.attrs:
        getCountries(getPage(nextPage.attrs['href']))

    return country_data

with open('data.csv', mode='w') as file:
    countryData = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    mp = getPage('/places')
    all_country_data = getCountries(mp)
    for dataRow in all_country_data:
        countryData.writerow(dataRow)