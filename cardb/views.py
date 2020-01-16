import plotly
import plotly.express as px
from django.shortcuts import render
from django.views import generic
import numpy as np
from moneyed import Money
# Create your views here.
from cardb.models import Car, Listing
from cardb.lib.views_helpers import price_stats, mileage_stats


def home(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_cars = Car.objects.all().count()
    num_listings = Listing.objects.all().count()

    # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    context = {
        'num_cars': num_cars,
        'num_listings': num_listings,
    }

    # Render the HTML template home.html with the data in the context variable
    return render(request, 'home.html', context=context)


class CarListView(generic.ListView):
    model = Car


class CarDetailView(generic.DetailView):
    model = Car

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        car = context['car']
        # Add in a QuerySet of all the books
        listings = car.listing_set.all()
        a = np.array([[1, 2, 3, 4]])
        free = Money(amount=0, currency='USD')
        for listing in listings:
            if listing.price is None or listing.price == free or listing.mileage is None:
                continue
            a = np.append(a, [[listing.price, listing.mileage, listing.year, listing.id]], axis=0)
        a = np.delete(a, 0, axis=0)
        print(len(a))
        mileages = a[:, 1]
        prices = a[:, 0]
        year = a[:, 2]
        context['price_stats'] = price_stats(prices)
        context['mileage_stats'] = mileage_stats(mileages)
        # context['graph_div'] = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return context

