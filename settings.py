from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    METHOD: str
    BODY: dict = {}
    HEADERS: dict = {}
    PARAMS: dict = {}
    BASE_URL: str
    ENDPOINT: str
    TOTAL_REQUESTS: int
    MAX_AT_ONCE: int
    MAX_PER_SECOND: int

    def __init__(self, **data):
        super().__init__(**data)
        if not self.ENDPOINT.startswith('/'):
            self.ENDPOINT = '/' + self.ENDPOINT
