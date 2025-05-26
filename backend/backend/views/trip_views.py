from cornice.resource import resource, view
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from ..models.schedule import Schedule
from ..models.booking import Booking, BookingStatus # Untuk cek kursi terpesan
from sqlalchemy import func
import datetime

# Untuk /api/trips/search
@resource(collection_path='/api/trips/search', name='trip_search_api', cors_enabled=True, cors_origins=['http://localhost:3000'])
class TripSearchAPI:
    def __init__(self, request, context=None):
        self.request = request
        self.dbsession = request.dbsession

    @view(renderer='json', request_method='GET')
    def collection_get(self):
        # Implementasi logika pencarian dari frontend/src/pages/SearchTrip.jsx
        # Ambil params: from, to, departure, passengers, class
        # Query ke tabel Schedule
        # Return hasil dalam format yang diharapkan frontend
        # Contoh:
        # from_loc = self.request.params.get('from')
        # ...
        # schedules = self.dbsession.query(Schedule).filter(...).all()
        # results = [...]
        return {'results': []} # Ganti dengan hasil sebenarnya

# Untuk /api/trips/search
@resource(
    collection_path='/api/trips/search',
    path='/api/trips/search',  # <-- TAMBAHKAN BARIS INI
    name='trip_search_api',
    cors_enabled=True,
    cors_origins=['http://localhost:3000']
)
class TripSearchAPI:
    def __init__(self, request, context=None):
        self.request = request
        self.dbsession = request.dbsession

    @view(renderer='json', request_method='GET')
    def collection_get(self): # Perhatikan ini adalah collection_get, bukan get
        # Implementasi logika pencarian dari frontend/src/pages/SearchTrip.jsx
        # Ambil params: from, to, departure, passengers, class
        # Query ke tabel Schedule
        # Return hasil dalam format yang diharapkan frontend
        # Contoh:
        # from_loc = self.request.params.get('from')
        # ...
        # schedules = self.dbsession.query(Schedule).filter(...).all()
        # results = [...]
        print("DEBUG: TripSearchAPI collection_get called") # Tambahkan untuk debugging
        return {'results': [], 'message': 'Search endpoint hit, implement logic'} # Ganti dengan hasil sebenarnya


# Untuk /api/trips/{trip_id}/seats
@resource(collection_path='/api/trips/search', name='trip_search_api', cors_enabled=True, cors_origins=['http://localhost:3000'])
class TripSearchAPI:
    def __init__(self, request, context=None):
        self.request = request
        self.dbsession = request.dbsession

    @view(renderer='json')
    def get(self):
        trip_id = self.request.matchdict.get('trip_id')
        if not trip_id:
            return HTTPBadRequest(json_body={'error': 'trip_id is required'})

        try:
            trip_id_int = int(trip_id)
        except ValueError:
            return HTTPBadRequest(json_body={'error': 'trip_id must be an integer'})
        
        print(f"DEBUG: TripSeatsAPI get called for trip_id: {trip_id_int}") # Tambahkan untuk debugging

        # Implementasi dari frontend/src/pages/SelectSeat.jsx
        # Query ke tabel Booking untuk kursi yang sudah terisi pada schedule_id (trip_id)
        booked_seats_query = self.dbsession.query(Booking.seat_number)\
            .filter_by(schedule_id=trip_id_int)\
            .filter(Booking.status.in_([BookingStatus.PAID, BookingStatus.PENDING]))
        
        booked_seats = [item[0] for item in booked_seats_query.all()]
        
        return {'bookedSeats': booked_seats}