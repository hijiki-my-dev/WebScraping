import azure.functions as func
import datetime
import json
import logging
import requests
import time

from utils import (environment,
    log_level,
    storage_book_list_path,
    storage_container,
)

from job import run
from modules import delete_old_pages
# print(environment, log_level, storage_book_list_path, storage_container)

app = func.FunctionApp()

@app.route(route="HttpExampleFunc", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExampleFunc(req: func.HttpRequest) -> func.HttpResponse:
    print(f"IPアドレス: {requests.get('https://ifconfig.me').text}")
    logging.info('Python HTTP trigger function processed a request.')

    delete_old_pages()
    time.sleep(3)
    run()

    # 特定のWebサイトにアクセス
    url = "https://dengekibunko.jp/product/newrelease-bunko.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
        "Cache-Control": "no-cache",
    }
    time.sleep(3)
    response = requests.get(url, headers=headers)
    print(f"スクレイピングURL: {url}")
    print(f"ステータスコード: {response.status_code}")
    print(f"ヘッダー: {response.headers}")


    url = "https://fantasiabunko.jp/product/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
        "Cache-Control": "no-cache",
    }
    time.sleep(3)
    response = requests.get(url, headers=headers)
    print(f"スクレイピングURL: {url}")
    print(f"ステータスコード: {response.status_code}")
    print(f"ヘッダー: {response.headers}")

    url = "https://sneakerbunko.jp/product/2025/04/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
        "Cache-Control": "no-cache",
    }
    time.sleep(3)
    response = requests.get(url, headers=headers)
    print(f"スクレイピングURL: {url}")
    print(f"ステータスコード: {response.status_code}")
    print(f"ヘッダー: {response.headers}")

    url = "https://ga.sbcr.jp/release/month_current/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
        "Cache-Control": "no-cache",
    }
    time.sleep(3)
    response = requests.get(url, headers=headers)
    print(f"スクレイピングURL: {url}")
    print(f"ステータスコード: {response.status_code}")
    print(f"ヘッダー: {response.headers}")





    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
