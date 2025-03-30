import azure.functions as func
import datetime
import json
import logging
import requests
import time

from utils import (environment,
    log_level,
    storage_book_list_path,
    storage_bucket,
)
print(environment, log_level, storage_book_list_path, storage_bucket)

app = func.FunctionApp()

@app.route(route="HttpExampleFunc", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExampleFunc(req: func.HttpRequest) -> func.HttpResponse:
    print(f"IPアドレス: {requests.get('https://ifconfig.me').text}")
    logging.info('Python HTTP trigger function processed a request.')

    # 特定のWebサイトにアクセス
    url = "https://dengekibunko.jp/product/newrelease-bunko.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
        "Cache-Control": "no-cache",
    }
    time.sleep(3)
    response = requests.get(url, headers=headers)
    print(f"Scraping URL: {url}")
    print(f"Status code: {response.status_code}")
    print(f"Headers: {response.headers}")


    url = "https://mfbunkoj.jp/product/new-release.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
        "Cache-Control": "no-cache",
    }
    time.sleep(3)
    response = requests.get(url, headers=headers)
    print(f"Scraping URL: {url}")
    print(f"Status code: {response.status_code}")
    print(f"Headers: {response.headers}")

    url = "https://sneakerbunko.jp/product/2025/04/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
        "Cache-Control": "no-cache",
    }
    time.sleep(3)
    response = requests.get(url, headers=headers)
    print(f"Scraping URL: {url}")
    print(f"Status code: {response.status_code}")
    print(f"Headers: {response.headers}")



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
