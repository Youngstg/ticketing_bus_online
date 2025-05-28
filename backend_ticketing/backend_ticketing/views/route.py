from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPCreated
from backend_ticketing.models import Route

@view_config(route_name='route_list', renderer='json', request_method='GET')
def get_routes(request):
    routes = request.dbsession.query(Route).all()
    return [
        {'id': r.id, 'origin': r.origin, 'destination': r.destination, 'duration': r.duration}
        for r in routes
    ]

@view_config(route_name='route_create', renderer='json', request_method='POST')
def create_route(request):
    try:
        data = request.json_body
        route = Route(
            origin=data['origin'],
            destination=data['destination'],
            duration=data['duration']
        )
        request.dbsession.add(route)
        request.dbsession.flush()
        return HTTPCreated(json_body={'message': 'Route created', 'id': route.id})
    except Exception as e:
        raise HTTPBadRequest(json_body={'error': str(e)})

@view_config(route_name='route_detail', renderer='json', request_method='GET')
def get_route(request):
    id = request.matchdict['id']
    route = request.dbsession.get(Route, id)
    if not route:
        raise HTTPNotFound(json_body={'error': 'Route not found'})
    return {
        'id': route.id,
        'origin': route.origin,
        'destination': route.destination,
        'duration': route.duration
    }

@view_config(route_name='route_update', renderer='json', request_method='PUT')
def update_route(request):
    id = request.matchdict['id']
    route = request.dbsession.get(Route, id)
    if not route:
        raise HTTPNotFound(json_body={'error': 'Route not found'})
    
    data = request.json_body
    route.origin = data.get('origin', route.origin)
    route.destination = data.get('destination', route.destination)
    route.duration = data.get('duration', route.duration)
    return {'message': 'Route updated'}

@view_config(route_name='route_delete', renderer='json', request_method='DELETE')
def delete_route(request):
    id = request.matchdict['id']
    route = request.dbsession.get(Route, id)
    if not route:
        raise HTTPNotFound(json_body={'error': 'Route not found'})
    request.dbsession.delete(route)
    return {'message': 'Route deleted'}
