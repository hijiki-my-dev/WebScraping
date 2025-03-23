import time

from modules import (
    DengekiScraper,
    FantasiaScraper,
    GagagaScraper,
    GaScraper,
    MfScraper,
    NotionClient,
    SneakerScraper,
    StorageClient
)
from utils import Logger, reading_book_list, log_level, environment, storage_bucket, storage_book_list_path

logger = Logger(log_level=log_level)


def run():
    logger.info("Start scraping")
    if not environment == "local":
        logger.info("Get reading book list from storage")
        storage_client = StorageClient(storage_bucket)
        reading_book_list = storage_client.get_reading_book_list(storage_book_list_path)
    logger.info(f"Reading book list: {reading_book_list}")

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
        try:
            all_book_list += scraping_class().scrape()
        except:
            logger.error(f"Error occurred in {scraping_class}")
        logger.info(f"Length of book_list: {len(all_book_list)}")

    # 現在のデータベース情報を取得
    logger.info("Start getting current pages")
    notion_client = NotionClient()
    current_db = notion_client.get_current_pages()

    logger.info("Start adding to notion")
    for i in range(len(all_book_list)):
        # 既存のデータベースに含まれている場合はスキップ
        if all_book_list[i].title in current_db:
            continue
        else:
            check_flag = 0
            for book in reading_book_list:
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
    logger.info("Finish all process")
