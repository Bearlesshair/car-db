from celery.utils.log import get_task_logger
from celery import task
from carscraper import get_cl_results, get_cc_results, process_posts
from .models import Listing, Car
from datetime import datetime


logger = get_task_logger(__name__)


@task()
def run_scraping():
    all_cars = Car.objects.all()

    for car in all_cars:
        print('-------------CRAIGSLIST--------------')
        results = get_cl_results(car.craigslist_searchterm, car.name)
        print('--------------CARS.COM---------------')
        results += get_cc_results(car.carscom_makeid, car.carscom_modelid)
        print('Processing results')
        results = process_posts(results)
        for result in results:
            # I can't imagine this is the best way to go about assigning values but it works for now
            engine = result['cylinders'] if 'cylinders' in result else None
            mileage = result['odometer'] if 'odometer' in result else None
            seller_type = result['sellerType'] if 'sellerType' in result else None
            title = result['title status'] if 'title status' in result else None
            transmission = result['transmission'] if 'transmission' in result else None
            date = result['date'] if 'date' in result else datetime.now()
            vin = result['VIN'] if 'VIN' in result else None
            year = result['year'] if 'year' in result else None
            price = result['price']
            other_info = result['other_info'] if 'other_info' in result else None
            description = result['description'] if 'description' in result else None
            record = Listing(name=result['listing'],
                             description=description,
                             price=price,
                             date=date,
                             link=result['link'],
                             region=result['region'],
                             engine=engine,
                             mileage=mileage,
                             seller_type=seller_type,
                             transmission=transmission,
                             title=title,
                             year=year,
                             vin=vin,
                             other_info=other_info,
                             car=car)
            record.save()
    find_duplicates()


def find_duplicates():
    listings = Listing.objects.all()
    import datetime
    checked_listings = []
    remove_listings = []
    for listing in listings:
        is_duplicate = False
        for checked_listing in checked_listings:
            day_range = 60
            # date1 = datetime.datetime.strptime(listing['date'], '%Y-%m-%d %H:%M')
            # date2 = datetime.datetime.strptime(checked_listing['date'], '%Y-%m-%d %H:%M')
            similar_date = -1 * day_range <= (listing.date - checked_listing.date).days <= day_range

            same_price = listing.price == checked_listing.price
            same_name = listing.name == checked_listing.name
            if listing.vin is not None and checked_listing.vin is not None:
                same_vin = listing.vin == checked_listing.vin
            else:
                same_vin = None
            if listing.mileage is not None and checked_listing.mileage is not None:
                same_mileage = listing.mileage == checked_listing.mileage
            else:
                same_mileage = None

            if (similar_date and same_vin) \
                    or (similar_date and same_mileage and same_name) \
                    or (similar_date and same_name and same_price):
                if listing.date <= checked_listing.date:  # Apply the oldest found date for a listing
                    checked_listing.date = listing.date
                is_duplicate = True

        if is_duplicate:
            Listing.objects.filter(id=listing.id).delete()
        else:
            checked_listings.append(listing)
