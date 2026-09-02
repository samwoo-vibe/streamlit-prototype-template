from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from samwoo_prototype.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
database_url = make_url(settings.database_url)
if (
    database_url.get_backend_name() == "sqlite"
    and database_url.database
    and database_url.database != ":memory:"
):
    Path(database_url.database).parent.mkdir(parents=True, exist_ok=True)

engine_options: dict[str, object] = {"pool_pre_ping": True}
if database_url.get_backend_name() == "postgresql":
    # The provisioned role is limited to 20 sessions. Two overlapping rolling
    # containers stay below that limit while leaving room for migrations.
    engine_options.update(
        pool_size=5,
        max_overflow=3,
        pool_timeout=5,
        connect_args={"connect_timeout": 5},
    )

engine = create_engine(database_url, **engine_options)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
