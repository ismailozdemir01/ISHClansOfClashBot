from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    name: str = Field("ISHClansOfClashBot", alias="BOT_NAME")
    host: str = Field("127.0.0.1", alias="BOT_HOST")
    port: int = Field(8080, alias="BOT_PORT")
    dry_run: bool = Field(True, alias="BOT_DRY_RUN")
    device_serial: str = Field("", alias="BOT_DEVICE_SERIAL")
    screen_width: int = Field(1280, alias="BOT_SCREEN_WIDTH")
    screen_height: int = Field(720, alias="BOT_SCREEN_HEIGHT")
    screenshot_interval: float = Field(0.5, alias="BOT_SCREENSHOT_INTERVAL")
    state_timeout: float = Field(30, alias="BOT_STATE_TIMEOUT")
    max_recovery: int = Field(3, alias="BOT_MAX_RECOVERY")
    database_url: str = Field("sqlite:///./data/bot.db", alias="BOT_DATABASE_URL")
    template_dir: str = Field("assets/templates", alias="BOT_TEMPLATE_DIR")
    ocr_enabled: bool = Field(False, alias="BOT_OCR_ENABLED")
    ocr_lang: str = Field("eng", alias="BOT_OCR_LANG")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)

@lru_cache
def get_settings() -> Settings:
    Path("data").mkdir(exist_ok=True)
    return Settings()
