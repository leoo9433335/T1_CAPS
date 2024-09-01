from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import pandas as pd

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

def getCountries(page: BeautifulSoup, country_data):
    table = page.find('table')
    countries = table.find_all('a')
    for country in countries:
        cPage = getPage(country.attrs['href'])
        country_data.append(getCountryInfo(cPage))

    nextPage = page.find('div', id='pagination',).find('a', string='Next >')
    if nextPage and 'href' in nextPage.attrs:
        getCountries(getPage(nextPage.attrs['href']), country_data)

    return country_data

with open('data.csv', mode='w') as file:
    country_data = []
    countryData = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    mp = getPage('/places')
    all_country_data = getCountries(mp, country_data)
    for dataRow in all_country_data:
        countryData.writerow(dataRow)


csvfile=('data.csv')



def lercsv(csvfile):
    with open(csvfile, 'r') as file:
        reader = csv.reader(file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        npk=list(reader)
        return npk
    
def escrevercsv(all_country_data):
     with open(csvfile, 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for dataRow in all_country_data:
            writer.writerow(dataRow)
       

def seexisteatualiza():
    countr = []
    mp = getPage('/places')
    all_country_dat = getCountries(mp, countr)
    bj= getCountryInfo(all_country_dat)
    ##################
    exiscvs=lercsv(csvfile)
      ####################
    update = False

    if len(exiscvs) != len(bj):
                print("precisa atualizar")
                exiscvs = bj
                update = True
    else:
        for i, (row1, row2) in enumerate(zip(bj, country_data)):
            if row1 != row2:
                print(f"Registro {i} atualizado")
                country_data[i] = row1
                updated = True

    if updated:
        escrevercsv(country_data)
        print("Arquivo CSV atualizado")
    else:
        print("Não há atualizações a serem feitas")


        ######kksks
    
#
    seexisteatualiza()
