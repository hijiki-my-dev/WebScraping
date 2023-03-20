#NotionのAPIキーやデータベースIDはローカルだけに載せる。

import requests
from bs4 import BeautifulSoup
import time
import json
import datetime
import re

#import module
import main_local


class label:
    def __init__(self, title_name, date_caractor, tag_name):
        self.title = title_name
        self.date = date_caractor
        self.tag = tag_name
    

def dengeki(all_list):
    #電撃文庫の今月と来月発売の作品タイトルと発売日を抜粋
    #タイトルと発売日を順番に表示するにはループを使う。elmsは配列だから、それで回す。
    url = "https://dengekibunko.jp/product/newrelease-bunko.html"

    #リクエストの前には必ずsleepを入れる。
    time.sleep(1)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")
    
    elms = soup.select(".p-books-media__title > a")
    tag = "電撃"
    
    #dateをISO8601に合わせる。まずは発売日の文字列をfind_allしてくる。
    date_elms = soup.find_all("td", text=re.compile("日発売"))
    date_iso_list = []
    for elm in date_elms:
        d = elm.text
        d_list = list(d)
        if d_list[6] == "月":
            d_list.insert(5 ,"0")
        if d_list[9] == "日":
            d_list.insert(8, "0")
            
        d = ''.join(d_list)
        
        d = d.replace("年", "-")
        d = d.replace("月", "-")
        d = d.replace("日発売", "")
        
        date_iso_list.append(d)
        
    #スマホ用とPC用で、要素が重複。インデックスが奇数のものを削除。
    del date_iso_list[1::2]
    
    #各作品のタイトルと発売日とレーベルを変数とするインスタンスのリストを生成。
    for i in range(len(elms)):
        cl = label(elms[i].text, date_iso_list[i], tag)
        all_list.append(cl)
        
    return all_list


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
    date = all_list[0].date

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
                ],
            },
            "発売日": {
                "date": {
                    "start": date
                    #"end": null
                }
            },
        }
    }

    response = requests.post(notion_url, json=payload, headers=headers)

    #result_dict = response.json()
    #result = result
    
    
    
    
if __name__ == "__main__":
    main()