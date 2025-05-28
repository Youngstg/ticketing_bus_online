from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPCreated
from backend_ticketing.models import Schedule, Bus, Route
from sqlalchemy.sql import cast
from sqlalchemy.types import Date



@view_config(route_name='schedule_list', renderer='json', request_method='GET')
def get_schedules(request):
    schedules = request.dbsession.query(Schedule).all()
    return [
        {
            'id': s.id,
            'bus_id': s.bus_id,
            'route_id': s.route_id,
            'departure_time': s.departure_time.isoformat()
        } for s in schedules
    ]

@view_config(route_name='schedule_create', renderer='json', request_method='POST')
def create_schedule(request):
    try:
        data = request.json_body
        schedule = Schedule(
            bus_id=data['bus_id'],
            route_id=data['route_id'],
            departure_time=data['departure_time'],  # Pastikan ISO 8601 format
            price=data['price']
        )
        request.dbsession.add(schedule)
        request.dbsession.flush()
        return HTTPCreated(json_body={'message': 'Schedule created', 'id': schedule.id})
    except Exception as e:
        raise HTTPBadRequest(json_body={'error': str(e)})

@view_config(route_name='schedule_detail', renderer='json', request_method='GET')
def get_schedule(request):
    s = request.dbsession.get(Schedule, request.matchdict['id'])
    if not s:
        raise HTTPNotFound(json_body={'error': 'Schedule not found'})
    return {
        'id': s.id,
        'bus_id': s.bus_id,
        'route_id': s.route_id,
        'departure_time': s.departure_time.isoformat()
    }

@view_config(route_name='schedule_update', renderer='json', request_method='PUT')
def update_schedule(request):
    s = request.dbsession.get(Schedule, request.matchdict['id'])
    if not s:
        raise HTTPNotFound(json_body={'error': 'Schedule not found'})

    data = request.json_body
    s.bus_id = data.get('bus_id', s.bus_id)
    s.route_id = data.get('route_id', s.route_id)
    s.departure_time = data.get('departure_time', s.departure_time)
    return {'message': 'Schedule updated'}

@view_config(route_name='schedule_delete', renderer='json', request_method='DELETE')
def delete_schedule(request):
    s = request.dbsession.get(Schedule, request.matchdict['id'])
    if not s:
        raise HTTPNotFound(json_body={'error': 'Schedule not found'})
    request.dbsession.delete(s)
    return {'message': 'Schedule deleted'}

@view_config(route_name='schedule_search', renderer='json', request_method='GET')
def search_schedules(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    query = request.dbsession.query(Schedule).join(Bus).join(Route)

    if origin:
        query = query.filter(Route.origin.ilike(f"%{origin}%"))
    if destination:
        query = query.filter(Route.destination.ilike(f"%{destination}%"))
    if date:
        query = query.filter(cast(Schedule.departure_time, Date) == date)

    results = query.all()

    return [
        {
            'id': s.id,
            'bus': s.bus.name,
            'origin': s.route.origin,
            'destination': s.route.destination,
            'departure_time': s.departure_time.isoformat(),
            'duration': s.route.duration,  # asumsi `duration` ada di Route (bukan Schedule)
            'price': s.price, # asumsi harga per rute (bisa juga pindahkan ke Schedule jika perlu)
        }
        for s in results
    ]

