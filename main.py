#NotionのAPIキーやデータベースIDはローカルだけに載せる。

import requests
from bs4 import BeautifulSoup
import time
import json
import datetime

import module
import main_local


url = "https://dengekibunko.jp/product/newrelease-bunko.html"

time.sleep(1)
r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

titles = module.title_only(soup)



#elms = soup.find_all("a")
#print(soup.select("h1"))

#print(r.headers)
#print(r.content)


notion_url = 'https://api.notion.com/v1/pages'

api_key = main_local.api_key
databaseid = main_local.databaseid
title = titles[0].text

headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
}

payload = {
    "parent": {
        "database_id": databaseid
    },
    "properties": {
        "名前": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    }
}

response = requests.post(notion_url, json=payload, headers=headers)

#result_dict = response.json()
#result = result