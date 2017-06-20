#!/usr/bin/python
# -*- encoding: utf-8 -*-
from urllib2 import urlopen
import json
from BeautifulSoup import BeautifulSoup

defaultPage = 1
items = []
url = "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/%d/"


def getWebsiteContent(page=defaultPage):
    return urlopen(url % (page)).read()

def writeToFile(content):
    file = open("nepremicnine1.json", "w+")
    json.dump(content, file)
    file.close()

def main():
    defaultPage = 1
    while (defaultPage <= 500):
        content = getWebsiteContent(page=defaultPage)
        soup = BeautifulSoup(content)
        posesti = soup.findAll("div", {"itemprop": "itemListElement"})

        for stanovanja in posesti:

            item = {}
            item["Naslov"] = stanovanja.find("span", attrs={"class": "title"}).string
            item["Velikost"] = stanovanja.find("span", attrs={"class": "velikost"}).string[:-3].replace(",",".")
            if float(item["Velikost"]) > 100 or float(item["Velikost"]) < 70:
                continue
            item["Cena"] = stanovanja.find("span", attrs={"class": "cena"}).string[:-10].replace(".","")
            if float(item["Cena"]) < 200000:
                continue
            item["Slika"] = stanovanja.find("img", src = True)["src"]



            items.append(item)

            writeToFile(items)
        defaultPage += 1
main()

