from bs4 import BeautifulSoup
import requests
import re
import time
import csv
import random
import datetime



def normalizeText(string): 

    string = string.replace("\n","")
    string  = re.sub(r"\d+", "", string)
    string = re.sub(r"\(.*?\)", "", string)
    #for i in badText:
    #    string = string.replace(i, "")
    string = re.sub(r"\Ws\W", "", string)
    string = string.strip()
    return string


t = datetime.datetime.now()

doc = requests.get("https://www.seriouseats.com/sitemap_1.xml")

soup = BeautifulSoup(doc.content, 'lxml-xml')

foundURLS = soup.find_all('loc')
urls = []
for i in foundURLS:
    urls.append(i.text)

fullData = []
w = csv.writer(open("output.csv", "w"))
w.writerow(("URL","Ingredients","Steps","Cuisine"))
for i in urls:
    if i.find("recipe") != -1:
        try:
            doc = requests.get(i)
        except Exception as e:
            print("Could not get request")
            print(e)
            continue
        try:
            soup = (BeautifulSoup(doc.content, 'lxml-xml'))
            ingredients = [normalizeText(ingredient.text) for ingredient in soup.find_all("li", class_ = ["structured-ingredients__list-item", "simple-list__item js-checkbox-trigger ingredient text-passage"])]
            if ingredients == []:
                continue
            cuisine = [cuisine.text.replace('\n',"") for cuisine in soup.find_all("li", {'class' : 'link-list__item tag-nav__item'})]
            steps = [step.findChild().text for step in soup.find_all('LI', {"class":"comp mntl-sc-block-group--LI mntl-sc-block mntl-sc-block-startgroup"})]
        except Exception as e:
            print(e)
            print("Error in parsing soup")
        try:
            fullData.append((i, ingredients, steps, cuisine))
            w.writerow((i,ingredients,steps,cuisine))
        except Exception as e:
            print(e)
            print("Error writing data")
            continue

        time.sleep(random.uniform(2,20))

print("\n\nDONEDONEDONE\nCompleted in:", datetime.datetime.now() - t, "\n\n")
