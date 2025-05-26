# backend/backend/models/bus.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum as SAEnum
)
from sqlalchemy.orm import relationship
from .meta import Base
import enum

class BusClass(enum.Enum):
    ECONOMY = "economy"
    BUSINESS = "business"

class Bus(Base):
    __tablename__ = 'buses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True) # Nama bus sebaiknya unik
    capacity = Column(Integer, nullable=False)
    bus_class = Column(SAEnum(BusClass, name="bus_class_enum", create_type=True), nullable=False, default=BusClass.ECONOMY)

    # Relasi ke Schedule: satu bus bisa memiliki banyak jadwal
    schedules = relationship("Schedule", back_populates="bus")

    def __repr__(self):
        return f"<Bus(id={self.id}, name='{self.name}', class='{self.bus_class.value}')>"