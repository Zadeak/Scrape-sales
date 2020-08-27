
import json
import locale
import glob
import os
import subprocess
from staticjinja import Site
import sys


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def format_price(value):
    if value is None or not isinstance(value, int):
        return value
    formatted_price = "{:,d}".format(value).replace(",", " ")
    return formatted_price


filters = {
    'format_price': format_price,
}

dir_path = os.path.abspath("")
def collect_data_filepaths(directory_path=dir_path):
    for file in os.listdir(directory_path):
        if file.endswith(".json"):
            yield os.path.join(directory_path, file)


def renderpage():
    locale.setlocale(locale.LC_ALL, '')
    data_filepaths = list(collect_data_filepaths())
    prices = []
    for filename in data_filepaths:
        with open(filename, 'r') as file:
            site_price = json.loads(file.read())
            prices.extend(site_price)
    site = Site.make_site(env_globals={
        'prices': prices,
    }, filters=filters)

    site.render(use_reloader=False)
    pathtofile = "index.html"
    open_file(pathtofile)
