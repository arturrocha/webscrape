import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from basic import *
import time
from progress.bar import Bar
from progress.spinner import Spinner

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def set_max_min():
    set_max = input("Set your max price in euros or leave blank for no MAX (example: >800): >")
    set_min = input("Set your min price in euros or leave blank for no MIN (example: >200): >")
    if set_max == "":
        max = 9999999
    else:
        max = int(set_max)

    if set_min == "":
        min = 0
    else:
        min = int(set_min)
    return (max, min)

def site_search(offset,min,max):
    bar = []
    #daft site
    url = "http://www.daft.ie/dublin-city/residential-property-for-rent/" \
          "?s%5Bmnp%5D={}&s%5Bmxp%5D={}&s%5Bsort_by%5D=price&s%5BsearchSource=rental&offset={}".format(min, max, offset)
    opener = AppURLopener()
    response = opener.open(url)
    soup = BeautifulSoup(response, "html.parser")

    #testing to see if search has results
    result_search = soup.find("div", {"id": "gc_content"})
    if "<h1>No results</h1>" in str(result_search):
        return False
    else:
        #grabing search results putting as a list with the url for each property
        elements = soup.findAll("div", {"class": "box"})
        for element in elements:
            for line in element:
                vars = str(element).splitlines()
                for var in vars:
                    if "href=" in var:
                        if "<li>" not in var and "Learn more" not in var and "><span class=" not in var and "https://www.daft.ie/" not in var and "smi-onview-cal-link" not in var:
                            if "View more details" in var:
                                var = var.split(">View ", 1)[0]
                                if var not in bar:
                                    bar.append(str(var))
                            else:
                                if var not in bar:
                                    bar.append(str(var))

        #editing url for proper http://.....
        prop_url_list = []
        for property in bar:
            prop_url_list.append("http://www.daft.ie" + property[9:-2])

        return prop_url_list

def grab_pics(prop_url_list):
    iterator = len(prop_url_list)
    pbar = Bar('Processing', max=iterator)
    for i in range(0, iterator):
        opener = AppURLopener()
        response = opener.open(prop_url_list[i])
        soup = BeautifulSoup(opener.open(prop_url_list[i]), "html.parser")
        elements = soup.findAll("div", {"class": "smi-gallery"})
        elements.append(soup.findAll("ul", {"class": "smi-gallery-list"}))

        images = []
        for element in elements:
            vars = str(element).splitlines()
            for var in vars:
                if "<img alt=" in var:
                    images.append(str(var))

        image_list = []
        for image in images:
            image_ = image.split()
            for thing in image_:
                if "src=" in thing:
                    s = list(thing)
                    del s[9]
                    s = "".join(s)
                    new_thing = s
                    image_list.append(new_thing[5:-1])

        bar = []
        photos_url = []
        clean = prop_url_list[i].replace("/", "")
        clean = clean.replace(":", "")
        file_path = "../downloads/" + clean[0:60] + "/"
        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        for image in image_list:
            if "daft_no_photo_" not in image[20:]:
                urllib.request.urlretrieve(image, file_path + "/" + image[20:])
                file = open(file_path + '__url.txt', 'w')
                file.write(prop_url_list[i])
                file.close()
        pbar.next()
    pbar.finish()