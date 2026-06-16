import os
from contextlib import contextmanager
from datetime import date
from typing import Iterator

from sqlalchemy import Date, Float, Integer, String, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/vehicle_management"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


class Base(DeclarativeBase):
    pass


class RefuelEntry(Base):
    __tablename__ = "refuels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    odometer: Mapped[int] = mapped_column(Integer, nullable=False)
    fuel_type: Mapped[str] = mapped_column(String(50), nullable=False)
    total_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    price_per_liter: Mapped[float | None] = mapped_column(Float, nullable=True)
    liters: Mapped[float | None] = mapped_column(Float, nullable=True)


class VehicleEntry(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(80), nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=False)
    version: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    plate: Mapped[str] = mapped_column(String(20), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    original_width: Mapped[int] = mapped_column(Integer, nullable=False)
    original_aspect: Mapped[int] = mapped_column(Integer, nullable=False)
    original_rim: Mapped[int] = mapped_column(Integer, nullable=False)
    current_width: Mapped[int] = mapped_column(Integer, nullable=False)
    current_aspect: Mapped[int] = mapped_column(Integer, nullable=False)
    current_rim: Mapped[int] = mapped_column(Integer, nullable=False)
    fuel_tank_capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)


engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def ensure_database_exists() -> None:
    url = make_url(DATABASE_URL)
    if url.get_backend_name() != "postgresql":
        return

    database_name = url.database
    if not database_name:
        raise ValueError("DATABASE_URL must include a PostgreSQL database name.")

    maintenance_url = url.set(database="postgres")
    maintenance_engine = create_engine(maintenance_url, isolation_level="AUTOCOMMIT", future=True)

    try:
        with maintenance_engine.connect() as connection:
            exists = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
                {"database_name": database_name},
            ).scalar()

            if not exists:
                connection.exec_driver_sql(f"CREATE DATABASE {_quote_identifier(database_name)}")
    finally:
        maintenance_engine.dispose()


def init_db() -> None:
    ensure_database_exists()
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
