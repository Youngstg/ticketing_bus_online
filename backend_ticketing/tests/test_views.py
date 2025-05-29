from pyramid.testing import DummyRequest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend_ticketing.models.meta import Base
from backend_ticketing.models import Bus
from backend_ticketing.views.bus import get_buses

def test_get_buses_view():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(Bus(name="TestBus", license_plate="B 2222 ZZ"))
    session.commit()

    request = DummyRequest()
    request.dbsession = session

    result = get_buses(request)
    assert isinstance(result, list)
    assert result[0]['name'] == "TestBus"
