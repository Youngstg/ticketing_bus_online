from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum as SAEnum
)
from sqlalchemy.orm import relationship
from .meta import Base
from passlib.apps import custom_app_context as pwd_context # Untuk hashing password
import enum

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole, name='user_role_enum', create_type=True), nullable=False, default=UserRole.USER)
    # Ganti create_type=False jika enum sudah dibuat manual di DB atau oleh migrasi sebelumnya.
    # Untuk migrasi pertama, create_type=True biasanya aman jika Alembic menanganinya.

    # bookings = relationship("Booking", back_populates="user") # Contoh relasi

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

# Pastikan Anda mengimpor semua model Anda di backend/backend/models/__init__.py
# agar Alembic dapat menemukannya.