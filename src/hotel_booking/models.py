from sqlalchemy import Integer, String, Float, ForeignKey, CheckConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from .database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="available")

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
    )

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )


class Guest(Base):
    __tablename__ = "guests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="guest", cascade="all, delete-orphan"
    )


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    guest_id: Mapped[int] = mapped_column(ForeignKey("guests.id"), nullable=False)

    check_in: Mapped[date] = mapped_column(Date, nullable=False)
    check_out: Mapped[date] = mapped_column(Date, nullable=False)

    room: Mapped["Room"] = relationship(back_populates="reservations")
    guest: Mapped["Guest"] = relationship(back_populates="reservations")