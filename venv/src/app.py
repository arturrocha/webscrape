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

t1 = site_search(offset,min,max)
while t1 != False:
    prop_url_list.extend(t1)
    offset += 20
    t1 = site_search(offset,min,max)
    spinner.next()

print("\rgrabing pics...\r")

grab_pics(prop_url_list)


