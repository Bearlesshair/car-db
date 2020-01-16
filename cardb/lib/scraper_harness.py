from .craigslist.query import do
from .craigslist.config import get
from .carscom.carscom import run_scraper


def get_cl_results(search_term, config_path=None):

    # get configuration
    config_dict = get(config_path)
    config_dict['auto_make_model'] = search_term  # THIS SEARCHES CAR MAKE/MODEL, NOT TITLE
    # run query
    result = do(config_dict)  # Multiple filenames to parse new entries
    return result


def get_cc_results(mkid,mdid, gl):
    return run_scraper(mkid, mdid, gl)


