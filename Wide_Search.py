# Scrape www.evanscycles.com for currently listed product codes and save them in JSON format to "/first_pass.json"
import requests, json
from bs4 import BeautifulSoup as Soup

def Wide():

  def search(category):

    loop = True
    page = 0
    codes = []

    while loop:
      res = requests.get(f'https://www.evanscycles.com/bikes/{category}_c?page={str(page)}')
      print(f'page {page} of {category} results')
      page += 1
      index = Soup(res.text,"html.parser")
      tags = index.find_all("meta", itemprop="productId")
      print(len(tags))
      if len(tags) >= 2:
        for tag in tags:
          if (tag["content"])[0] == "E":
            codes.append(tag["content"])
      else: 
        loop = False
      
    return codes


  data = {}
  categories = ['road-bikes','cyclocross-bikes','mountain-bikes','touring-bikes','hybrid-bikes','folding-bikes']

  for cat in categories:
    cat_codes = search(cat)
    for code in cat_codes:
      if code in data:
        print("overwritten")
      data[code] = {'category': cat}

  with open('first_pass.json', 'w') as data_save:
    json.dump(data, data_save)


if __name__ == "__main__":
  Wide()