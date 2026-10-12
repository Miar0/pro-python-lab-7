import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from hotel_booking.models import Base
from hotel_booking.uow import UnitOfWork


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite:///:memory:")

    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def uow(test_engine):
    TestSession = sessionmaker(bind=test_engine, expire_on_commit=False)
    uow = UnitOfWork()
    uow.session_factory = TestSession
    return uow