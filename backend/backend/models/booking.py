# backend/backend/models/booking.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    Enum as SAEnum
)
from sqlalchemy.orm import relationship
from .meta import Base
import datetime
import enum

class BookingStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    seat_number = Column(String(10), nullable=False) # Contoh: 'A1', 'B3'
    
    # Frontend menggunakan 'price' untuk order, kita simpan sebagai total_price
    # Ini bisa sama dengan schedule.price jika 1 booking = 1 tiket
    total_price = Column(Numeric(10, 2), nullable=False)
    
    status = Column(SAEnum(BookingStatus, name="booking_status_enum", create_type=True), nullable=False, default=BookingStatus.PENDING)
    
    # Frontend menggunakan 'createdAt' untuk order di dashboard admin
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False) #
    
    # booking_time bisa sama dengan created_at atau waktu spesifik saat konfirmasi
    booking_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


    # Relasi ke User
    user = relationship("User") # Tambahkan back_populates="bookings" di model User jika diperlukan
    # Relasi ke Schedule
    schedule = relationship("Schedule", back_populates="bookings")

    def __repr__(self):
        return f"<Booking(id={self.id}, user_id={self.user_id}, schedule_id={self.schedule_id}, seat='{self.seat_number}', status='{self.status.value}')>"