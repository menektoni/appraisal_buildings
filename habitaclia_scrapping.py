from bs4 import BeautifulSoup as bs
import requests
import time
import re

def parse_url(url):
    page = requests.get(url).text
    return bs(page, features = 'html.parser')

def get_price(soup):
    try:
        price = soup.find(class_='price').find(class_='font-2').text
    except:
        price = None
    return price

def get_square_meters(soup):
    try:
        square_meters = soup.find_all(class_='feature')[0].text
    except:
        square_meters = None
    return square_meters

def get_rooms(soup):
    try:
        rooms = soup.find_all(class_='feature')[1].text
    except:
        rooms = None
    return rooms

def get_wc(soup):
    try:
        wc = soup.find_all(class_='feature')[2].text
    except:
        wc = None
    return wc

def get_year_construction(soup):
    try:
        general_data = soup.find_all(class_='has-aside')[2].find('ul').find_all('li')
        data = [item.text for item in general_data]
        construction_year = [i for i in data if 'constr' in i]
        # It remains to clean the construction year. Way to go.

    except:
        construction_year = None
    return construction_year

def get_zone(soup):
    try:
        location = soup.find(class_='location').find('a').text
    except:
        location = None
    return location

def get_realstate(soup):
    try:
        realstate = soup.find(id='js-contact-top').find(class_='title').text
    except:
        realstate= None

    return realstate

def get_energy(soup):
    try:
        energy_certificate = soup.find(class_='rating c-G').next.next
    except:
        energy_certificate = None
    return energy_certificate

def get_parking(soup):
    try:
        general_data = soup.find_all(class_='has-aside')[2].find('ul').find_all('li')
        data = [item.text for item in general_data]
        parking = [i for i in data if 'parking' in i]
    except:
        parking = None
    return parking

def get_terrace(soup):
    try:
        general_data = soup.find_all(class_='has-aside')[1].find('ul').find_all('li')
        data = [item.text for item in general_data]
        terrace = [i for i in data if 'Terraza' in i]
    except:
        terrace = None
    return terrace

def get_all_specs(url):
    try:
        soup = parse_url(url)
    except:
        print(f'Cannot parse url: {url}')
        return None

    building_info = {}

    values = ['energy', 'price', 'parking', 'realstate', 'rooms', 'square_meters', 'terrace',
              'wc', 'construction_year', 'zone']
    functions = [get_energy, get_price, get_parking, get_realstate, get_rooms,
                 get_square_meters, get_terrace, get_wc, get_year_construction, get_zone]

    for val, func in zip(values, functions):
        try:
            building_info[val] = func(soup)
        except:
            building_info[val] = None
    return building_info





print(get_all_specs('https://www.habitaclia.com/comprar-apartamento-piso_de_70m2_con_26m2_terraza_en_venta_en_eixample_derecho_dreta_de_l_eixample-barcelona-i4975003169645.htm?f=&geo=c&from=list&lo=55'))