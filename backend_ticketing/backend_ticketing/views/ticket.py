from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPCreated
from backend_ticketing.models import Ticket
import uuid

@view_config(route_name='ticket_list', renderer='json', request_method='GET')
def get_tickets(request):
    tickets = request.dbsession.query(Ticket).all()
    return [
        {
            'id': t.id,
            'seat_id': t.seat_id,
            'customer_name': t.customer_name,
            'booking_code': t.booking_code,
            'status': t.status
        } for t in tickets
    ]

@view_config(route_name='ticket_create', renderer='json', request_method='POST')
def create_ticket(request):
    try:
        data = request.json_body
        ticket = Ticket(
            seat_id=data['seat_id'],
            customer_name=data['customer_name'],
            booking_code=str(uuid.uuid4())[:8].upper(),  # kode unik acak
            status='confirmed'
        )
        request.dbsession.add(ticket)
        request.dbsession.flush()
        return HTTPCreated(json_body={'message': 'Ticket created', 'booking_code': ticket.booking_code})
    except Exception as e:
        raise HTTPBadRequest(json_body={'error': str(e)})

@view_config(route_name='ticket_detail', renderer='json', request_method='GET')
def get_ticket(request):
    t = request.dbsession.get(Ticket, request.matchdict['id'])
    if not t:
        raise HTTPNotFound(json_body={'error': 'Ticket not found'})
    return {
        'id': t.id,
        'seat_id': t.seat_id,
        'customer_name': t.customer_name,
        'booking_code': t.booking_code,
        'status': t.status
    }

@view_config(route_name='ticket_update', renderer='json', request_method='PUT')
def update_ticket(request):
    t = request.dbsession.get(Ticket, request.matchdict['id'])
    if not t:
        raise HTTPNotFound(json_body={'error': 'Ticket not found'})

    data = request.json_body
    t.customer_name = data.get('customer_name', t.customer_name)
    t.status = data.get('status', t.status)
    return {'message': 'Ticket updated'}

@view_config(route_name='ticket_delete', renderer='json', request_method='DELETE')
def delete_ticket(request):
    t = request.dbsession.get(Ticket, request.matchdict['id'])
    if not t:
        raise HTTPNotFound(json_body={'error': 'Ticket not found'})
    request.dbsession.delete(t)
    return {'message': 'Ticket deleted'}
