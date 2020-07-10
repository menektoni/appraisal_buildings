from bs4 import BeautifulSoup as bs
import requests
import time
import re
import pandas as pd
import numpy as np

def parse_url(url):
    page = requests.get(url).text
    return bs(page, features = 'html.parser')

def get_price(soup):
    try:
        price = soup.find(class_='price').find(class_='font-2').text
        price_list = re.findall('\d+', price)
        price_clean = int(''.join(map(str, price_list)))
    except:
        price_clean = None
    return price_clean

def get_square_meters(soup):
    try:
        square_meters = soup.find_all(class_='feature')[0].text
        square_meters = re.findall('\d+', square_meters)
    except:
        square_meters = None
    return int(square_meters[0])
def get_rooms(soup):
    try:
        rooms = soup.find_all(class_='feature')[1].text
        rooms = re.findall('\d+', rooms)
    except:
        rooms = None
    return int(rooms[0])

def get_wc(soup):
    try:
        wc = soup.find_all(class_='feature')[2].text
        wc = re.findall('\d+', wc)
    except:
        wc = None
    return int(wc[0])

def get_year_construction(soup):
    try:
        general_data = soup.find_all(class_='has-aside')[2].find('ul').find_all('li')
        data = [item.text for item in general_data]
        construction_year = [i for i in data if 'constr' in i]
        # It remains to clean the construction year. Way to go.
        construction_year = re.findall('\d+', construction_year[0])

    except:
        construction_year = None
    return int(construction_year[0])

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
        energy_certificate = soup.find(class_='rating-box').next.next.next.next
        energy_certificate = re.findall('\d+', energy_certificate)

    except:
        energy_certificate = None
    return int(energy_certificate[0])

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
        terrace = terrace[0].split(u'\xa0')
        terrace = re.findall('\d+', terrace[0])
    except:
        terrace = None
    return int(terrace[0])

def get_all_specs(url):
    try:
        soup = parse_url(url)
    except:
        print(f'Cannot parse url: {url}')


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

all_b = [] # All the buildings info
def get_all_page_urls(url):
    page = parse_url(url)
    links = page.find(class_='list-items').find_all('a')

    building_links_pre = [link['href'] for link in links]
    building_links = [b_link for b_link in building_links_pre if 'comprar' in b_link]

    return building_links

pages_links = [] # The links of each existing page.
def get_all_pages(url):
    page = parse_url(url)
    limit = page.find(id = 'js-nav').find('ul').find(class_='gap').next.next.next.next.text
    limit = int(limit)

    for i in range(1, limit):
        pages_links.append('https://www.habitaclia.com/viviendas-barcelona-' + str(i) + '.htm')

    return pages_links


# BCN
def all_lego(url):
    pages = get_all_pages(url)
    for page in pages:
        time.sleep(3 + np.random.random())
        building_links = get_all_page_urls(page)
        for building in building_links:

            all_b.append(get_all_specs(building))
    return all_b


all_lego('https://www.habitaclia.com/viviendas-barcelona-1.htm')

barcelona = pd.DataFrame(all_b)

barcelona.to_csv('barcelona.csv', index = False)
