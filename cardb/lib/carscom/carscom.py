import re
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim


def next_page(url, page):
    url = re.sub("&page=" + str(page) + "&", "&page=" + str(page + 1) + "&", url)
    return url


def run_scraper(mkid,mdid, gl):
    url = f'https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&mdId={mdid}&mkId={mkid}&page=1&perPage=100&rd=99999&searchSource=GN_BREADCRUMB&sort=relevance&zc=55127'
    page_match = re.search("&page=(\d+)&", url)
    page = int(page_match.groups()[0])
    last_page = 0
    listings = []
    while page != last_page:
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        type(soup)
        # Extracts the car data
        # text = soup.get_text()
        # print(soup.text)
        all_scripts = soup.find_all('script')
        page_listings = []
        for script in all_scripts:
            text = str(script)
            # print(text)

            if re.search("CARS\.digitalData\W=\W(.+);", text):
                z = re.search("CARS\.digitalData\W=\W(.+);", text)
                x = z.groups()[0]
                foo = json.loads(x)
                search_info = foo["page"]["search"]
                # print(search_info)
                page_listings = foo["page"]["vehicle"]
        for listing in page_listings:
            listings.append(standardize_carscom(listing, gl))
        page = search_info['pageNum']
        last_page = search_info['totalNumPages']
        print(f'Done with page {page} of {last_page}')
        url = next_page(url, page)
    return listings


class Seller:
    def __init__(self, seller_data):
        self.id = seller_data['id']
        self.name = seller_data['name']
        self.phone_number = seller_data['phoneNumber']
        self.distance_from_search_zip = seller_data['distanceFromSearchZip']
        self.customer_id = seller_data['customerId']
        self.display_label = seller_data['sellerDisplayLabel']
        self.address = seller_data['streetAddress']
        self.city = seller_data['city']
        self.state = seller_data['state']


def standardize_carscom(listing, geolocator):
    output = {
        'listing': f"{listing['year']} {listing['make']} {listing['model']}",
        'stock_type': listing['stockType'],
        'make': listing['make'],
        'make_id': listing['makeId'],
        'model': listing['model'],
        'model_id': listing['modelId'],
        'year': listing['year'],
        'trim': listing['trim'],
        'body_style': listing['bodyStyle'],
        'private_seller': listing['privateSeller'],
        'price': listing['price'],
        'odometer': listing['mileage'],
        'VIN': listing['vin'],
        'certified': listing['certified'],
        'city': listing['seller']['city'],
        'state': listing['seller']['state'],
        'link': f'https://www.cars.com/vehicledetail/detail/{listing["listingId"]}/overview/',
        'source': 'cars.com'}
    return output


def get_long_lat(street, city, state, geolocator):
    loc = geolocator.geocode(f'{street}, {city}, {state}')
    if loc is not None:
        return [loc.longitude, loc.latitude]
    else:
        return [None, None]
