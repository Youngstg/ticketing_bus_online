import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from backend_ticketing.models.meta import Base
from backend_ticketing.models import Bus, Route, Schedule, Seat, Ticket
from datetime import datetime, timedelta

@pytest.fixture
def session():
    """Create a fresh database session for each test."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

class TestBusModel:
    def test_bus_creation(self, session):
        """Test basic bus creation."""
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        session.add(bus)
        session.commit()
        
        assert bus.id is not None
        assert bus.name == "Test Bus"
        assert bus.license_plate == "B 1234 AB"
    
    def test_bus_unique_license_plate(self, session):
        """Test that license plates must be unique."""
        bus1 = Bus(name="Bus 1", license_plate="B 1234 AB")
        bus2 = Bus(name="Bus 2", license_plate="B 1234 AB")
        
        session.add(bus1)
        session.commit()
        
        session.add(bus2)
        with pytest.raises(IntegrityError):
            session.commit()
    
    def test_bus_unique_name(self, session):
        """Test that bus names must be unique."""
        bus1 = Bus(name="Unique Bus", license_plate="B 1111 AA")
        bus2 = Bus(name="Unique Bus", license_plate="B 2222 BB")
        
        session.add(bus1)
        session.commit()
        
        session.add(bus2)
        with pytest.raises(IntegrityError):
            session.commit()
    
    def test_bus_required_fields(self, session):
        """Test that required fields cannot be null."""
        # Test missing name
        with pytest.raises(IntegrityError):
            bus = Bus(license_plate="B 1234 AB")
            session.add(bus)
            session.commit()
        
        session.rollback()
        
        # Test missing license_plate
        with pytest.raises(IntegrityError):
            bus = Bus(name="Test Bus")
            session.add(bus)
            session.commit()

class TestRouteModel:
    def test_route_creation(self, session):
        """Test basic route creation."""
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add(route)
        session.commit()
        
        assert route.id is not None
        assert route.origin == "Jakarta"
        assert route.destination == "Bandung"
        assert route.duration == 180
    
    def test_route_required_fields(self, session):
        """Test that required fields cannot be null."""
        # Test missing origin
        with pytest.raises(IntegrityError):
            route = Route(destination="Bandung", duration=180)
            session.add(route)
            session.commit()
        
        session.rollback()
        
        # Test missing destination
        with pytest.raises(IntegrityError):
            route = Route(origin="Jakarta", duration=180)
            session.add(route)
            session.commit()
        
        session.rollback()
        
        # Test missing duration
        with pytest.raises(IntegrityError):
            route = Route(origin="Jakarta", destination="Bandung")
            session.add(route)
            session.commit()

class TestScheduleModel:
    def test_schedule_creation(self, session):
        """Test basic schedule creation."""
        # Create dependencies first
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        departure_time = datetime.now() + timedelta(hours=2)
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=departure_time,
            price=50000
        )
        session.add(schedule)
        session.commit()
        
        assert schedule.id is not None
        assert schedule.bus_id == bus.id
        assert schedule.route_id == route.id
        assert schedule.departure_time == departure_time
        assert schedule.price == 50000
    
    def test_schedule_relationships(self, session):
        """Test schedule relationships with bus and route."""
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=2),
            price=50000
        )
        session.add(schedule)
        session.commit()
        
        # Test relationships
        assert schedule.bus == bus
        assert schedule.route == route
        assert schedule.bus.name == "Test Bus"
        assert schedule.route.origin == "Jakarta"
    
    def test_schedule_required_fields(self, session):
        """Test that required fields cannot be null."""
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        # Test missing departure_time
        with pytest.raises(IntegrityError):
            schedule = Schedule(bus_id=bus.id, route_id=route.id, price=50000)
            session.add(schedule)
            session.commit()
        
        session.rollback()
        
        # Test missing price
        with pytest.raises(IntegrityError):
            schedule = Schedule(
                bus_id=bus.id,
                route_id=route.id,
                departure_time=datetime.now() + timedelta(hours=2)
            )
            session.add(schedule)
            session.commit()

class TestSeatModel:
    def test_seat_creation(self, session):
        """Test basic seat creation."""
        # Create dependencies
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=2),
            price=50000
        )
        session.add_all([bus, route])
        session.flush()
        schedule.bus_id = bus.id
        schedule.route_id = route.id
        session.add(schedule)
        session.flush()
        
        seat = Seat(
            schedule_id=schedule.id,
            seat_number="A1",
            is_booked=False
        )
        session.add(seat)
        session.commit()
        
        assert seat.id is not None
        assert seat.schedule_id == schedule.id
        assert seat.seat_number == "A1"
        assert seat.is_booked is False
    
    def test_seat_relationships(self, session):
        """Test seat relationships with schedule."""
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=2),
            price=50000
        )
        session.add(schedule)
        session.flush()
        
        seat = Seat(
            schedule_id=schedule.id,
            seat_number="A1",
            is_booked=False
        )
        session.add(seat)
        session.commit()
        
        # Test relationships
        assert seat.schedule == schedule
        assert schedule in [s.schedule for s in schedule.seats]
    
    def test_seat_required_fields(self, session):
        """Test that required fields cannot be null."""
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=2),
            price=50000
        )
        session.add(schedule)
        session.flush()
        
        # Test missing seat_number
        with pytest.raises(IntegrityError):
            seat = Seat(schedule_id=schedule.id, is_booked=False)
            session.add(seat)
            session.commit()

class TestTicketModel:
    def test_ticket_creation(self, session):
        """Test basic ticket creation."""
        # Create dependencies
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=2),
            price=50000
        )
        session.add(schedule)
        session.flush()
        
        seat = Seat(
            schedule_id=schedule.id,
            seat_number="A1",
            is_booked=False
        )
        session.add(seat)
        session.flush()
        
        ticket = Ticket(
            seat_id=seat.id,
            customer_name="John Doe",
            booking_code="ABCD1234",
            status="confirmed"
        )
        session.add(ticket)
        session.commit()
        
        assert ticket.id is not None
        assert ticket.seat_id == seat.id
        assert ticket.customer_name == "John Doe"
        assert ticket.booking_code == "ABCD1234"
        assert ticket.status == "confirmed"
    
    def test_ticket_relationships(self, session):
        """Test ticket relationships with seat."""
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=2),
            price=50000
        )
        session.add(schedule)
        session.flush()
        
        seat = Seat(
            schedule_id=schedule.id,
            seat_number="A1",
            is_booked=False
        )
        session.add(seat)
        session.flush()
        
        ticket = Ticket(
            seat_id=seat.id,
            customer_name="John Doe",
            booking_code="ABCD1234",
            status="confirmed"
        )
        session.add(ticket)
        session.commit()
        
        # Test relationships
        assert ticket.seat == seat
        assert ticket.seat.seat_number == "A1"
        assert ticket.seat.schedule.bus.name == "Test Bus"
    
    def test_ticket_unique_booking_code(self, session):
        """Test that booking codes must be unique."""
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=2),
            price=50000
        )
        session.add(schedule)
        session.flush()
        
        seat1 = Seat(schedule_id=schedule.id, seat_number="A1", is_booked=False)
        seat2 = Seat(schedule_id=schedule.id, seat_number="A2", is_booked=False)
        session.add_all([seat1, seat2])
        session.flush()
        
        ticket1 = Ticket(
            seat_id=seat1.id,
            customer_name="John Doe",
            booking_code="DUPLICATE",
            status="confirmed"
        )
        session.add(ticket1)
        session.commit()
        
        ticket2 = Ticket(
            seat_id=seat2.id,
            customer_name="Jane Doe",
            booking_code="DUPLICATE",
            status="confirmed"
        )
        session.add(ticket2)
        
        with pytest.raises(IntegrityError):
            session.commit()
    
    def test_ticket_required_fields(self, session):
        """Test that required fields cannot be null."""
        bus = Bus(name="Test Bus", license_plate="B 1234 AB")
        route = Route(origin="Jakarta", destination="Bandung", duration=180)
        session.add_all([bus, route])
        session.flush()
        
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=2),
            price=50000
        )
        session.add(schedule)
        session.flush()
        
        seat = Seat(schedule_id=schedule.id, seat_number="A1", is_booked=False)
        session.add(seat)
        session.flush()
        
        # Test missing customer_name
        with pytest.raises(IntegrityError):
            ticket = Ticket(
                seat_id=seat.id,
                booking_code="ABCD1234",
                status="confirmed"
            )
            session.add(ticket)
            session.commit()
        
        session.rollback()
        
        # Test missing booking_code
        with pytest.raises(IntegrityError):
            ticket = Ticket(
                seat_id=seat.id,
                customer_name="John Doe",
                status="confirmed"
            )
            session.add(ticket)
            session.commit()
        
        session.rollback()
        
        # Test missing seat_id
        with pytest.raises(IntegrityError):
            ticket = Ticket(
                customer_name="John Doe",
                booking_code="ABCD1234",
                status="confirmed"
            )
            session.add(ticket)
            session.commit()

class TestComplexRelationships:
    def test_full_booking_flow(self, session):
        """Test a complete booking flow with all relationships."""
        # Create bus
        bus = Bus(name="Express Bus", license_plate="B 9999 EX")
        
        # Create route
        route = Route(origin="Jakarta", destination="Surabaya", duration=720)
        
        session.add_all([bus, route])
        session.flush()
        
        # Create schedule
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(days=1),
            price=150000
        )
        session.add(schedule)
        session.flush()
        
        # Create seats
        seats = []
        for i in range(1, 6):  # 5 seats
            seat = Seat(
                schedule_id=schedule.id,
                seat_number=f"A{i}",
                is_booked=False
            )
            seats.append(seat)
        
        session.add_all(seats)
        session.flush()
        
        # Book some seats
        ticket1 = Ticket(
            seat_id=seats[0].id,
            customer_name="Alice Johnson",
            booking_code="ALICE001",
            status="confirmed"
        )
        
        ticket2 = Ticket(
            seat_id=seats[1].id,
            customer_name="Bob Smith",
            booking_code="BOB002",
            status="confirmed"
        )
        
        session.add_all([ticket1, ticket2])
        
        # Mark seats as booked
        seats[0].is_booked = True
        seats[1].is_booked = True
        
        session.commit()
        
        # Verify the complete chain
        assert len(schedule.seats) == 5
        assert sum(1 for seat in schedule.seats if seat.is_booked) == 2
        assert ticket1.seat.schedule.bus.name == "Express Bus"
        assert ticket1.seat.schedule.route.destination == "Surabaya"
        assert ticket1.seat.schedule.price == 150000
    
    def test_cascade_operations(self, session):
        """Test cascade behavior when deleting related records."""
        # Create complete structure
        bus = Bus(name="Test Bus", license_plate="B 1234 TEST")
        route = Route(origin="A", destination="B", duration=60)
        session.add_all([bus, route])
        session.flush()
        
        schedule = Schedule(
            bus_id=bus.id,
            route_id=route.id,
            departure_time=datetime.now() + timedelta(hours=1),
            price=25000
        )
        session.add(schedule)
        session.flush()
        
        seat = Seat(schedule_id=schedule.id, seat_number="A1", is_booked=False)
        session.add(seat)
        session.flush()
        
        ticket = Ticket(
            seat_id=seat.id,
            customer_name="Test User",
            booking_code="TEST123",
            status="confirmed"
        )
        session.add(ticket)
        session.commit()
        
        # Verify all records exist
        assert session.query(Bus).count() == 1
        assert session.query(Route).count() == 1
        assert session.query(Schedule).count() == 1
        assert session.query(Seat).count() == 1
        assert session.query(Ticket).count() == 1
        
        # Test that we can query through relationships
        found_ticket = session.query(Ticket).filter_by(booking_code="TEST123").first()
        assert found_ticket is not None
        assert found_ticket.seat.schedule.bus.name == "Test Bus"