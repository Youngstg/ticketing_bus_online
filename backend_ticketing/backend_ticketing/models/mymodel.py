from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .meta import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user', nullable=False)  # 'user' or 'admin'

class Bus(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    license_plate = Column(String, unique=True, nullable=False)

class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)

class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey('buses.id'))
    route_id = Column(Integer, ForeignKey('routes.id'))
    departure_time = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)

    seats = relationship("Seat", back_populates="schedule")
    bus = relationship("Bus")
    route = relationship("Route")

class Seat(Base):
    __tablename__ = 'seats'
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    seat_number = Column(String, nullable=False)  # 🆕 nomor kursi seperti A1, A2, dst.
    is_booked = Column(Boolean, default=False)

    schedule = relationship('Schedule', back_populates='seats')

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    seat_id = Column(Integer, ForeignKey('seats.id'), nullable=False)
    customer_name = Column(String, nullable=False)
    booking_code = Column(String, unique=True, nullable=False)
    status = Column(String, default='confirmed')

    seat = relationship("Seat")