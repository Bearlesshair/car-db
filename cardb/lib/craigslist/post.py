import requests
from bs4 import BeautifulSoup as bs
from .smartdelay import delay
import re


def checkTitle(soup, titlekeywords):
    title = soup.find('span', {'id': 'titletextonly'}).text
    for word in titlekeywords:
        if word.lower() not in title.lower():
            return False
    return True


def checkBody(soup, bodykeywords):
    body = soup.find('section', {'class': 'userbody'}).text
    for word in bodykeywords:
        if word.lower() not in body.lower():
            return False  # if keyword missing from body return false
    return True  # otherwise return true


def get_soup(url):
    # fetch posting
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    while True:
        try:
            rsp = requests.get(url=url, headers=headers)
        except (ConnectionError, requests.exceptions.RequestException) as e:
            print("Connection error, pausing requests ~5s...")
            delay(5, 10)
            continue
        break

    soup = bs(rsp.text, 'html.parser')
    return soup


def add_tags(url, searchterm):
    soup = get_soup(url)

    attributes = soup.find_all('p', {'class': 'attrgroup'})
    attr_dict = {}
    try:
        longitude_str = soup.find('div', {'id': 'map'}).attrs['data-longitude']
        latitude_str = soup.find('div', {'id': 'map'}).attrs['data-latitude']
        attr_dict['longitude'] = float(longitude_str)
        attr_dict['latitude'] = float(latitude_str)
    except TypeError:
        print('Map not found - TypeError')
    except AttributeError:
        print('Map not found - Attribute Error')
    except KeyError:
        print('Latitude and longitude not found.')
    body = soup.find('section', {'id': 'postingbody'})
    if body is not None:
        desc = body.text
    else:
        desc = ''
    for attribute in attributes:
        for attr in attribute.find_all('span'):
            text = attr.text
            yearfind = f'(?=.?{searchterm})' + '\d{4}'
            if ':' in text:
                groups = text.split(': ')
                attr_dict[groups[0]] = groups[1]
            elif re.search(yearfind, text):
                attr_dict['year'] = re.search(yearfind, text).group()
            elif text.find('more ads  by this user') != -1:
                attr_dict['sellerType'] = 'Dealer'
    attr_dict['description'] = desc
    return attr_dict


def identify_dealership_posts(listing):
    if 'description' in listing:
        desc = listing['description']
        if re.match('(?:bad credit)|(?:stock ?#)|(?:financing)', desc):
            listing['sellerType'] = 'Dealer'