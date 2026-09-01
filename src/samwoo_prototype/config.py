from functools import lru_cache

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    # 기본값을 주지 않는다. 값이 없을 때 조용히 SQLite로 넘어가면 운영에서 데이터가
    # 엉뚱한 곳에 쌓이고 재배포마다 사라진다(사내 배포 규약 R4-4).
    # 로컬에서는 .env가 값을 준다 — 없으면 start.cmd가 .env.example에서 만들어 준다.
    database_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as error:
        raise RuntimeError(
            "DATABASE_URL이 설정되지 않았습니다. "
            "로컬에서는 .env.example을 .env로 복사해 값을 넣으세요. "
            "배포 환경에서는 프로비저너가 주입한 값을 그대로 사용합니다."
        ) from error
