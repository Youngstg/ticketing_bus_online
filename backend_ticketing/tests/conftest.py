import pytest
import transaction
from webtest import TestApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend_ticketing import main
from backend_ticketing.models.meta import Base
from backend_ticketing.models import Bus, Route, Schedule, Seat, Ticket
from datetime import datetime, timedelta
import base64

@pytest.fixture(scope="session")
def engine():
    """Create an in-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def dbsession(engine):
    """Create a database session for each test."""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Add sample data
    bus1 = Bus(name="Sinar Jaya", license_plate="B 1234 XX")
    bus2 = Bus(name="Kramat Djati", license_plate="B 5678 YY")
    
    route1 = Route(origin="Jakarta", destination="Bandung", duration=180)
    route2 = Route(origin="Jakarta", destination="Surabaya", duration=720)
    
    session.add_all([bus1, bus2, route1, route2])
    session.flush()
    
    # Create schedules
    schedule1 = Schedule(
        bus_id=bus1.id,
        route_id=route1.id,
        departure_time=datetime.now() + timedelta(hours=2),
        price=50000
    )
    schedule2 = Schedule(
        bus_id=bus2.id,
        route_id=route2.id,
        departure_time=datetime.now() + timedelta(hours=4),
        price=150000
    )
    
    session.add_all([schedule1, schedule2])
    session.flush()
    
    # Create seats
    for i in range(1, 5):  # 4 seats per schedule
        seat1 = Seat(schedule_id=schedule1.id, seat_number=f"A{i}", is_booked=False)
        seat2 = Seat(schedule_id=schedule2.id, seat_number=f"A{i}", is_booked=False)
        session.add_all([seat1, seat2])
    
    session.commit()
    
    yield session
    
    session.close()

@pytest.fixture(scope="function")
def app(dbsession):
    """Create a TestApp instance with mocked database session."""
    settings = {
        "sqlalchemy.url": "sqlite:///:memory:",
        "pyramid.includes": ["pyramid_tm"],
        "testing": True,
    }
    
    pyramid_app = main({}, **settings)
    
    # Mock the dbsession request method
    def mock_dbsession(request):
        return dbsession
    
    pyramid_app.registry.settings = settings
    testapp = TestApp(pyramid_app)
    
    # Patch the request to use our test session
    original_get = testapp.app.__call__
    
    def patched_call(environ, start_response):
        def get_dbsession(request):
            return dbsession
        
        # Store original method and replace
        if hasattr(testapp.app.registry, '_dbsession_factory'):
            original_factory = testapp.app.registry._dbsession_factory
        
        # Mock the dbsession factory
        testapp.app.registry['dbsession_factory'] = lambda: dbsession
        
        # Create a mock request object that will return our test session
        class MockRequest:
            def __init__(self, real_request):
                self._real_request = real_request
                
            def __getattr__(self, name):
                if name == 'dbsession':
                    return dbsession
                return getattr(self._real_request, name)
        
        return original_get(environ, start_response)
    
    testapp.app.__call__ = patched_call
    return testapp

@pytest.fixture
def basic_auth_headers():
    """Generate basic auth headers for admin access."""
    credentials = base64.b64encode(b"admin:admin123").decode('utf-8')
    return {"Authorization": f"Basic {credentials}"}

@pytest.fixture
def sample_bus_data():
    return {
        "name": "Test Bus",
        "license_plate": "B 9999 TEST"
    }

@pytest.fixture
def sample_route_data():
    return {
        "origin": "Test Origin",
        "destination": "Test Destination", 
        "duration": 300
    }

@pytest.fixture
def sample_schedule_data():
    return {
        "bus_id": 1,
        "route_id": 1,
        "departure_time": (datetime.now() + timedelta(hours=6)).isoformat(),
        "price": 75000
    }