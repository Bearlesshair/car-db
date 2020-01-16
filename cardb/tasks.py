from celery.utils.log import get_task_logger
from celery import task
from cardb.lib.scraper_harness import get_cl_results, get_cc_results
from .lib import listing_processing
from .models import Car
from geopy.geocoders import Nominatim


logger = get_task_logger(__name__)


@task()
def run_scrapers():
    print('Beginning Scrape...')
    geolocator = Nominatim(user_agent="car_db")

    all_cars = Car.objects.all()

    for car in all_cars:
        print('-------------CRAIGSLIST--------------')
        results = get_cl_results(car.craigslist_searchterm)
        print('--------------CARS.COM---------------')
        results += get_cc_results(car.carscom_makeid, car.carscom_modelid, geolocator)
        print('Adding results to database...')
        listing_processing.import_listings(results, car)
    print('Removing Duplicates...')
    listing_processing.find_duplicates()
    print('Extracting info from listing descriptions...')
    listing_processing.extract_implicit_info()



