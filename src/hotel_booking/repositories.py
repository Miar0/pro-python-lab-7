from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, asc, desc
from .models import Base, Room, Guest, Reservation

T = TypeVar('T', bound=Base)

class GenericRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def add(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.session.get(self.model, entity_id)

    def get_all(self, skip: int = 0, limit: int = 100, sort_by: str = "id", order: str = "asc") -> List[T]:
        sort_col = getattr(self.model, sort_by)
        statement = select(self.model).order_by(
            asc(sort_col) if order == "asc" else desc(sort_col)
        ).offset(skip).limit(limit)
        return list(self.session.scalars(statement))

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

class RoomRepository(GenericRepository[Room]):
    def __init__(self, session: Session):
        super().__init__(session, Room)

    def get_by_number(self, number: str) -> Optional[Room]:
        return self.session.scalar(select(Room).where(Room.number == number))

class GuestRepository(GenericRepository[Guest]):
    def __init__(self, session: Session):
        super().__init__(session, Guest)

class ReservationRepository(GenericRepository[Reservation]):
    def __init__(self, session: Session):
        super().__init__(session, Reservation)