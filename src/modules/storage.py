import ast

from google.cloud import storage

class StorageClient:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def get_reading_book_list(self, file_name):
        blob = self.bucket.blob(file_name)
        content = blob.download_as_string()

        # バイト列を文字列に変換
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        reading_book_list = ast.literal_eval(content)

        return reading_book_list