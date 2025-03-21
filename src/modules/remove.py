# Notionに追加したのが結構前のやつは削除する。
import datetime
import os
import re
import time

import requests

from utils import environment


def delete_old_pages():
    # この日付より前のメモを消す
    today = datetime.date.today()
    two_month_ago = today - datetime.timedelta(days=60)
    delete_limit_date = str(two_month_ago)

    # まずは条件に合致する（この場合は古い情報）要素だけをNotionのDBから抜き出す。
    if environment == "local":
        import main_local

        api_key = main_local.api_key
        notion_url_db = main_local.notionurldb
    else:
        api_key = os.environ.get("NotionAPIKey")
        notion_database_id = os.environ.get("NotionDatabaseID")
        notion_url_db = (
            f"https://api.notion.com/v1/databases/{notion_database_id}/query"
        )

    # ヘッダー。これは固定
    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    # 抜き出す情報のフィルターをかける
    payload = {
        "filter": {
            "and": [
                {
                    "property": "作成日時",
                    "date": {"before": delete_limit_date},
                },
                {"property": "追ってる", "checkbox": {"equals": False}},
            ]
        }
    }

    response = requests.request(
        "POST", url=notion_url_db, json=payload, headers=headers
    )
    print(response.status_code)
    if response.status_code != 200:
        print("Error: ", response.text)
        return

    # これで作成日が古すぎる項目のページIDを取得できる。
    result = re.findall(r'"page","id":"(.*?)"', response.text)

    # NotionAPIで、ページを削除するJSON
    payload_del = {"in_trash": True}

    for page_id in result:
        time.sleep(0.8)
        notion_url_page = "https://api.notion.com/v1/pages/" + page_id
        response = requests.request(
            "PATCH", url=notion_url_page, json=payload_del, headers=headers
        )
