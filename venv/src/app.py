import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from basic import *
import time
from progress.bar import Bar
from progress.spinner import Spinner

opener = AppURLopener()

max, min = set_max_min()

offset = 0
prop_url_list = []

pbar = Bar('Processing', max=20)

spinner = Spinner('searching ')

res_search = site_search(offset,min,max)
while res_search != False:
    prop_url_list.extend(res_search)
    offset += 20
    res_search = site_search(offset,min,max)
    spinner.next()

print("\rCreating dirs in \'daft.ie_scraper/venv/downloads/.....\' and adding pictures...\r")

grab_pics(prop_url_list)


