import requests, json
from bs4 import BeautifulSoup as Soup



def Deep():

  # open the data from the wide search
  with open('first_pass.json','r') as json_file:
    shallow_data = json.load(json_file)
  # instantly write a new file to preserve the old one
  with open('evans_data.json', 'w') as json_file:
    json.dump(shallow_data, json_file)

  for key in shallow_data: 

      res = requests.get(f'https://www.evanscycles.com/-{key}')
      index = Soup(res.text,"html.parser")
      name_tags = index.find_all("h1", itemprop="name")
      price_tags = index.find_all("meta", itemprop="price")
      offer_tags = index.find_all("del", class_="text-fade price old")


      if len(name_tags) >= 1 and len(price_tags) >= 1: # did we gett he info we needed?

        # Read it
        with open('evans_data.json','r') as json_file:
          deep_data = json.load(json_file)

        name = name_tags[0].getText().strip('\n ')
        deep_data[key]['brand'] = name.split()[0]
        deep_data[key]['name'] = name
        deep_data[key]['price'] = float(price_tags[0]["content"])
        if len(offer_tags) >= 1:
           str_price = offer_tags[0].getText().strip('£')
           deep_data[key]["RRP"] = float(''.join([c for c in str_price if not c == ","]))
        else:
          deep_data[key]["RRP"] = deep_data[key]['price']
        print(deep_data[key]['name'],deep_data[key]['price'],deep_data[key]['RRP'])

        # Write it
        with open('evans_data.json', 'w') as json_file:
          json.dump(deep_data, json_file)

      else:
        print(key) # this page is probably no longer up

if __name__ == "__main__":
  Deep()