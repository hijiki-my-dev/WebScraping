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
        
#現在のデータベースに含まれるページ情報を取得して文字列を返す。        
def get_current(url):
    api_key = main_local.api_key
    databaseid = main_local.databaseid

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.request('POST', url=url, headers=headers)
    
    return response.text

#指定された引数を元にNotionに追加する。        
def add_notion(title, tag, date):
    notion_url = 'https://api.notion.com/v1/pages'

    api_key = main_local.api_key
    databaseid = main_local.databaseid
    
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
                        "name": tag
                    }
                ],
            },
            "発売日": {
                "date": {
                    "start": date
                }
            },
        }
    }

    response = requests.post(notion_url, json=payload, headers=headers)
    
    
#スクレイピングの部分
def dengeki(all_list):
    #電撃文庫の今月と来月発売の作品タイトルと発売日を抜粋
    #タイトルと発売日を順番に表示するにはループを使う。elmsは配列だから、それで回す。
    url = "https://dengekibunko.jp/product/newrelease-bunko.html"

    #リクエストの前には必ずsleepを入れる。
    time.sleep(5)
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

def mf(all_list):
    url = "https://mfbunkoj.jp/product/new-release.html"
    
    time.sleep(5)
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, "html.parser")
    
    elms = soup.select(".detail > h2 > a")
    tag = "MF"
    
    date_elms = soup.find_all("p", text = re.compile("発売日"))
    date_iso_list = []
    for elm in date_elms:
        d = elm.text
        d_list = list(d)
        if d_list[10] == "月":
            d_list.insert(9, "0")
        if d_list[13] == "日":
            d_list.insert(12, "0")
            
        d = ''.join(d_list)
        
        d = d.replace("発売日：", "")
        d = d.replace("年", "-")
        d = d.replace("月", "-")
        d = d.replace("日", "")
        
        date_iso_list.append(d)
        
    for i in range(len(elms)):
        cl = label(elms[i].text, date_iso_list[i], tag)
        all_list.append(cl)
            
    return all_list

def gagaga(all_list):
    url = "https://gagagabunko.jp/release/index.html"
    
    time.sleep(5)
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, "html.parser")
    
    elms = soup.select(".content > #title > h3")
    tag = "ガガガ"
    
    dt_now = datetime.datetime.now()
    date = ""
    today = dt_now.day
    
    #ISO形式（2023-03-22など）の一文字ずつをリストに格納
    d_today = list(str(datetime.date.today()))
    if today < 18:
        d_today[8], d_today[9] = "1", "8"
        date =  "".join(d_today)
    else:
        if dt_now.month == 12:
            next_year = str(dt_now.year + 1)
            date = next_year + "-01-18"
        else:
            next_month = ""
            if dt_now.month < 9 :
                next_month = "0" + str(dt_now.month + 1)
            else:
                next_month = str(dt_now.month + 1)
            d_today[5], d_today[6] = next_month[0], next_month[1]
            d_today[8], d_today[9] = "1", "8"
            date =  "".join(d_today)
    
    for i in range(len(elms)):
        cl = label(elms[i].text, date, tag)
        all_list.append(cl)
    return all_list

def main():
    all_list = []
    #all_list = dengeki(all_list)
    #all_list = mf(all_list)
    all_list = gagaga(all_list)
    #all_list = fanta(all_list)
    #all_list = ga(all_list)
    #all_list = sneaker(all_list)
    
    
    #現在のデータベースの状況を取得。タイトルなども取得できる。
    notion_url_db = main_local.notionurldb
    current_db = get_current(notion_url_db)

    for i in range(len(all_list)):
        #重複の除外
        if all_list[i].title in current_db:
            continue
        else:
            add_notion(all_list[i].title, all_list[i].tag, all_list[i].date)


    
    
    
if __name__ == "__main__":
    d_today = str(datetime.date.today())

    #print(d_today)
    
    main()