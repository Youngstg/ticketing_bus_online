import pytest
import json
from datetime import datetime, timedelta

class TestHomepage:
    def test_homepage(self, app):
        """Test homepage returns correct message."""
        res = app.get("/", status=200)
        assert res.json['message'] == "Welcome to Whiish Bus Ticketing API"

class TestBusAPI:
    def test_get_buses(self, app):
        """Test getting all buses."""
        res = app.get("/api/buses", status=200)
        data = res.json
        assert isinstance(data, list)
        assert len(data) >= 2
        assert data[0]['name'] in ["Sinar Jaya", "Kramat Djati"]
    
    def test_create_bus_without_auth(self, app, sample_bus_data):
        """Test creating bus without authentication fails."""
        res = app.post_json("/api/buses/create", sample_bus_data, status=401)
        assert 'error' in res.json or res.status_int == 401
    
    def test_create_bus_with_auth(self, app, sample_bus_data, basic_auth_headers):
        """Test creating bus with authentication succeeds."""
        res = app.post_json("/api/buses/create", sample_bus_data, 
                           headers=basic_auth_headers, status=201)
        assert res.json['message'] == 'Bus created'
        assert 'id' in res.json
    
    def test_get_bus_detail(self, app):
        """Test getting specific bus details."""
        res = app.get("/api/buses/detail/1", status=200)
        data = res.json
        assert 'id' in data
        assert 'name' in data
        assert 'license_plate' in data
    
    def test_get_nonexistent_bus(self, app):
        """Test getting non-existent bus returns 404."""
        app.get("/api/buses/detail/999", status=404)
    
    def test_update_bus(self, app):
        """Test updating bus data."""
        update_data = {"name": "Updated Bus Name"}
        res = app.put_json("/api/buses/update/1", update_data, status=200)
        assert res.json['message'] == 'Bus updated'
    
    def test_delete_bus(self, app):
        """Test deleting a bus."""
        res = app.delete("/api/buses/delete/2", status=200)
        assert res.json['message'] == 'Bus deleted'

class TestRouteAPI:
    def test_get_routes(self, app):
        """Test getting all routes."""
        res = app.get("/api/routes", status=200)
        data = res.json
        assert isinstance(data, list)
        assert len(data) >= 2
        
    def test_create_route(self, app, sample_route_data):
        """Test creating a new route."""
        res = app.post_json("/api/routes/create", sample_route_data, status=201)
        assert res.json['message'] == 'Route created'
        assert 'id' in res.json
    
    def test_get_route_detail(self, app):
        """Test getting specific route details."""
        res = app.get("/api/routes/detail/1", status=200)
        data = res.json
        assert 'id' in data
        assert 'origin' in data
        assert 'destination' in data
        assert 'duration' in data
    
    def test_update_route(self, app):
        """Test updating route data."""
        update_data = {"origin": "Updated Origin", "duration": 240}
        res = app.put_json("/api/routes/update/1", update_data, status=200)
        assert res.json['message'] == 'Route updated'
    
    def test_delete_route(self, app):
        """Test deleting a route."""
        # Create a route first to delete
        create_data = {"origin": "Delete Test", "destination": "Test Dest", "duration": 120}
        create_res = app.post_json("/api/routes/create", create_data, status=201)
        route_id = create_res.json['id']
        
        res = app.delete(f"/api/routes/delete/{route_id}", status=200)
        assert res.json['message'] == 'Route deleted'

class TestScheduleAPI:
    def test_get_schedules(self, app):
        """Test getting all schedules."""
        res = app.get("/api/schedules", status=200)
        data = res.json
        assert isinstance(data, list)
        assert len(data) >= 2
    
    def test_create_schedule(self, app, sample_schedule_data):
        """Test creating a new schedule."""
        res = app.post_json("/api/schedules/create", sample_schedule_data, status=201)
        assert res.json['message'] == 'Schedule created'
        assert 'id' in res.json
    
    def test_get_schedule_detail(self, app):
        """Test getting specific schedule details."""
        res = app.get("/api/schedules/detail/1", status=200)
        data = res.json 
        assert 'id' in data
        assert 'bus_id' in data
        assert 'route_id' in data
        assert 'departure_time' in data
    
    def test_search_schedules(self, app):
        """Test searching schedules with filters."""
        res = app.get("/api/schedules/search?origin=Jakarta", status=200)
        data = res.json
        assert isinstance(data, list)
        
        # Test with multiple filters
        res = app.get("/api/schedules/search?origin=Jakarta&destination=Bandung", status=200)
        data = res.json
        assert isinstance(data, list)
    
    def test_update_schedule(self, app):
        """Test updating schedule data."""
        update_data = {"price": 60000}
        res = app.put_json("/api/schedules/update/1", update_data, status=200)
        assert res.json['message'] == 'Schedule updated'

class TestSeatAPI:
    def test_get_seats_for_schedule(self, app):
        """Test getting seats for a specific schedule."""
        res = app.get("/api/seats/1", status=200)
        data = res.json
        assert isinstance(data, list)
        assert len(data) >= 4  # We created 4 seats per schedule
        
        # Check seat structure
        if data:
            seat = data[0]
            assert 'id' in seat
            assert 'seat_number' in seat  
            assert 'is_booked' in seat
            assert 'status' in seat
    
    def test_create_seat(self, app):
        """Test creating a new seat."""
        seat_data = {
            "schedule_id": 1,
            "seat_number": "B1",
            "status": "available"
        }
        res = app.post_json("/api/seats/create", seat_data, status=201)
        assert res.json['message'] == 'Seat created'
        assert 'id' in res.json
    
    def test_update_existing_seat(self, app):
        """Test updating existing seat status."""
        seat_data = {
            "schedule_id": 1,
            "seat_number": "A1", 
            "status": "booked"
        }
        res = app.post_json("/api/seats/create", seat_data, status=200)
        assert res.json['message'] == 'Seat status updated'
    
    def test_get_seat_detail(self, app):
        """Test getting specific seat details."""
        res = app.get("/api/seats/detail/1", status=200)
        data = res.json
        assert 'id' in data
        assert 'seat_number' in data
        assert 'is_booked' in data

class TestTicketAPI:
    def test_get_tickets(self, app):
        """Test getting all tickets."""
        res = app.get("/api/tickets", status=200)
        data = res.json
        assert isinstance(data, list)
    
    def test_create_ticket(self, app):
        """Test creating a new ticket."""
        ticket_data = {
            "seat_id": 1,
            "customer_name": "John Doe"
        }
        res = app.post_json("/api/tickets/create", ticket_data, status=201)
        assert res.json['message'] == 'Ticket created'
        assert 'booking_code' in res.json
        
        # Verify booking code format
        booking_code = res.json['booking_code']
        assert len(booking_code) == 8
        assert booking_code.isupper()
    
    def test_get_ticket_detail(self, app):
        """Test getting specific ticket details."""
        # First create a ticket
        ticket_data = {
            "seat_id": 2,
            "customer_name": "Jane Doe"
        }
        create_res = app.post_json("/api/tickets/create", ticket_data, status=201)
        
        # Get the ticket list to find our ticket ID
        tickets_res = app.get("/api/tickets", status=200)
        tickets = tickets_res.json
        
        if tickets:
            ticket_id = tickets[0]['id']
            res = app.get(f"/api/tickets/detail/{ticket_id}", status=200)
            data = res.json
            assert 'id' in data
            assert 'customer_name' in data
            assert 'booking_code' in data

class TestErrorHandling:
    def test_invalid_json_payload(self, app, basic_auth_headers):
        """Test handling of invalid JSON payload."""
        res = app.post("/api/buses/create", "invalid json", 
                      headers=basic_auth_headers, status=400,
                      content_type='application/json')
    
    def test_missing_required_fields(self, app, basic_auth_headers):
        """Test handling of missing required fields."""
        incomplete_data = {"name": "Test Bus"}  # missing license_plate
        app.post_json("/api/buses/create", incomplete_data,
                     headers=basic_auth_headers, status=400)
    
    def test_cors_preflight(self, app):
        """Test CORS preflight requests."""
        res = app.options("/api/buses/create", status=200)
        # Should return 200 for OPTIONS requests

class TestAuth:
    def test_invalid_auth_format(self, app, sample_bus_data):
        """Test invalid authentication format."""
        headers = {"Authorization": "InvalidFormat"}
        app.post_json("/api/buses/create", sample_bus_data,
                     headers=headers, status=401)
    
    def test_wrong_credentials(self, app, sample_bus_data):
        """Test wrong credentials."""
        import base64
        wrong_creds = base64.b64encode(b"wrong:password").decode('utf-8')
        headers = {"Authorization": f"Basic {wrong_creds}"}
        app.post_json("/api/buses/create", sample_bus_data,
                     headers=headers, status=403)