from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import register

# Impor Base dan metadata dari meta.py
from .meta import Base, metadata # Pastikan metadata juga diimpor

# Impor semua model Anda di sini
from .user import User, UserRole # UserRole juga perlu jika Enum didefinisikan di sana
from .bus import Bus, BusClass
from .schedule import Schedule
from .booking import Booking, BookingStatus
# ... dan model lainnya

def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)

def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory

def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    register(dbsession, transaction_manager=transaction_manager)
    return dbsession

def includeme(config):
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    config.include('pyramid_tm')

    engine = get_engine(settings)
    # Jika tidak menggunakan Alembic untuk membuat tabel (tidak direkomendasikan)
    # Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)
    config.registry['dbsession_factory'] = session_factory

    config.add_request_method(
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )