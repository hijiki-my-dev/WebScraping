import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    notion_api_key: str
    notion_database_id: str
    mail_address: str
    gmail_password: str
    log_level: str = "DEBUG"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def notion_url_db(self) -> str:
        return f"https://api.notion.com/v1/databases/{self.notion_database_id}/query"

    @property
    def log_level_int(self) -> int:
        return getattr(logging, self.log_level.upper(), logging.DEBUG)


settings = Settings()
log_level = settings.log_level_int
