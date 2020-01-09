from celery.utils.log import get_task_logger
from celery import task
from carscraper import get_results
from .models import Listing, Car

logger = get_task_logger(__name__)


@task()
def some_task():
    all_cars = Car.objects.all()
    for car in all_cars:
        results = get_results(car._craigslist_searchterm, car.name)
        for result in results:
            # I can't imagine this is the best way to go about assigning values but it works for now
            engine = result['cylinders'] if 'cylinders' in result else None
            mileage = result['odometer'] if 'odometer' in result else None
            title = result['title status'] if 'title status' in result else None
            transmission = result['transmission'] if 'transmission' in result else None
            price = result['price'].replace('$', '')
            record = Listing(name=result['listing'],
                             description=result['description'],
                             price=price,
                             date=result['date'],
                             link=result['link'],
                             region=result['region'],
                             mileage=mileage,
                             engine=engine,
                             transmission=transmission,
                             title=title,
                             car=car)
            record.save()
