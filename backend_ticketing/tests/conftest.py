import pytest
from webtest import TestApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend_ticketing import main
from backend_ticketing.models.meta import Base
from backend_ticketing.models import Bus

@pytest.fixture(scope="session")
def app():
    settings = {
        "sqlalchemy.url": "sqlite:///:memory:",
        "pyramid.includes": ["pyramid_sqlalchemy"],
        "testing": True,
    }

    from backend_ticketing import main
    from backend_ticketing.models import initialize_sql
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend_ticketing.models.meta import Base
    from backend_ticketing.models import Bus

    engine = create_engine(settings["sqlalchemy.url"])
    initialize_sql(engine)

    # Setup Pyramid app
    pyramid_app = main({}, **settings)

    # Buat session
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(Bus(name="Sinar Jaya", license_plate="B 1234 XX"))
    session.commit()

    # Inject manual session ke registry agar bisa dipakai saat test
    def dummy_session_factory(request=None):
        return session

    pyramid_app.registry["dbsession_factory"] = dummy_session_factory
    return TestApp(pyramid_app)
