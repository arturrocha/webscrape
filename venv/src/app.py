import requests
from bs4 import BeautifulSoup
import urllib.request
import os

from basic import *

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

max, min = set_max_min()

offset = 100

url = "http://www.daft.ie/dublin-city/residential-property-for-rent/" \
      "?s%5Bmnp%5D={}&s%5Bmxp%5D={}&s%5BsearchSource=rental&offset={}".format(min,max,offset)

response = opener.open(url)
soup = BeautifulSoup(response, "html.parser")

elements = soup.findAll("div", {"class": "box"})

tst = soup.find("div", {"id": "gc_content"})
if "<h1>No results</h1>" in str(tst):
    print("nothing to show")

var = []
bar = []
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

prop_url_list = []
for property in bar:
     prop_url_list.append("http://www.daft.ie" + property[9:-2])

bar = None

iterator = len(prop_url_list)

for i in range(0, iterator):
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
            print(file_path + "/" + image[20:])

            urllib.request.urlretrieve(image, file_path + "/" + image[20:])
            file = open(file_path + '__url.txt', 'w')
            file.write(prop_url_list[i])
            file.close()

