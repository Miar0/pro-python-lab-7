import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from hotel_booking.models import Room, Guest
from hotel_booking.services import HotelService


def test_crud_room(uow):
    with uow as u:
        room = Room(number="105", type="Standard", price=1200.0)
        u.rooms.add(room)
        u.commit()
        room_id = room.id

    with uow as u:
        loaded = u.rooms.get_by_id(room_id)
        assert loaded.number == "105"

        loaded.price = 1500.0
        u.commit()

    with uow as u:
        updated = u.rooms.get_by_id(room_id)
        assert updated.price == 1500.0

        u.rooms.delete(updated)
        u.commit()

    with uow as u:
        assert u.rooms.get_by_id(room_id) is None


def test_check_constraint_price(uow):
    with uow as u:
        room = Room(number="999", type="Standard", price=-100.0)
        u.rooms.add(room)
        with pytest.raises(IntegrityError):
            u.commit()


def test_transaction_rollback_on_double_booking(uow):
    service = HotelService(uow)

    with uow as u:
        room = Room(number="777", type="Luxe", price=2000.0)
        guest1 = Guest(first_name="A", last_name="B", email="a@b.com")
        guest2 = Guest(first_name="C", last_name="D", email="c@d.com")
        u.rooms.add(room)
        u.guests.add(guest1)
        u.guests.add(guest2)
        u.commit()
        r_id, g1_id, g2_id = room.id, guest1.id, guest2.id

    service.book_room(r_id, g1_id, date(2023, 5, 1), date(2023, 5, 10))

    with pytest.raises(ValueError, match="Конфлікт"):
        service.book_room(r_id, g2_id, date(2023, 5, 5), date(2023, 5, 15))

    with uow as u:
        reservations = u.reservations.get_all()
        assert len(reservations) == 1
        assert reservations[0].guest_id == g1_id


def test_aggregations(uow):
    service = HotelService(uow)
    with uow as u:
        u.rooms.add(Room(number="001", type="A", price=100.0))
        u.rooms.add(Room(number="002", type="A", price=200.0))
        u.rooms.add(Room(number="003", type="B", price=300.0))
        u.commit()

    assert service.get_potential_revenue() == 600.0

    rev_by_type = service.get_revenue_by_room_type()
    assert rev_by_type["A"] == 300.0
    assert rev_by_type["B"] == 300.0