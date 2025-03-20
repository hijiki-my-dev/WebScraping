# NotionのAPIキーやデータベースIDはローカルだけに載せる。

import requests
from bs4 import BeautifulSoup
import time
import json
import datetime
import re
import os
from dataclasses import dataclass
from logging import DEBUG, ERROR

from modules import delete_old_pages, NotionClient
from utils import booklist, Logger, log_level, request_error_mail

logger = Logger(log_level=log_level)



# TODO: requestsエラーの検出やメール送信、デバッグなどをutilsにまとめる。クラス化はしなくても良さそう


@dataclass
class book_info:
    title: str
    tag: str
    date: str


# ガガガ文庫用。"8月刊は8月18日発売予定"の形式で文字列を受け取って、2023-08-18などを返す。
def set_date_gagaga(date_origin):
    d_list = list(date_origin)
    del d_list[0:4]
    if d_list[1] == "月":
        d_list.insert(0, "0")

    # 1月に発売する時は来年になる可能性があることに注意して、発売する年を最初につける。
    # 発売する月、今の年月を取得
    dt_now = datetime.datetime.now()
    dt_year = dt_now.year

    # 1月発売の場合、今12月なら発売日は来年
    if (d_list[0] == "0") & (d_list[1] == "1"):
        dt_month = dt_now.month
        if dt_month == 12:
            dt_year += 1

    # ["y", "y", "y", "y", "-"]の形式のリストを作成
    d_list_year = list(str(dt_year) + "-")
    d_list_year.extend(d_list)

    # yyyy-mm-ddの形式の文字列にする。
    d = "".join(d_list_year)
    d = d.replace("月", "-")
    d = d.replace("日発売予定", "")

    return d

# スクレイピングの部分
def dengeki(all_list):
    # 電撃文庫の今月と来月発売の作品タイトルと発売日を抜粋
    # タイトルと発売日を順番に表示するにはループを使う。elmsは配列だから、それで回す。
    url = "https://dengekibunko.jp/product/newrelease-bunko.html"

    # リクエストの前には必ずsleepを入れる。
    time.sleep(1)
    r = requests.get(url)
    if r.status_code != 200:
        request_error_mail("電撃文庫", r.status_code)
        return

    soup = BeautifulSoup(r.content, "html.parser")

    elms = soup.select(".p-books-media__title > a")
    tag = "電撃"

    # dateをISO8601に合わせる。まずは発売日の文字列をfind_allしてくる。
    date_elms = soup.find_all("td", string=re.compile("日発売"))
    date_iso_list = []
    for elm in date_elms:
        d = elm.text
        d_list = list(d)
        if d_list[6] == "月":
            d_list.insert(5, "0")
        if d_list[9] == "日":
            d_list.insert(8, "0")

        d = "".join(d_list)

        d = d.replace("年", "-")
        d = d.replace("月", "-")
        d = d.replace("日発売", "")

        date_iso_list.append(d)

    # スマホ用とPC用で、要素が重複。インデックスが奇数のものを削除。
    del date_iso_list[1::2]

    # 各作品のタイトルと発売日とレーベルを変数とするインスタンスのリストを生成。
    for i in range(len(elms)):
        cl = book_info(elms[i].text, tag, date_iso_list[i])
        all_list.append(cl)

    return all_list


def mf(all_list):
    url = "https://mfbunkoj.jp/product/new-release.html"

    time.sleep(1)
    r = requests.get(url)
    if r.status_code != 200:
        request_error_mail("MF文庫J", r.status_code)
        return

    soup = BeautifulSoup(r.content, "html.parser")

    elms = soup.select(".detail > h2 > a")
    tag = "MF"

    date_elms = soup.find_all("p", string=re.compile("発売日"))
    date_iso_list = []
    for elm in date_elms:
        d = elm.text
        d_list = list(d)
        if d_list[10] == "月":
            d_list.insert(9, "0")
        if d_list[13] == "日":
            d_list.insert(12, "0")

        d = "".join(d_list)

        d = d.replace("発売日：", "")
        d = d.replace("年", "-")
        d = d.replace("月", "-")
        d = d.replace("日", "")

        date_iso_list.append(d)

    for i in range(len(elms)):
        cl = book_info(elms[i].text, tag, date_iso_list[i])
        all_list.append(cl)

    return all_list


def gagaga(all_list):
    url = "https://gagagabunko.jp/release/index.html"

    time.sleep(1)
    r = requests.get(url)
    if r.status_code != 200:
        request_error_mail("ガガガ文庫", r.status_code)
        return

    soup = BeautifulSoup(r.content, "html.parser")

    elms = soup.select(".content > #title > h3")
    tag = "ガガガ"

    date_origin = soup.select(".heading > .headingReleasedate")
    date = set_date_gagaga(date_origin[0].text)

    for i in range(len(elms)):
        cl = book_info(elms[i].text, tag, date)
        all_list.append(cl)
    return all_list


def fantasia(all_list):
    url = "https://fantasiabunko.jp/product/"

    time.sleep(1)
    r = requests.get(url)
    if r.status_code != 200:
        request_error_mail("ファンタジア文庫", r.status_code)
        return

    soup = BeautifulSoup(r.content, "html.parser")

    elms = soup.select(".detail > .head > h3 > a")
    tag = "ファンタジア"

    date_elms = soup.find_all("p", string=re.compile("発売日"))
    date_iso_list = []
    for elm in date_elms:
        d = elm.text
        d_list = list(d)
        if d_list[10] == "月":
            d_list.insert(9, "0")
        if d_list[13] == "日":
            d_list.insert(12, "0")

        d = "".join(d_list)

        d = d.replace("発売日：", "")
        d = d.replace("年", "-")
        d = d.replace("月", "-")
        d = d.replace("日", "")

        date_iso_list.append(d)

    for i in range(len(elms)):
        cl = book_info(elms[i].text, tag, date_iso_list[i])
        all_list.append(cl)

    return all_list


def ga(all_list):
    url1 = "https://ga.sbcr.jp/release/month_current/"
    url2 = "https://ga.sbcr.jp/release/month_next/"

    time.sleep(1)
    r1 = requests.get(url1)
    time.sleep(1)
    r2 = requests.get(url2)
    if (r1.status_code != 200) or (r2.status_code != 200):
        request_error_mail("GA文庫", r1.status_code)
        request_error_mail("GA文庫", r2.status_code)
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
        if dt_now.month < 9:
            next_month = "0" + str(dt_now.month + 1)
        else:
            next_month = str(dt_now.month + 1)
        d_today[5], d_today[6] = next_month[0], next_month[1]
        d_today[8], d_today[9] = "1", "5"
        date2 = "".join(d_today)

    tag = "GA"

    for i in range(len(elms1)):
        cl1 = book_info(elms1[i].text, tag, date1)
        all_list.append(cl1)
    for i in range(len(elms2)):
        cl2 = book_info(elms2[i].text, tag, date2)
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
        if dt_now.month < 9:
            next_month = "0" + str(dt_now.month + 1)
        else:
            next_month = str(dt_now.month + 1)

    url1 = "https://sneakerbunko.jp/product/" + today[0:4] + "/" + today[5:7]
    url2 = "https://sneakerbunko.jp/product/" + year + "/" + next_month

    time.sleep(1)
    r1 = requests.get(url1)
    time.sleep(1)
    r2 = requests.get(url2)
    if (r1.status_code != 200) or (r2.status_code != 200):
        request_error_mail("スニーカー文庫", r1.status_code)
        request_error_mail("スニーカー文庫", r2.status_code)
        return

    soup1 = BeautifulSoup(r1.content, "html.parser")
    soup2 = BeautifulSoup(r2.content, "html.parser")

    elms1 = soup1.select(".c-thumbnail-book__title > a")
    elms2 = soup2.select(".c-thumbnail-book__title > a")

    # 今月の発売日
    date1 = list(today)
    date1[-2], date1[-1] = "0", "1"
    date1 = "".join(date1)

    # 来月の発売日
    date2 = year + "-" + next_month + "-" + "01"

    tag = "スニーカー"

    for i in range(len(elms1)):
        cl1 = book_info(elms1[i].text, tag, date1)
        all_list.append(cl1)
    for i in range(len(elms2)):
        cl2 = book_info(elms2[i].text, tag, date2)
        all_list.append(cl2)

    return all_list


def main():
    all_list = []
    # all_list = dengeki(all_list)
    # all_list = mf(all_list)
    # all_list = gagaga(all_list)
    # all_list = fantasia(all_list)
    # all_list = ga(all_list)
    # all_list = sneaker(all_list)

    # 現在のデータベース情報を取得
    notion_client = NotionClient()
    current_db = notion_client.get_current_pages()

    # for i in range(len(all_list)):
    #     # 既存のデータベースに含まれている場合はスキップ
    #     if all_list[i].title in current_db:
    #         continue
    #     else:
    #         check_flag = 0
    #         for book in booklist:
    #             if book in all_list[i].title:
    #                 check_flag = 1
    #                 break
    #         time.sleep(0.5)
    #         notion_client.add_to_notion(all_list[i].title, all_list[i].tag, all_list[i].date, check_flag)


if __name__ == "__main__":
    # delete_old_pages()
    # time.sleep(10)
    main()
