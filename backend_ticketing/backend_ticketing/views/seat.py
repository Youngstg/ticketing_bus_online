from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPCreated
from backend_ticketing.models import Seat

@view_config(route_name='seat_list', renderer='json', request_method='GET')
def get_seats(request):
    schedule_id = request.matchdict.get('schedule_id')
    seats = request.dbsession.query(Seat).filter_by(schedule_id=schedule_id).all()
    return [
        {
            'id': s.id, 
            'seat_number': s.seat_number, 
            'is_booked': s.is_booked,
            'status': 'booked' if s.is_booked else 'available'
        } 
        for s in seats
    ]

@view_config(route_name='seat_create', renderer='json', request_method='POST')
def create_seat(request):
    try:
        data = request.json_body
        
        # Cek apakah kursi sudah ada
        existing_seat = request.dbsession.query(Seat).filter_by(
            schedule_id=data['schedule_id'],
            seat_number=data['seat_number']
        ).first()
        
        if existing_seat:
            # Update status kursi yang sudah ada
            existing_seat.is_booked = data.get('status') == 'booked'
            request.dbsession.flush()
            return {
                'message': 'Seat status updated', 
                'id': existing_seat.id,
                'seat_number': existing_seat.seat_number,
                'is_booked': existing_seat.is_booked
            }
        else:
            # Buat kursi baru
            seat = Seat(
                schedule_id=data['schedule_id'],
                seat_number=data['seat_number'],
                is_booked=data.get('status') == 'booked'
            )
            request.dbsession.add(seat)
            request.dbsession.flush()
            return HTTPCreated(json_body={
                'message': 'Seat created', 
                'id': seat.id,
                'seat_number': seat.seat_number,
                'is_booked': seat.is_booked
            })
            
    except Exception as e:
        raise HTTPBadRequest(json_body={'error': str(e)})
    
@view_config(route_name='seat_create', renderer='json', request_method='OPTIONS')
def seat_create_options(request):
    return {}

@view_config(route_name='seat_detail', renderer='json', request_method='GET')
def get_seat(request):
    s = request.dbsession.get(Seat, request.matchdict['id'])
    if not s:
        raise HTTPNotFound(json_body={'error': 'Seat not found'})
    return {
        'id': s.id,
        'schedule_id': s.schedule_id,
        'seat_number': s.seat_number,
        'is_booked': s.is_booked
    }

@view_config(route_name='seat_update', renderer='json', request_method='PUT')
def update_seat(request):
    s = request.dbsession.get(Seat, request.matchdict['id'])
    if not s:
        raise HTTPNotFound(json_body={'error': 'Seat not found'})

    data = request.json_body
    s.seat_number = data.get('seat_number', s.seat_number)
    s.is_booked = data.get('is_booked', s.is_booked)
    return {'message': 'Seat updated'}

@view_config(route_name='seat_delete', renderer='json', request_method='DELETE')
def delete_seat(request):
    s = request.dbsession.get(Seat, request.matchdict['id'])
    if not s:
        raise HTTPNotFound(json_body={'error': 'Seat not found'})
    request.dbsession.delete(s)
    return {'message': 'Seat deleted'}