from datetime import date
from .database import engine, Base, find_available_rooms_dbapi
from .uow import UnitOfWork
from .services import HotelService
from .models import Room, Guest


def main() -> None:
    Base.metadata.create_all(engine)

    uow = UnitOfWork()
    service = HotelService(uow)

    with uow as u:
        if not u.rooms.get_by_number("101"):
            u.rooms.add(Room(number="101", type="Standard", price=1000.0))
            u.rooms.add(Room(number="201", type="Luxe", price=2500.0))
            u.guests.add(Guest(first_name="Ivan", last_name="Petrov", email="ivan@example.com"))
            u.commit()

    print("Вільні номери Luxe через DB-API:")
    print(find_available_rooms_dbapi("hotel.db", "Luxe"))

    with uow as u:
        guest = u.session.query(Guest).first()
        room = u.rooms.get_by_number("101")

        try:
            service.book_room(room.id, guest.id, date(2023, 10, 1), date(2023, 10, 5))
            print(f"\nУспішне бронювання номера {room.number}!")
        except Exception as e:
            print(f"Помилка бронювання: {e}")

    print(f"\nПотенційна виручка: {service.get_potential_revenue()}")
    print(f"Виручка за типами номерів: {service.get_revenue_by_room_type()}")


if __name__ == "__main__":
    main()