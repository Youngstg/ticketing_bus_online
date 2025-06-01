import pytest
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPCreated, HTTPUnauthorized, HTTPForbidden
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend_ticketing.models.meta import Base
from backend_ticketing.models import Bus, Route, Schedule, Seat, Ticket
from backend_ticketing.views.bus import get_buses, create_bus, get_bus, update_bus, delete_bus
from backend_ticketing.views.route import get_routes, create_route, get_route, update_route, delete_route
from backend_ticketing.views.schedule import get_schedules, create_schedule, get_schedule, search_schedules
from backend_ticketing.views.seat import get_seats, create_seat, get_seat
from backend_ticketing.views.ticket import get_tickets, create_ticket, get_ticket
from backend_ticketing.views.default import home_view
from backend_ticketing.views.auth import check_basic_auth
from datetime import datetime, timedelta
import base64
import uuid

@pytest.fixture
def db_session():
    """Create an in-memory database session for testing."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Add test data
    bus1 = Bus(name="Test Bus 1", license_plate="B 1111 AA")
    bus2 = Bus(name="Test Bus 2", license_plate="B 2222 BB")
    
    route1 = Route(origin="Jakarta", destination="Bandung", duration=180)
    route2 = Route(origin="Bandung", destination="Surabaya", duration=480)
    
    session.add_all([bus1, bus2, route1, route2])
    session.flush()
    
    schedule1 = Schedule(
        bus_id=bus1.id,
        route_id=route1.id,
        departure_time=datetime.now() + timedelta(hours=2),
        price=50000
    )
    
    session.add(schedule1)
    session.flush()
    
    seat1 = Seat(schedule_id=schedule1.id, seat_number="A1", is_booked=False)
    seat2 = Seat(schedule_id=schedule1.id, seat_number="A2", is_booked=True)
    
    session.add_all([seat1, seat2])
    session.flush()
    
    ticket1 = Ticket(
        seat_id=seat2.id,
        customer_name="John Doe",
        booking_code="ABCD1234",
        status="confirmed"
    )
    
    session.add(ticket1)
    session.commit()
    
    return session

class TestDefaultViews:
    def test_home_view(self):
        """Test home view returns correct message."""
        request = DummyRequest()
        result = home_view(request)
        assert result['message'] == 'Welcome to Whiish Bus Ticketing API'

class TestBusViews:
    def test_get_buses(self, db_session):
        """Test getting all buses."""
        request = DummyRequest()
        request.dbsession = db_session
        
        result = get_buses(request)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['name'] == "Test Bus 1"
        assert result[1]['name'] == "Test Bus 2"
    
    def test_get_bus_existing(self, db_session):
        """Test getting an existing bus."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '1'}
        
        result = get_bus(request)
        assert result['id'] == 1
        assert result['name'] == "Test Bus 1"
        assert result['license_plate'] == "B 1111 AA"
    
    def test_get_bus_not_found(self, db_session):
        """Test getting a non-existent bus raises HTTPNotFound."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '999'}
        
        with pytest.raises(HTTPNotFound):
            get_bus(request)
    
    def test_create_bus_without_auth(self, db_session):
        """Test creating bus without authentication raises HTTPUnauthorized."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {'name': 'New Bus', 'license_plate': 'B 3333 CC'}
        
        with pytest.raises(HTTPUnauthorized):
            create_bus(request)
    
    def test_create_bus_with_auth(self, db_session):
        """Test creating bus with valid authentication."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {'name': 'New Bus', 'license_plate': 'B 3333 CC'}
        
        # Add auth header
        credentials = base64.b64encode(b"admin:admin123").decode('utf-8')
        request.headers = {'Authorization': f'Basic {credentials}'}
        
        result = create_bus(request)
        assert isinstance(result, HTTPCreated)
        assert result.json_body['message'] == 'Bus created'
    
    def test_update_bus(self, db_session):
        """Test updating an existing bus."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '1'}
        request.json_body = {'name': 'Updated Bus Name'}
        
        result = update_bus(request)
        assert result['message'] == 'Bus updated'
        assert 'updated_name' in result
    
    def test_delete_bus(self, db_session):
        """Test deleting an existing bus."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '2'}
        
        result = delete_bus(request)
        assert result['message'] == 'Bus deleted'

class TestRouteViews:
    def test_get_routes(self, db_session):
        """Test getting all routes."""
        request = DummyRequest()
        request.dbsession = db_session
        
        result = get_routes(request)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['origin'] == "Jakarta"
        assert result[0]['destination'] == "Bandung"
    
    def test_create_route(self, db_session):
        """Test creating a new route."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {
            'origin': 'Jakarta',
            'destination': 'Yogyakarta',
            'duration': 420
        }
        
        result = create_route(request)
        assert isinstance(result, HTTPCreated)
        assert result.json_body['message'] == 'Route created'
    
    def test_get_route_existing(self, db_session):
        """Test getting an existing route."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '1'}
        
        result = get_route(request)
        assert result['id'] == 1
        assert result['origin'] == "Jakarta"
        assert result['destination'] == "Bandung"
    
    def test_get_route_not_found(self, db_session):
        """Test getting a non-existent route."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '999'}
        
        with pytest.raises(HTTPNotFound):
            get_route(request)
    
    def test_update_route(self, db_session):
        """Test updating an existing route."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '1'}
        request.json_body = {'duration': 200}
        
        result = update_route(request)
        assert result['message'] == 'Route updated'
    
    def test_delete_route(self, db_session):
        """Test deleting an existing route."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '2'}
        
        result = delete_route(request)
        assert result['message'] == 'Route deleted'

class TestScheduleViews:
    def test_get_schedules(self, db_session):
        """Test getting all schedules."""
        request = DummyRequest()
        request.dbsession = db_session
        
        result = get_schedules(request)
        assert isinstance(result, list)
        assert len(result) >= 1
        assert 'departure_time' in result[0]
    
    def test_create_schedule(self, db_session):
        """Test creating a new schedule."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {
            'bus_id': 1,
            'route_id': 1,
            'departure_time': (datetime.now() + timedelta(hours=4)).isoformat(),
            'price': 75000
        }
        
        result = create_schedule(request)
        assert isinstance(result, HTTPCreated)
        assert result.json_body['message'] == 'Schedule created'
    
    def test_get_schedule_existing(self, db_session):
        """Test getting an existing schedule."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '1'}
        
        result = get_schedule(request)
        assert result['id'] == 1
        assert 'departure_time' in result
    
    def test_search_schedules_no_filters(self, db_session):
        """Test searching schedules without filters."""
        request = DummyRequest()
        request.dbsession = db_session
        request.GET = {}
        
        result = search_schedules(request)
        assert isinstance(result, list)
    
    def test_search_schedules_with_origin(self, db_session):
        """Test searching schedules with origin filter."""
        request = DummyRequest()
        request.dbsession = db_session
        request.GET = {'origin': 'Jakarta'}
        
        result = search_schedules(request)
        assert isinstance(result, list)

class TestSeatViews:
    def test_get_seats(self, db_session):
        """Test getting seats for a schedule."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'schedule_id': '1'}
        
        result = get_seats(request)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['seat_number'] in ['A1', 'A2']
    
    def test_create_new_seat(self, db_session):
        """Test creating a new seat."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {
            'schedule_id': 1,
            'seat_number': 'B1',
            'status': 'available'
        }
        
        result = create_seat(request)
        assert isinstance(result, HTTPCreated)
        assert result.json_body['message'] == 'Seat created'
    
    def test_update_existing_seat(self, db_session):
        """Test updating an existing seat."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {
            'schedule_id': 1,
            'seat_number': 'A1',
            'status': 'booked'
        }
        
        result = create_seat(request)
        assert result['message'] == 'Seat status updated'
    
    def test_get_seat_existing(self, db_session):
        """Test getting an existing seat."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '1'}
        
        result = get_seat(request)
        assert result['id'] == 1
        assert result['seat_number'] == 'A1'

class TestTicketViews:
    def test_get_tickets(self, db_session):
        """Test getting all tickets."""
        request = DummyRequest()
        request.dbsession = db_session
        
        result = get_tickets(request)
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0]['customer_name'] == 'John Doe'
    
    def test_create_ticket(self, db_session):
        """Test creating a new ticket."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {
            'seat_id': 1,
            'customer_name': 'Jane Smith'
        }
        
        result = create_ticket(request)
        assert isinstance(result, HTTPCreated)
        assert result.json_body['message'] == 'Ticket created'
        assert 'booking_code' in result.json_body
    
    def test_get_ticket_existing(self, db_session):
        """Test getting an existing ticket."""
        request = DummyRequest()
        request.dbsession = db_session
        request.matchdict = {'id': '1'}
        
        result = get_ticket(request)
        assert result['id'] == 1
        assert result['customer_name'] == 'John Doe'
        assert result['booking_code'] == 'ABCD1234'

class TestAuth:
    def test_check_basic_auth_no_header(self):
        """Test authentication check without Authorization header."""
        request = DummyRequest()
        request.headers = {}
        
        with pytest.raises(HTTPUnauthorized):
            check_basic_auth(request)
    
    def test_check_basic_auth_invalid_format(self):
        """Test authentication check with invalid format."""
        request = DummyRequest()
        request.headers = {'Authorization': 'InvalidFormat'}
        
        with pytest.raises(HTTPUnauthorized):
            check_basic_auth(request)
    
    def test_check_basic_auth_invalid_credentials(self):
        """Test authentication check with invalid credentials."""
        request = DummyRequest()
        credentials = base64.b64encode(b"wrong:password").decode('utf-8')
        request.headers = {'Authorization': f'Basic {credentials}'}
        
        with pytest.raises(HTTPForbidden):
            check_basic_auth(request)
    
    def test_check_basic_auth_valid_credentials(self):
        """Test authentication check with valid credentials."""
        request = DummyRequest()
        credentials = base64.b64encode(b"admin:admin123").decode('utf-8')
        request.headers = {'Authorization': f'Basic {credentials}'}
        
        result = check_basic_auth(request)
        assert result is True

class TestModelOperations:
    def test_bus_model_creation(self, db_session):
        """Test Bus model creation and attributes."""
        bus = Bus(name="Test Model Bus", license_plate="B 4444 DD")
        db_session.add(bus)
        db_session.flush()
        
        assert bus.id is not None
        assert bus.name == "Test Model Bus"
        assert bus.license_plate == "B 4444 DD"
    
    def test_route_model_creation(self, db_session):
        """Test Route model creation and attributes."""
        route = Route(origin="Test Origin", destination="Test Destination", duration=300)
        db_session.add(route)
        db_session.flush()
        
        assert route.id is not None
        assert route.origin == "Test Origin"
        assert route.destination == "Test Destination"
        assert route.duration == 300
    
    def test_schedule_relationships(self, db_session):
        """Test Schedule model relationships."""
        schedule = db_session.query(Schedule).first()
        
        assert schedule.bus is not None
        assert schedule.route is not None
        assert schedule.bus.name == "Test Bus 1"
        assert schedule.route.origin == "Jakarta"
    
    def test_seat_relationships(self, db_session):
        """Test Seat model relationships."""
        seat = db_session.query(Seat).first()
        
        assert seat.schedule is not None
        assert seat.schedule.bus.name == "Test Bus 1"
    
    def test_ticket_relationships(self, db_session):
        """Test Ticket model relationships."""
        ticket = db_session.query(Ticket).first()
        
        assert ticket.seat is not None
        assert ticket.seat.seat_number in ["A1", "A2"]

class TestErrorHandling:
    def test_create_route_missing_data(self, db_session):
        """Test creating route with missing required data."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {'origin': 'Jakarta'}  # missing destination and duration
        
        with pytest.raises(HTTPBadRequest):
            create_route(request)
    
    def test_create_schedule_invalid_data(self, db_session):
        """Test creating schedule with invalid data."""
        request = DummyRequest()
        request.dbsession = db_session
        request.json_body = {
            'bus_id': 999,  # non-existent bus
            'route_id': 1,
            'departure_time': 'invalid-date',
            'price': 50000
        }
        
        with pytest.raises(HTTPBadRequest):
            create_schedule(request)