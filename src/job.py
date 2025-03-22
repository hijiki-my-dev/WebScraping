import time

from modules import (
    DengekiScraper,
    FantasiaScraper,
    GagagaScraper,
    GaScraper,
    MfScraper,
    NotionClient,
    SneakerScraper,
    delete_old_pages,
)
from utils import Logger, booklist, log_level

logger = Logger(log_level=log_level)


def run():
    all_book_list = []
    scraping_classes = [
        DengekiScraper,
        MfScraper,
        GagagaScraper,
        FantasiaScraper,
        GaScraper,
        SneakerScraper,
    ]
    for scraping_class in scraping_classes:
        all_book_list += scraping_class().scrape()
        logger.debug(f"Length of book_list: {len(all_book_list)}")

    # 現在のデータベース情報を取得
    logger.debug("Start getting current pages")
    notion_client = NotionClient()
    current_db = notion_client.get_current_pages()

    logger.debug("Start adding to notion")
    for i in range(len(all_book_list)):
        # 既存のデータベースに含まれている場合はスキップ
        if all_book_list[i].title in current_db:
            continue
        else:
            check_flag = 0
            for book in booklist:
                if book in all_book_list[i].title:
                    check_flag = 1
                    break
            time.sleep(0.5)
            notion_client.add_to_notion(
                all_book_list[i].title,
                all_book_list[i].tag,
                all_book_list[i].date,
                check_flag,
            )


if __name__ == "__main__":
    delete_old_pages()
    time.sleep(10)
    run()
