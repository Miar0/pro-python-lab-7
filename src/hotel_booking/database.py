import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///hotel.db"

engine = create_engine(DATABASE_URL, echo=False)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
Base = declarative_base()

def find_available_rooms_dbapi(db_path: str, room_type: str) -> list[tuple]:
    """
    Використовує Python DB-API та parameterized query для пошуку вільних номерів.
    Демонструє операцію Read мовою SQL (SELECT).
    """
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT number, type, price 
            FROM rooms 
            WHERE status = 'available' AND type = ?
            """,
            (room_type,)
        )
        return cursor.fetchall()