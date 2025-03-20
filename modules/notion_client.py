import os
import time
import requests
import main_local
from utils import Logger, log_level

logger = Logger(log_level=log_level)


class NotionClient:
    def __init__(self):
        # self.notion_api_key = os.environ.get("NotionAPIKey")
        # self.notion_database_id = os.environ.get("NotionDatabaseID")
        self.notion_api_key = main_local.api_key
        self.notion_database_id = main_local.databaseid
        self.notion_url = f"https://api.notion.com/v1/databases/{self.notion_database_id}/query"

        self.headers = {
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.notion_api_key,
        }

    def get_current_pages(self) -> str:
        params = {"page_size": 100}
        time.sleep(1)
        response = requests.request("POST", url=self.notion_url, headers=self.headers)

        logger.debug(f"In NotionClient.get_current_pages status code: {response.status_code}")

        # 最初100個のレスポンスを文字列として格納する。この後、ループで追加していく。
        response_text = response.text

        if response.ok:
            search_response_obj = response.json()
            pages_and_databases = search_response_obj.get("results")

            while search_response_obj.get("has_more"):
                params["start_cursor"] = search_response_obj.get("next_cursor")
                time.sleep(1)
                response = requests.request("POST", url=self.notion_url, json=params, headers=self.headers)
                response_text += response.text
                if response.ok:
                    search_response_obj = response.json()
                    pages_and_databases.extend(search_response_obj.get("results"))

        return response_text

    def add_to_notion(self, title: str, tag: str, date: str, checkbox_flg: int = 0):
        notion_url = "https://api.notion.com/v1/pages"

        payload = {
            "parent": {"database_id": self.notion_database_id},
            "properties": {
                "名前": {
                    "title": [{"text": {"content": title}}],
                },
                "レーベル": {
                    "multi_select": [{"name": tag}],
                },
                "発売日": {"date": {"start": date}},
                "追ってる": {"checkbox": bool(checkbox_flg)},
            },
        }

        response = requests.request("POST", url=notion_url, json=payload, headers=self.headers)
        logger.debug(f"In NotionClient.add_to_notion status code: {response.status_code}")
        if response.status_code != 200:
            # メールでエラー通知
            pass