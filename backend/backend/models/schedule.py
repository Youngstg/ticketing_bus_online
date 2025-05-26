# backend/backend/models/schedule.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .meta import Base
import datetime

class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey('buses.id'), nullable=False)
    
    # Untuk menyederhanakan, kita gunakan lokasi string langsung seperti di frontend.
    # Jika ingin lebih kompleks, Anda bisa membuat tabel 'Routes' atau 'Locations'.
    origin_location = Column(String(255), nullable=False)
    destination_location = Column(String(255), nullable=False)
    
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 2), nullable=False) # Harga per kursi untuk jadwal ini

    # Relasi ke Bus
    bus = relationship("Bus", back_populates="schedules")
    # Relasi ke Booking: satu jadwal bisa memiliki banyak booking
    bookings = relationship("Booking", back_populates="schedule")

    @property
    def duration_str(self):
        """Menghasilkan durasi dalam format 'Xh Ym'."""
        if self.departure_time and self.arrival_time:
            delta = self.arrival_time - self.departure_time
            total_seconds = delta.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        return None

    def __repr__(self):
        return f"<Schedule(id={self.id}, bus_id={self.bus_id}, from='{self.origin_location}', to='{self.destination_location}')>"