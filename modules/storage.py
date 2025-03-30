import ast

from azure.storage.blob import BlobServiceClient

from utils import Logger, log_level

logger = Logger(log_level)


class StorageClient:
    def __init__(self, connection_string: str, container_name: str):
        logger.debug(f"connection_string: {connection_string}")
        logger.debug(f"container_name: {container_name}")
        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        logger.debug(f"blob_service_client: {self.blob_service_client}")
        self.container_client = self.blob_service_client.get_container_client(
            container_name
        )
        logger.debug(f"container_client: {self.container_client}")

    def get_reading_book_list(self, blob_name: str) -> list[str]:
        blob_client = self.container_client.get_blob_client(blob_name)
        logger.debug(f"blob_client: {blob_client}")
        content = blob_client.download_blob().readall().decode("utf-8")
        # 改行で分割してリスト化
        words_list = [line.strip() for line in content.splitlines() if line.strip()]

        return words_list
