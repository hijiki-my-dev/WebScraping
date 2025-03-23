import ast

from google.cloud import storage

from utils import Logger, log_level

logger = Logger(log_level)

class StorageClient:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        logger.debug(f"client: {self.client}")
        self.bucket = self.client.bucket(bucket_name)
        logger.debug(f"bucket: {self.bucket}")

    def get_reading_book_list(self, file_name: str) -> list[str]:
        blob = self.bucket.blob(file_name)
        content = blob.download_as_text()
        # 改行で分割してリスト化
        words_list = [line.strip() for line in content.splitlines() if line.strip()]

        return words_list
