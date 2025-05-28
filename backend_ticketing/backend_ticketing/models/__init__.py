from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, configure_mappers
import zope.sqlalchemy

# Ekspor DBSession dan Base dari meta
from .meta import DBSession, Base

# Import semua model
from .mymodel import Bus, Route, Schedule, Seat, Ticket # , Seat, Ticket

# Pastikan semua relasi terkonfigurasi sebelum digunakan
configure_mappers()

def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)

def get_session_factory(engine):
    return sessionmaker(bind=engine)

def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession

def includeme(config):
    """
    Inisialisasi model untuk Pyramid.
    """
    settings = config.get_settings()

    config.include('pyramid_tm')
    # config.include('pyramid_retry')  # opsional

    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    Base.metadata.bind = engine

    config.registry['dbsession_factory'] = session_factory

    def dbsession(request):
        return get_tm_session(session_factory, request.tm)

    config.add_request_method(dbsession, reify=True)
