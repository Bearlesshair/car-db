import random
from django import http
import datetime
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


def price_stats(prices):
    ps = np.array([np.percentile(prices, q=0), np.percentile(prices, q=25),
                   np.percentile(prices, q=50), np.percentile(prices, q=75),
                   np.percentile(prices, q=100)])
    return ps


def mileage_stats(mileages):
    ms = np.array([np.percentile(mileages, q=0), np.percentile(mileages, q=25),
                   np.percentile(mileages, q=50), np.percentile(mileages, q=75),
                   np.percentile(mileages, q=100)])
    return ms

