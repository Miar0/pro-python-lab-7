from datetime import date
from sqlalchemy import select, func, or_, and_
from .uow import UnitOfWork
from .models import Room, Reservation, Guest


class HotelService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def book_room(self, room_id: int, guest_id: int, check_in: date, check_out: date) -> Reservation:
        """
        Транзакційна операція бронювання з дотриманням принципів ACID (Atomicity, Consistency, Isolation, Durability).
        Якщо виникає конфлікт дат або помилка - виконується rollback().
        """
        with self.uow as uow:
            conflict = uow.session.execute(
                select(Reservation).where(
                    Reservation.room_id == room_id,
                    or_(
                        and_(Reservation.check_in <= check_in, Reservation.check_out > check_in),
                        and_(Reservation.check_in < check_out, Reservation.check_out >= check_out),
                        and_(Reservation.check_in >= check_in, Reservation.check_out <= check_out)
                    )
                )
            ).scalars().first()

            if conflict:
                uow.rollback()
                raise ValueError("Конфлікт бронювання: номер вже зайнятий на ці дати.")

            room = uow.rooms.get_by_id(room_id)
            if not room:
                raise ValueError("Номер не знайдено.")

            reservation = Reservation(room_id=room_id, guest_id=guest_id, check_in=check_in, check_out=check_out)
            uow.reservations.add(reservation)

            room.status = "booked"

            try:
                uow.commit()
                uow.session.refresh(reservation)
                return reservation
            except Exception as e:
                uow.rollback()
                raise e

    def get_potential_revenue(self) -> float:
        """Використання агрегації SUM()."""
        with self.uow as uow:
            result = uow.session.scalar(select(func.sum(Room.price)))
            return float(result) if result else 0.0

    def get_revenue_by_room_type(self) -> dict:
        """Використання агрегацій SUM() та GROUP BY (додаткове завдання)."""
        with self.uow as uow:
            result = uow.session.execute(
                select(Room.type, func.sum(Room.price)).group_by(Room.type)
            ).all()
            return {row[0]: row[1] for row in result}

    def get_booking_history(self) -> list:
        """Складний JOIN декількох таблиць (додаткове завдання)."""
        with self.uow as uow:
            result = uow.session.execute(
                select(Guest.last_name, Room.number, Reservation.check_in)
                .join(Guest, Reservation.guest_id == Guest.id)
                .join(Room, Reservation.room_id == Room.id)
            ).all()
            return result