import datetime
import re
import time
from dataclasses import dataclass

import bs4
import requests
from bs4 import BeautifulSoup

from src.utils import Logger, log_level, request_error_mail

logger = Logger(log_level=log_level)
time.sleep(1)
ip_address = requests.get("https://ifconfig.me").text
logger.debug(f"IPアドレス: {ip_address}")

@dataclass
class BookInfo:
    title: str
    tag: str
    date: str


class BaseScraper:
    def __init__(self, urls: list[str]):
        self.urls = urls
        self.date = None

    def get_soup(self, url: str) -> BeautifulSoup:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
            "Cache-Control": "no-cache",
        }
        time.sleep(3)
        r = requests.get(url, headers=headers)
        logger.debug(f"Scraping URL: {url}")
        logger.debug(f"Status code: {r.status_code}")
        logger.debug(f"Headers: {r.headers}")
        if r.status_code != 200:
            request_error_mail(self.tag, r.status_code)
            return
        soup = BeautifulSoup(r.content, "html.parser")
        return soup

    def set_book_info(
        self, elms: bs4.element.ResultSet, dates: list[str]
    ) -> list[BookInfo]:
        book_list = []
        for elm, date in zip(elms, dates):
            book = BookInfo(elm.text, self.tag, date)
            book_list.append(book)
        return book_list


class DengekiScraper(BaseScraper):
    def __init__(self):
        urls = ["https://dengekibunko.jp/product/newrelease-bunko.html"]
        super().__init__(urls)
        self.tag = "電撃"

    def scrape(self) -> list[BookInfo]:
        logger.info("Start scraping Dengeki Bunko")
        soup = self.get_soup(self.urls[0])
        elms = soup.select(".p-books-media__title > a")
        date_elms = soup.find_all("td", string=re.compile("日発売"))
        date_iso_list = []
        for elm in date_elms:
            date_list = list(elm.text)
            if date_list[6] == "月":
                date_list.insert(5, "0")
            if date_list[9] == "日":
                date_list.insert(8, "0")

            d = "".join(date_list)
            d = d.replace("年", "-")
            d = d.replace("月", "-")
            d = d.replace("日発売", "")
            logger.debug(f"Date for Dengeki: {d}")

            date_iso_list.append(d)

        # スマホ用とPC用で、要素が重複。インデックスが奇数のものを削除。
        del date_iso_list[1::2]
        return self.set_book_info(elms, date_iso_list)


class MfScraper(BaseScraper):
    def __init__(self):
        urls = ["https://mfbunkoj.jp/product/new-release.html"]
        super().__init__(urls)
        self.tag = "MF"

    def scrape(self) -> list[BookInfo]:
        logger.info("Start scraping MF Bunko")
        soup = self.get_soup(self.urls[0])
        elms = soup.select(".detail > h2 > a")
        date_elms = soup.find_all("p", string=re.compile("発売日"))
        date_iso_list = []
        for elm in date_elms:
            date_list = list(elm.text)[4:]
            if date_list[6] == "月":
                date_list.insert(5, "0")
            if date_list[9] == "日":
                date_list.insert(8, "0")

            d = "".join(date_list[:11])
            d = d.replace("年", "-")
            d = d.replace("月", "-")
            d = d.replace("日", "")
            logger.debug(f"Date for MF: {d}")

            date_iso_list.append(d)

        return self.set_book_info(elms, date_iso_list)


class GagagaScraper(BaseScraper):
    def __init__(self):
        urls = ["https://gagagabunko.jp/release/index.html"]
        super().__init__(urls)
        self.tag = "ガガガ"

    def set_date(self, date_origin: str) -> str:
        logger.info("Start scraping Gagaga Bunko")
        date_list = list(date_origin.replace("日発売予定", ""))[-5:]
        if not date_list[1].isdecimal():
            # 発売日の記載形式の変更。エラーメールを通知
            pass
        elif date_list[0] == "は":
            date_list[0] = "0"

        dt_now = datetime.datetime.now()
        dt_year = dt_now.year

        if (date_list[0] == "0") & (date_list[1] == "1"):
            dt_month = dt_now.month
            if dt_month == 11 or dt_month == 12:
                dt_year += 1

        # ["y", "y", "y", "y", "-"]の形式のリストを作成
        date_list_year = list(str(dt_year) + "-")
        date_list_year.extend(date_list)

        # yyyy-mm-ddの形式の文字列にする。
        d = "".join(date_list_year)
        d = d.replace("月", "-")
        return d

    def scrape(self) -> list[BookInfo]:
        soup = self.get_soup(self.urls[0])
        elms = soup.select(".content > #title > h3")
        date_origin = soup.select(".heading > .headingReleasedate2")
        date = self.set_date(date_origin[0].text)
        logger.debug(f"Date for Gagaga: {date}")
        return self.set_book_info(elms, [date] * len(elms))


class FantasiaScraper(BaseScraper):
    def __init__(self):
        urls = ["https://fantasiabunko.jp/product/"]
        super().__init__(urls)
        self.tag = "ファンタジア"

    def scrape(self) -> list[BookInfo]:
        logger.info("Start scraping Fantasia Bunko")
        soup = self.get_soup(self.urls[0])
        elms = soup.select(".detail > .head > h3 > a")
        date_elms = soup.find_all("p", string=re.compile("発売日"))
        date_iso_list = []
        for elm in date_elms:
            date_list = list(elm.text)
            if date_list[10] == "月":
                date_list.insert(9, "0")
            if date_list[13] == "日":
                date_list.insert(12, "0")

            d = "".join(date_list)
            d = d.replace("発売日：", "")
            d = d.replace("年", "-")
            d = d.replace("月", "-")
            d = d.replace("日", "")
            logger.debug(f"Date for Fantasia: {d}")

            date_iso_list.append(d)

        return self.set_book_info(elms, date_iso_list)


class GaScraper(BaseScraper):
    def __init__(self):
        urls = [
            "https://ga.sbcr.jp/release/month_current/",
            "https://ga.sbcr.jp/release/month_next/",
        ]
        super().__init__(urls)
        self.tag = "GA"

    def scrape(self) -> list[BookInfo]:
        logger.info("Start scraping GA Bunko")
        soup1 = self.get_soup(self.urls[0])
        soup2 = self.get_soup(self.urls[1])

        elms1 = soup1.select(".newBook_gaBunko_wrap .title_area > .title > a > span")
        elms2 = soup2.select(".newBook_gaBunko_wrap .title_area > .title > a > span")

        del elms1[1::2]
        del elms2[1::2]

        date1 = list(str(datetime.date.today()))
        date1[-2], date1[-1] = "1", "5"
        date1 = "".join(date1)
        logger.debug(f"Date for GA 1: {date1}")

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
        logger.debug(f"Date for GA 2: {date2}")

        book_list = self.set_book_info(elms1, [date1] * len(elms1))
        return book_list + self.set_book_info(elms2, [date2] * len(elms2))


class SneakerScraper(BaseScraper):
    def __init__(self):
        dt_now = datetime.datetime.now()
        self.today = str(datetime.date.today())
        self.year = str(dt_now.year)
        self.next_month = "01"
        if dt_now.month == 12:
            self.year = str(dt_now.year + 1)
        else:
            if dt_now.month < 9:
                self.next_month = "0" + str(dt_now.month + 1)
            else:
                self.next_month = str(dt_now.month + 1)

        urls = [
            "https://sneakerbunko.jp/product/"
            + self.today[0:4]
            + "/"
            + self.today[5:7]
            + "/",
            "https://sneakerbunko.jp/product/"
            + self.year
            + "/"
            + self.next_month
            + "/",
        ]
        super().__init__(urls)
        self.tag = "スニーカー"

    def scrape(self) -> list[BookInfo]:
        logger.info("Start scraping Sneaker Bunko")
        soup1 = self.get_soup(self.urls[0])
        soup2 = self.get_soup(self.urls[1])

        elms1 = soup1.select(".c-thumbnail-book__title > a")
        elms2 = soup2.select(".c-thumbnail-book__title > a")

        # 今月の発売日
        date1 = list(self.today)
        date1[-2], date1[-1] = "0", "1"
        date1 = "".join(date1)
        logger.debug(f"Date for Sneaker 1: {date1}")

        # 来月の発売日
        date2 = self.year + "-" + self.next_month + "-" + "01"
        logger.debug(f"Date for Sneaker 2: {date2}")

        book_list = self.set_book_info(elms1, [date1] * len(elms1))
        return book_list + self.set_book_info(elms2, [date2] * len(elms2))
