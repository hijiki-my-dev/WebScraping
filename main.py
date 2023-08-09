#NotionのAPIキーやデータベースIDはローカルだけに載せる。

import requests
from bs4 import BeautifulSoup
import time
import json
import datetime
import re

#import module
import main_local
import booklist
import remove
import error_mail

class label:
    def __init__(self, title_name, date_caractor, tag_name):
        self.title = title_name
        self.date = date_caractor
        self.tag = tag_name

#デバッグ用の関数。引数に文字列を指定するとTestsディレクトリ（ローカルのみ）内にファイルを作成。
def debug_file(s):
    path = 'Tests/output.txt'
    with open(path, mode='w') as f:
        f.write(s)
        
#リクエストエラーが発生した際にメールを送る
def request_error_mail(error_point, status_code):
    message="スクレイピングプログラムの" + error_point + "でリクエスト時にエラーが発生した可能性があります。HTTPステータスコードは" + str(status_code) + "です。"
    error_mail.main(message)

#引数はint
#def set_date(sale_day):
#    dt_now = datetime.datetime.now()
#    date = ""
#    today = dt_now.day
#    
#    sale_day_str = str(sale_day)
#    
#    #ISO形式（2023-03-22など）の一文字ずつをリストに格納
#    d_today = list(str(datetime.date.today()))
#    if today < sale_day:
#        d_today[8], d_today[9] = sale_day_str[0], sale_day_str[1]
#        date =  "".join(d_today)
#    else:
#        if dt_now.month == 12:
#            next_year = str(dt_now.year + 1)
#            date = next_year + "-01-" + sale_day_str
#        else:
#            next_month = ""
#            if dt_now.month < 9 :
#                next_month = "0" + str(dt_now.month + 1)
#            else:
#                next_month = str(dt_now.month + 1)
#            d_today[5], d_today[6] = next_month[0], next_month[1]
#            d_today[8], d_today[9] = sale_day_str[0], sale_day_str[1]
#            date =  "".join(d_today)
#    
#    return date

#ガガガ文庫用。"8月刊は8月18日発売予定"の形式で文字列を受け取って、2023-08-18などを返す。
def set_date_gagaga(date_origin):
    d_list = list(date_origin)
    del d_list[0:4]
    if d_list[1] == "月":
        d_list.insert(0, "0")
    
    #1月に発売する時は来年になる可能性があることに注意して、発売する年を最初につける。
    #発売する月、今の年月を取得
    dt_now = datetime.datetime.now()
    dt_year = dt_now.year
    
    #1月発売の場合、今12月なら発売日は来年
    if (d_list[0]=="0") & (d_list[1]=="1"):
        dt_month = dt_now.month
        if dt_month == 12:
            dt_year += 1

    #["y", "y", "y", "y", "-"]の形式のリストを作成
    d_list_year = list(str(dt_year) + "-")
    print(d_list_year, d_list)
    d_list_year.extend(d_list)
    print(d_list_year)
    
    #yyyy-mm-ddの形式の文字列にする。
    d = ''.join(d_list_year)
    d = d.replace("月", "-")
    d = d.replace("日発売予定", "")
    
    return d
            
        
#現在のデータベースに含まれるページ情報を取得して文字列を返す。        
def get_current(url):
    api_key = main_local.api_key

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    
    params = {"page_size": 100} 

    response = requests.request('POST', url=url, headers=headers)
    #最初100個のレスポンスを文字列として格納する。この後、ループで追加していく。
    response_text = response.text
    
    if response.ok:
        search_response_obj = response.json()		
        pages_and_databases = search_response_obj.get("results")

        while search_response_obj.get("has_more"):
            params["start_cursor"] = search_response_obj.get("next_cursor")
            
            response = requests.post(url, json=params, headers=headers)
            response_text += response.text
            if response.ok:
                search_response_obj = response.json()
                pages_and_databases.extend(search_response_obj.get("results"))

    
    return response_text

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

#追っている作品or興味のある作品にはチェックをつける
def add_notion_checkbox(title, tag, date):
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
            "追ってる":{
                "checkbox": True
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
    if r.status_code != 200:
        request_error_mail("電撃文庫", r.status_code)
        return

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
    if r.status_code != 200:
        request_error_mail("MF文庫J", r.status_code)
        return
    
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
    if r.status_code != 200:
        request_error_mail("ガガガ文庫", r.status_code)
        return
    
    soup = BeautifulSoup(r.content, "html.parser")
    
    elms = soup.select(".content > #title > h3")
    tag = "ガガガ"
    #date = set_date(18)
    
    date_origin = soup.select(".heading > .headingReleasedate")
    date = set_date_gagaga(date_origin[0].text)
    
    for i in range(len(elms)):
        cl = label(elms[i].text, date, tag)
        all_list.append(cl)
    return all_list

def fantasia(all_list):
    url = "https://fantasiabunko.jp/product/"
    
    time.sleep(5)
    r = requests.get(url)
    if r.status_code != 200:
        request_error_mail("ファンタジア文庫", r.status_code)
        return
    
    soup = BeautifulSoup(r.content, "html.parser")
    
    elms = soup.select(".detail > .head > h3 > a")
    tag = "ファンタジア"
    
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

def ga(all_list):
    url1 = "https://ga.sbcr.jp/release/month_current/"
    url2 = "https://ga.sbcr.jp/release/month_next/"
    
    time.sleep(5)
    r1 = requests.get(url1)
    time.sleep(5)
    r2 = requests.get(url2)
    if (r1.status_code != 200) or (r2.status_code != 200):
        request_error_mail("GA文庫", r.status_code)
        return
    
    soup1 = BeautifulSoup(r1.content, "html.parser")
    soup2 = BeautifulSoup(r2.content, "html.parser")
    
    elms1 = soup1.select(".newBook_gaBunko_wrap .title_area > .title > a > span")
    elms2 = soup2.select(".newBook_gaBunko_wrap .title_area > .title > a > span")
    
    del elms1[1::2]
    del elms2[1::2]
    
    date1 = list(str(datetime.date.today()))
    date1[-2], date1[-1] = "1", "5"
    date1 = "".join(date1)
    
    d_today = list(str(datetime.date.today()))
    date2 = ""    
    dt_now = datetime.datetime.now()
    if dt_now.month == 12:
        next_year = str(dt_now.year + 1)
        date2 = next_year + "-01-" + "15"
    else:
        next_month = ""
        if dt_now.month < 9 :
            next_month = "0" + str(dt_now.month + 1)
        else:
            next_month = str(dt_now.month + 1)
        d_today[5], d_today[6] = next_month[0], next_month[1]
        d_today[8], d_today[9] = "1", "5"
        date2 =  "".join(d_today)
    
    tag = "GA"
    
    for i in range(len(elms1)):
        cl1 = label(elms1[i].text, date1, tag)
        all_list.append(cl1)
    for i in range(len(elms2)):
        cl2 = label(elms2[i].text, date2, tag)
        all_list.append(cl2)
        
    return all_list

def sneaker(all_list):
    dt_now = datetime.datetime.now()
    today = str(datetime.date.today())
    year = str(dt_now.year)
    next_month = "01"
    if dt_now.month == 12:
        year = str(dt_now.year + 1)

    else:
        if dt_now.month < 9 :
            next_month = "0" + str(dt_now.month + 1)
        else:
            next_month = str(dt_now.month + 1)
        
    url1 = "https://sneakerbunko.jp/product/" + today[0:4] + "/" + today[5:7]
    url2 = "https://sneakerbunko.jp/product/" + year + "/" + next_month
    
    time.sleep(5)
    r1 = requests.get(url1)
    time.sleep(5)
    r2 = requests.get(url2)
    if (r1.status_code != 200) or (r2.status_code != 200):
        request_error_mail("スニーカー文庫", r.status_code)
        return    
    
    soup1 = BeautifulSoup(r1.content, "html.parser")
    soup2 = BeautifulSoup(r2.content, "html.parser")
    
    elms1 = soup1.select(".c-thumbnail-book__title > a")
    elms2 = soup2.select(".c-thumbnail-book__title > a")
    
    #今月の発売日
    date1 = list(today)
    date1[-2], date1[-1] = "0", "1"
    date1 = "".join(date1)
    
    #来月の発売日
    date2 = year + "-" + next_month + "-" + "01"     
    
    tag = "スニーカー"
    
    for i in range(len(elms1)):
        cl1 = label(elms1[i].text, date1, tag)
        all_list.append(cl1)
    for i in range(len(elms2)):
        cl2 = label(elms2[i].text, date2, tag)
        all_list.append(cl2)
        
    return all_list

def main():
    all_list = []
    all_list = dengeki(all_list)
    #all_list = mf(all_list)
    #all_list = gagaga(all_list)
    #all_list = fantasia(all_list)
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
            check_flag = 0
            for book in booklist.l:
                if book in all_list[i].title:
                    time.sleep(0.5)    
                    add_notion_checkbox(all_list[i].title, all_list[i].tag, all_list[i].date)
                    check_flag = 1
                    break
                
            if check_flag == 0:
                time.sleep(0.5)
                add_notion(all_list[i].title, all_list[i].tag, all_list[i].date)
                
    
if __name__ == "__main__":
    #remove.main()
    time.sleep(10)
    main()