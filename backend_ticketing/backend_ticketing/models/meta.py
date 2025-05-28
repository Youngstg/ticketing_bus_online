# backend_ticketing/models/meta.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import zope.sqlalchemy

# Rekomendasi penamaan konvensi untuk constraint SQLAlchemy
# lihat https://alembic.sqlalchemy.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

DBSession = scoped_session(sessionmaker())
zope.sqlalchemy.register(DBSession)

Base = declarative_base()

# DBSession tidak didefinisikan di sini atau di models/__init__.py secara global.
# Ini akan disediakan oleh request.dbsession.