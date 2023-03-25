#Notionに追加したのが結構前のやつは削除する。
import json
import requests
import re
import time

import main_local


def main():
    #まずは条件に合致する（この場合は古い情報）要素だけをNotionのDBから抜き出す。
    notion_url_db = main_local.notionurldb
    #current_db = get_current(notion_url_db)
    
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
                "property": "作成日時",
                    "date": {
                        "equals": "2023-03-25"
                    }
                #"property": "追ってる",
                #    "checkbox": {
                #        "equals": False
                #    },
        },
    }
    
    payload1 = {
        "filter": {
            "and": [
                {
                    "property": "作成日時",
                    "date": {
                        "equals": "2023-03-25"
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

    response = requests.request('POST', url=notion_url_db, json = payload1, headers=headers)
    
    
    #ここは内容を出力するためだけ。後で消す
    f = open('Tests/notiondb.txt', 'w')
    f.write(response.text)
    f.close()
    #print(response.text)
    #ここまで内容の出力
    
    #これで作成日が古すぎる項目のページIDを取得できる。
    result = re.findall(r'"page","id":"(.*?)"', response.text)
    f = open('Tests/notiondb2.txt', 'w')
    for i in result:
        f.write(i)
        f.write("\n")
    f.close()
    #print(result)
    
    
    
    payload_del = {
        "archived": True
    }
    
    for page_id in result:
        time.sleep(0.5)
        notion_url_page = "https://api.notion.com/v1/pages/" + page_id
        response = requests.request('PATCH', url=notion_url_page, json = payload_del, headers=headers)
    
    
    
if __name__ == "__main__":
    main()