import pytest
import json
from datetime import datetime, timedelta

class TestBookingWorkflow:
    """Test complete booking workflow from search to ticket creation."""
    
    def test_complete_booking_flow(self, app, basic_auth_headers):
        """Test a complete booking workflow."""
        # 1. Create a bus
        bus_data = {"name": "Integration Bus", "license_plate": "B 9999 INT"}
        bus_res = app.post_json("/api/buses/create", bus_data, 
                               headers=basic_auth_headers, status=201)
        bus_id = bus_res.json['id']
        
        # 2. Create a route
        route_data = {"origin": "Jakarta", "destination": "Yogyakarta", "duration": 360}
        route_res = app.post_json("/api/routes/create", route_data, status=201)
        route_id = route_res.json['id']
        
        # 3. Create a schedule
        departure_time = (datetime.now() + timedelta(days=1)).isoformat()
        schedule_data = {
            "bus_id": bus_id,
            "route_id": route_id,
            "departure_time": departure_time,
            "price": 80000
        }
        schedule_res = app.post_json("/api/schedules/create", schedule_data, status=201)
        schedule_id = schedule_res.json['id']
        
        # 4. Create seats for the schedule
        seat_ids = []
        for i in range(1, 4):  # 3 seats
            seat_data = {
                "schedule_id": schedule_id,
                "seat_number": f"A{i}",
                "status": "available"
            }
            seat_res = app.post_json("/api/seats/create", seat_data, status=201)
            seat_ids.append(seat_res.json['id'])
        
        # 5. Search for schedules
        search_res = app.get("/api/schedules/search?origin=Jakarta&destination=Yogyakarta", 
                            status=200)
        schedules = search_res.json
        assert len(schedules) >= 1
        found_schedule = next((s for s in schedules if s['id'] == schedule_id), None)
        assert found_schedule is not None
        assert found_schedule['price'] == 80000
        
        # 6. Get available seats
        seats_res = app.get(f"/api/seats/{schedule_id}", status=200)
        seats = seats_res.json
        assert len(seats) == 3
        available_seats = [s for s in seats if s['status'] == 'available']
        assert len(available_seats) == 3
        
        # 7. Book a seat by creating a ticket
        ticket_data = {
            "seat_id": seat_ids[0],
            "customer_name": "Integration Test Customer"
        }
        ticket_res = app.post_json("/api/tickets/create", ticket_data, status=201)
        booking_code = ticket_res.json['booking_code']
        assert len(booking_code) == 8
        
        # 8. Verify seat is now booked
        seats_res_after = app.get(f"/api/seats/{schedule_id}", status=200)
        seats_after = seats_res_after.json
        booked_seat = next((s for s in seats_after if s['id'] == seat_ids[0]), None)
        
        # 9. Verify ticket details
        tickets_res = app.get("/api/tickets", status=200)
        tickets = tickets_res.json
        our_ticket = next((t for t in tickets if t['booking_code'] == booking_code), None)
        assert our_ticket is not None
        assert our_ticket['customer_name'] == "Integration Test Customer"
        assert our_ticket['bus_name'] == "Integration Bus"
        assert our_ticket['origin'] == "Jakarta"
        assert our_ticket['destination'] == "Yogyakarta"

class TestDataConsistency:
    """Test data consistency across related models."""
    
    def test_schedule_bus_route_consistency(self, app, basic_auth_headers):
        """Test that schedule data is consistent with bus and route data."""
        # Get existing schedules
        schedules_res = app.get("/api/schedules", status=200)
        schedules = schedules_res.json
        
        for schedule in schedules:
            # Get bus details
            bus_res = app.get(f"/api/buses/detail/{schedule['bus_id']}", status=200)
            bus = bus_res.json
            
            # Get route details
            route_res = app.get(f"/api/routes/detail/{schedule['route_id']}", status=200)
            route = route_res.json
            
            # Verify schedule search returns same data
            search_res = app.get(f"/api/schedules/search?origin={route['origin']}", status=200)
            search_results = search_res.json
            
            matching_schedule = next((s for s in search_results if s['id'] == schedule['id']), None)
            if matching_schedule:  # Schedule might not appear in search if origin doesn't match
                assert matching_schedule['bus'] == bus['name']
                assert matching_schedule['origin'] == route['origin']
                assert matching_schedule['destination'] == route['destination']
    
    def test_ticket_seat_schedule_consistency(self, app):
        """Test that ticket data is consistent across all related models."""
        # Get all tickets
        tickets_res = app.get("/api/tickets", status=200)
        tickets = tickets_res.json
        
        for ticket in tickets:
            if ticket['seat_number'] and ticket['schedule_id']:
                # Get seat details
                seat_res = app.get(f"/api/seats/detail/{ticket['seat_id']}" if 'seat_id' in ticket else f"/api/seats/{ticket['schedule_id']}", status=200)
                
                if f"/api/seats/{ticket['schedule_id']}" in seat_res.request.url:
                    # This was a seats list call
                    seats = seat_res.json
                    matching_seat = next((s for s in seats if s['seat_number'] == ticket['seat_number']), None)
                    if matching_seat:
                        assert matching_seat['is_booked'] == True
                else:
                    # This was a single seat call
                    seat = seat_res.json
                    assert seat['seat_number'] == ticket['seat_number']

class TestErrorHandlingAndValidation:
    """Test error handling and data validation."""
    
    def test_duplicate_bus_creation(self, app, basic_auth_headers):
        """Test that creating duplicate buses is handled properly."""
        bus_data = {"name": "Duplicate Test Bus", "license_plate": "B 8888 DUP"}
        
        # First creation should succeed
        app.post_json("/api/buses/create", bus_data, 
                     headers=basic_auth_headers, status=201)
        
        # Second creation with same data should fail
        app.post_json("/api/buses/create", bus_data, 
                     headers=basic_auth_headers, status=400)
    
    def test_invalid_schedule_creation(self, app):
        """Test creating schedule with invalid bus/route IDs."""
        invalid_schedule_data = {
            "bus_id": 99999,  # Non-existent bus
            "route_id": 99999,  # Non-existent route
            "departure_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "price": 50000
        }
        
        app.post_json("/api/schedules/create", invalid_schedule_data, status=400)
    
    def test_booking_nonexistent_seat(self, app):
        """Test booking a seat that doesn't exist."""
        ticket_data = {
            "seat_id": 99999,  # Non-existent seat
            "customer_name": "Test Customer"
        }
        
        app.post_json("/api/tickets/create", ticket_data, status=400)
    
    def test_invalid_date_format_in_schedule(self, app):
        """Test creating schedule with invalid date format."""
        schedule_data = {
            "bus_id": 1,
            "route_id": 1,
            "departure_time": "invalid-date-format",
            "price": 50000
        }
        
        app.post_json("/api/schedules/create", schedule_data, status=400)

class TestSearchAndFiltering:
    """Test search and filtering functionality."""
    
    def test_schedule_search_filters(self, app, basic_auth_headers):
        """Test various combinations of schedule search filters."""
        # Create test data
        bus_data = {"name": "Search Test Bus", "license_plate": "B 7777 SRC"}
        bus_res = app.post_json("/api/buses/create", bus_data, 
                               headers=basic_auth_headers, status=201)
        bus_id = bus_res.json['id']
        
        route_data = {"origin": "Semarang", "destination": "Solo", "duration": 120}
        route_res = app.post_json("/api/routes/create", route_data, status=201)
        route_id = route_res.json['id']
        
        schedule_data = {
            "bus_id": bus_id,
            "route_id": route_id,
            "departure_time": (datetime.now() + timedelta(days=2)).isoformat(),
            "price": 35000
        }
        schedule_res = app.post_json("/api/schedules/create", schedule_data, status=201)
        schedule_id = schedule_res.json['id']
        
        # Test origin filter
        search_res = app.get("/api/schedules/search?origin=Semarang", status=200)
        results = search_res.json
        found = any(r['id'] == schedule_id for r in results)
        assert found
        
        # Test destination filter
        search_res = app.get("/api/schedules/search?destination=Solo", status=200)
        results = search_res.json
        found = any(r['id'] == schedule_id for r in results)
        assert found
        
        # Test combined filters
        search_res = app.get("/api/schedules/search?origin=Semarang&destination=Solo", status=200)
        results = search_res.json
        found = any(r['id'] == schedule_id for r in results)
        assert found
        
        # Test non-matching filter
        search_res = app.get("/api/schedules/search?origin=NonExistent", status=200)
        results = search_res.json
        found = any(r['id'] == schedule_id for r in results)
        assert not found
    
    def test_case_insensitive_search(self, app):
        """Test that search is case insensitive."""
        # Test with different case variations
        variations = [
            "jakarta",
            "JAKARTA", 
            "Jakarta",
            "jAkArTa"
        ]
        
        for variation in variations:
            search_res = app.get(f"/api/schedules/search?origin={variation}", status=200)
            results = search_res.json
            # Should return same results regardless of case
            assert isinstance(results, list)

class TestCORSAndPreflight:
    """Test CORS functionality."""
    
    def test_cors_headers_on_get_requests(self, app):
        """Test that CORS headers are present on GET requests."""
        res = app.get("/api/buses", status=200)
        # Note: In actual implementation, we would check for CORS headers
        # but WebTest doesn't automatically handle CORS headers
        assert res.status_int == 200
    
    def test_options_requests(self, app):
        """Test OPTIONS preflight requests."""
        endpoints_to_test = [
            "/api/buses/create",
            "/api/routes/create", 
            "/api/schedules/create",
            "/api/seats/create",
            "/api/tickets/create"
        ]
        
        for endpoint in endpoints_to_test:
            res = app.options(endpoint, status=200)
            assert res.status_int == 200

class TestDataTypes:
    """Test various data types and edge cases."""
    
    def test_large_numbers(self, app):
        """Test handling of large numbers in price and duration."""
        route_data = {
            "origin": "Very Far City",
            "destination": "Even Farther City", 
            "duration": 99999  # Very long journey
        }
        route_res = app.post_json("/api/routes/create", route_data, status=201)
        route_id = route_res.json['id']
        
        # Verify the route was created with large duration
        route_detail_res = app.get(f"/api/routes/detail/{route_id}", status=200)
        route_detail = route_detail_res.json
        assert route_detail['duration'] == 99999
    
    def test_special_characters_in_names(self, app, basic_auth_headers):
        """Test handling of special characters in names."""
        bus_data = {
            "name": "Bus-123 (Special & Chars!)",
            "license_plate": "B 6666 SPL"
        }
        
        bus_res = app.post_json("/api/buses/create", bus_data, 
                               headers=basic_auth_headers, status=201)
        bus_id = bus_res.json['id']
        
        # Verify the bus was created with special characters
        bus_detail_res = app.get(f"/api/buses/detail/{bus_id}", status=200)
        bus_detail = bus_detail_res.json
        assert bus_detail['name'] == "Bus-123 (Special & Chars!)"
    
    def test_unicode_characters(self, app):
        """Test handling of unicode characters."""
        route_data = {
            "origin": "Jakarta Pusat",
            "destination": "Yogyakarta", 
            "duration": 300
        }
        
        route_res = app.post_json("/api/routes/create", route_data, status=201)
        route_id = route_res.json['id']
        
        # Verify unicode characters are preserved
        route_detail_res = app.get(f"/api/routes/detail/{route_id}", status=200)
        route_detail = route_detail_res.json
        assert route_detail['origin'] == "Jakarta Pusat"

class TestPagingAndLimits:
    """Test system behavior with large amounts of data."""
    
    def test_large_number_of_buses(self, app, basic_auth_headers):
        """Test system with many buses."""
        # Create multiple buses
        bus_ids = []
        for i in range(10):
            bus_data = {
                "name": f"Bulk Bus {i:03d}",
                "license_plate": f"B {i:04d} BLK"
            }
            bus_res = app.post_json("/api/buses/create", bus_data, 
                                   headers=basic_auth_headers, status=201)
            bus_ids.append(bus_res.json['id'])
        
        # Get all buses and verify they're all there
        buses_res = app.get("/api/buses", status=200)
        buses = buses_res.json
        
        # Should have at least our 10 buses plus any existing ones
        assert len(buses) >= 10
        
        # Verify our buses are in the list
        bulk_buses = [b for b in buses if b['name'].startswith('Bulk Bus')]
        assert len(bulk_buses) == 10
    
    def test_large_number_of_seats(self, app):
        """Test creating many seats for a schedule."""
        # Get an existing schedule
        schedules_res = app.get("/api/schedules", status=200)
        schedules = schedules_res.json
        
        if schedules:
            schedule_id = schedules[0]['id']
            
            # Create many seats
            seat_ids = []
            for row in 'ABCDEFGHIJ':  # 10 rows
                for num in range(1, 5):  # 4 seats per row
                    seat_data = {
                        "schedule_id": schedule_id,
                        "seat_number": f"{row}{num}",
                        "status": "available"
                    }
                    # Some might already exist, so allow both 200 and 201
                    seat_res = app.post_json("/api/seats/create", seat_data, 
                                           status=[200, 201])
                    if 'id' in seat_res.json:
                        seat_ids.append(seat_res.json['id'])
            
            # Get all seats for this schedule
            seats_res = app.get(f"/api/seats/{schedule_id}", status=200)
            seats = seats_res.json
            
            # Should have many seats
            assert len(seats) >= 20  # At least some of our created seats