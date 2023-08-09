#Notionに追加したのが結構前のやつは削除する。
import json
import requests
import re
import time
import datetime

import main_local


def main():
    #この日付より前のメモを消すことにする。
    today = datetime.date.today()
    three_month_ago = today - datetime.timedelta(days=90)
    delete_limit_date = str(three_month_ago)
    
    #delete_limit_date = "2023-06-12"
            
    #まずは条件に合致する（この場合は古い情報）要素だけをNotionのDBから抜き出す。
    notion_url_db = main_local.notionurldb
    
    api_key = main_local.api_key
    databaseid = main_local.databaseid

    #ヘッダー。これは固定
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    
    #抜き出す情報のフィルターをかける
    payload = {
        "filter": {
            "and": [
                {
                    "property": "作成日時",
                    "date": {
                        "before": delete_limit_date
                    }
                },
                {
                    "property": "追ってる",
                    "checkbox": {
                        "equals": False
                        }
                }
            ]
        }
    }

    response = requests.request('POST', url=notion_url_db, json = payload, headers=headers)
    
    #これで作成日が古すぎる項目のページIDを取得できる。
    result = re.findall(r'"page","id":"(.*?)"', response.text)
    
    #NotionAPIで、ページを削除するJSON
    payload_del = {
        "archived": True
    }
    
    for page_id in result:
        time.sleep(0.8)
        notion_url_page = "https://api.notion.com/v1/pages/" + page_id
        response = requests.request('PATCH', url=notion_url_page, json = payload_del, headers=headers)
        
#main()