import re
from datetime import datetime

from moneyed import Money
from django.utils.timezone import make_aware

from ..models import Listing


def extract_implicit_info():
    listings = Listing.objects.all()
    for listing in listings:
        if listing.price < Money(amount=100, currency='USD') \
                and re.search('Attempted to extract price from description.', listing.other_info) is None:
            listing.price = _find_price(listing)
        if listing.mileage is None \
                and re.search('Attempted to extract mileage from description.', listing.other_info) is None:
            listing.mileage = _find_mileage(listing)
        if listing.year is None\
                and re.search('Attempted to extract year from title.', listing.other_info) is None:
            listing.year = _find_year(listing)
        listing.save()


def _find_price(listing):
    desc = listing.description.lower()
    possible_prices = re.findall('(?:asking |\$)((?:\d{1,5}?,?\d{3}?)|(?:\d+k))', desc)
    if len(possible_prices) != 1:
        listing.other_info += 'Attempted to extract price from description.\n'
        return listing.price
    price = re.sub('k', ' 000', possible_prices[0])
    price = re.sub(',', '', price)
    listing.other_info += 'Price extracted from description.\n'
    return price


def _find_mileage(listing):
    desc = listing.description.lower()
    mileages = re.findall('mileage:\s*((?:\d{1,6}(?:,(?:\d{3}|xxx))?)|(?:\d+k))', desc)
    if len(mileages) != 1:
        listing.other_info += 'Attempted to extract mileage from description.\n'
        return None
    mileage = re.sub('k', '000', mileages[0])
    mileage = re.sub(',', '', mileage)
    listing.other_info += 'Mileage extracted from description.\n'
    return mileage


def purge_bad_years():
    listings = Listing.objects.all()
    for listing in listings:
        if listing.year is None:
            continue
        elif listing.car.start_year <= listing.year <= listing.car.end_year:
            continue
        listing.year = None
        listing.save()


def purge_other_info(pattern, new):
    listings = Listing.objects.all()
    for listing in listings:
        listing.other_info = re.sub(pattern, new, listing.other_info)
        listing.save()


def _find_year(listing):
    title = listing.name
    min_year = listing.car.start_year
    max_year = listing.car.end_year
    years = re.findall('(\d{4}|\d{2}) ', title)
    if len(years) == 0:
        listing.other_info += 'Attempted to extract year from title.\n'
        return None
    years_found = []
    for year in years:
        year = int(year)
        if 50 < year < 100:
            year = year + 1900
        elif year < 100:
            year = year + 2000

        if min_year <= year <= max_year:
            years_found.append(year)

    if len(years_found) == 1:
        listing.other_info += 'Year extracted from title.\n'
        return years_found[0]
    else:
        listing.other_info += 'Attempted to extract year from title.\n'
        return None


def find_duplicates():
    listings = Listing.objects.all()
    checked_listings = []
    for listing in listings:
        is_duplicate = False
        for checked_listing in checked_listings:
            day_range = 60
            # date1 = datetime.datetime.strptime(listing['date'], '%Y-%m-%d %H:%M')
            # date2 = datetime.datetime.strptime(checked_listing['date'], '%Y-%m-%d %H:%M')
            similar_date = -1 * day_range <= (listing.date - checked_listing.date).days <= day_range

            same_price = listing.price == checked_listing.price
            if listing.price == 0:
                same_price = None
            same_name = listing.name == checked_listing.name
            if listing.vin != '' and checked_listing.vin != '':
                same_vin = listing.vin == checked_listing.vin
            else:
                same_vin = None
            if listing.mileage is not None and checked_listing.mileage is not None:
                same_mileage = listing.mileage == checked_listing.mileage
            else:
                same_mileage = None
            same_source = listing.source == checked_listing.source
            source = listing.source

            if (similar_date and same_vin) \
                    or (
                    similar_date and
                    same_mileage and
                    same_name and same_source and same_vin is None and (same_price is None or same_price)) \
                    or (
                    similar_date and
                    same_name and
                    same_price and same_source and same_vin is None and (same_mileage is None or same_mileage)):
                if listing.date <= checked_listing.date:  # Apply the oldest found date for a listing
                    checked_listing.date = listing.date
                update_old_listing(listing, checked_listing)
                is_duplicate = True

        if is_duplicate:
            Listing.objects.filter(id=listing.id).delete()
        else:
            checked_listings.append(listing)


def import_listings(results, car):
    for result in results:
        # Price cannot be None
        price = result['price'] if result['price'] is not None else 0
        record = Listing(name=result['listing'],
                         car=car,
                         city=get_set(result, 'city', ''),
                         date=get_set(result, 'date', make_aware(datetime.now())),
                         description=get_set(result, 'description', ''),
                         engine=get_set(result, 'engine', ''),
                         latitude=get_set(result, 'latitude', None),
                         link=result['link'],
                         longitude=get_set(result, 'longitude', None),
                         mileage=get_set(result, 'odometer', None),
                         other_info=get_set(result, 'other_info', ''),
                         price=price,
                         state=get_set(result, 'state', ''),
                         seller_type=get_set(result, 'seller_type', ''),
                         source=result['source'],
                         title=get_set(result, 'title', ''),
                         transmission=get_set(result, 'transmission', ''),
                         vin=get_set(result, 'vin', ''),
                         year=get_set(result, 'year', None))
        record.save()


def get_set(result, field, default):
    return result[field] if field in result else default


def update_old_listing(new, old):
    for field in new._meta.get_fields():
        new_value = field.value_from_object(new)
        old_value = field.value_from_object(old)
        if field.name == 'id' or field.name == 'date':
            continue
        if new_value != old_value and new_value is not None and new_value != 0 and new_value != '':
            setattr(old, field.name, new_value)
    old.save()
