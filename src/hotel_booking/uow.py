from .database import SessionLocal
from .repositories import RoomRepository, GuestRepository, ReservationRepository

class UnitOfWork:
    def __init__(self):
        self.session_factory = SessionLocal

    def __enter__(self):
        self.session = self.session_factory()
        self.rooms = RoomRepository(self.session)
        self.guests = GuestRepository(self.session)
        self.reservations = ReservationRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()