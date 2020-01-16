# Homemade Modules
import requests
import yaml
from bs4 import BeautifulSoup as bs

from cardb.lib.craigslist import post
from cardb.lib.craigslist.smartdelay import delay


def do(config_dict):
    with open('regions.yaml', 'r') as f:
        regions = yaml.safe_load(f)
    total = []
    for city, nearbyArea in regions.items():
        if city in config_dict['cities']:
            params = dict(sort='date', hasPic=1, query=config_dict['query'], max_price=config_dict['max_price'],
                          min_price=config_dict['min_price'], s=0, auto_make_model=config_dict['auto_make_model'])
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
            }
            print("Fetching region: %s" % city)
            while True:     # loop to check for more than one page of results
                # set up request
                url_base = 'http://%s.craigslist.org/search/cta%s' % (city, nearbyArea)
                # srchType='T'
                # make search request and parse with beautiful soup
                while True:     # loop to allow continuation when exceptions caught
                    try:
                        rsp = requests.get(url=url_base, params=params, headers=headers)
                    except (ConnectionError, requests.exceptions.RequestException) as e:
                        print("\nConnection error, pausing requests ~5s...")
                        delay(5, 10)
                        continue
                    break
                soup = bs(rsp.text, 'html.parser')
                print(rsp.url)
                for listing in soup.find_all('li', {'class': 'result-row'}):
                    title = listing.find('p').find('a').text
                    price = int(listing.find('span', {'class': 'result-price'}).text.replace('$', ''))
                    date = listing.find('time', {'class': 'result-date'})['datetime']
                    link = listing.find('a')['href']
                    source = 'craigslist'
                    tags = dict(listing=title, price=price, link=link, region=city.title(), date=date, source=source)
                    tags.update(post.add_tags(link, config_dict['auto_make_model']))
                    total.append(tags)
                delay(2, 100)
                nextpage = soup.find('a', {'class': 'button next'})
                if nextpage is None or nextpage['href'] == '':      # nextpage None for no results found, '' for 1 page
                    break
                params['s'] += 120
    #             print("Fetching page %d for region: %s" % (int(params['s']/120+1), city))
    # jsonname = os.path.join(os.path.expanduser("~"), '.carscraper-cl', filename + '.json')
    # changed = getchanged.compare(total, jsonname)
    #
    # # save total to JSON
    # with open(jsonname, 'w') as json_file:
    #     json.dump(total, json_file)

    # check individual postings for each region
    # relevant = []
    # if changed == []:
    #     print("No new listings.")
    # else:
    #     print("Checking posts...")
    #     for listing in progressbar.progressbar(changed):
    #         if post.check(listing['link']):
    #             relevant.append(listing)
    #         delay(0.4, 100)
    #
    print("Completed query for: ", config_dict['auto_make_model'])

    return total
