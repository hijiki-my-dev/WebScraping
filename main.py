#NotionのAPIキーやデータベースIDはローカルだけに載せる。

import requests
from bs4 import BeautifulSoup
import time
import json
import datetime

#import module
import main_local


class label:
    def __init__(self, title_name, date, tag_name):
        self.title = title_name
        self.tag = tag_name
    

def dengeki(list):
    #電撃文庫の今月と来月発売の作品タイトルと発売日を抜粋
    #タイトルと発売日を順番に表示するにはループを使う。elmsは配列だから、それで回す。
    url = "https://dengekibunko.jp/product/newrelease-bunko.html"

    time.sleep(1)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")
    
    elms = s.select(".p-books-media__title > a")
    tag = "電撃"
    
    for elm in elms:
        cl = label(elm.text, date, tag)
        list.append(cl)
        
    return list


def main():
    all_list = []
    all_list = dengeki(all_list)


    #elms = soup.find_all("a")
    #print(soup.select("h1"))

    #print(r.headers)
    #print(r.content)


    notion_url = 'https://api.notion.com/v1/pages'

    api_key = main_local.api_key
    databaseid = main_local.databaseid
    title = all_list[0].title
    tag_name = all_list[0].tag

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
                ],
            },
            "レーベル": {
                "multi_select": [
                    {
                        "name": tag_name
                    }
                ]
            }
        }
    }

    response = requests.post(notion_url, json=payload, headers=headers)

    #result_dict = response.json()
    #result = result
    
    
    
    
if __name__ == "__main__":
    main()