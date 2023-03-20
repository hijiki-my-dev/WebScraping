import requests
from bs4 import BeautifulSoup
import time

import module


url = "https://dengekibunko.jp/product/newrelease-bunko.html"

time.sleep(1)
r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

module.title_only(soup)



#elms = soup.find_all("a")
#print(soup.select("h1"))

#print(r.headers)
#print(r.content)