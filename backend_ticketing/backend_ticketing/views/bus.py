from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPCreated
from backend_ticketing.models import Bus
from pyramid.response import Response

import logging
import transaction
# ... (import lainnya dan model Bus) ...

log = logging.getLogger(__name__) # Pastikan ini ada


@view_config(route_name='bus_list', renderer='json', request_method='GET')
def get_buses(request):
    buses = request.dbsession.query(Bus).all()
    return [{"id": b.id, "name": b.name, "license_plate": b.license_plate} for b in buses]


from backend_ticketing.views.auth import check_basic_auth

@view_config(route_name='bus_create', renderer='json', request_method='POST')
def create_bus(request):
    check_basic_auth(request)  # ⬅️ Cek admin dulu

    data = request.json_body
    bus = Bus(name=data['name'], license_plate=data['license_plate'])
    request.dbsession.add(bus)
    request.dbsession.flush()
    return HTTPCreated(json_body={'message': 'Bus created', 'id': bus.id})

@view_config(route_name='bus_create', request_method='OPTIONS')
def bus_create_options(request):
    return Response(status=200)


@view_config(route_name='bus_detail', renderer='json', request_method='GET')
def get_bus(request):
    bus_id = request.matchdict.get('id')
    bus = request.dbsession.query(Bus).get(bus_id)
    if not bus:
        raise HTTPNotFound(json_body={'error': 'Bus not found'})
    return {'id': bus.id, 'name': bus.name, 'license_plate': bus.license_plate}


@view_config(route_name='bus_update', renderer='json', request_method='PUT')
def update_bus(request):
    bus_id = request.matchdict.get('id')
    log.info(f"=== UPDATE BUS START - ID: {bus_id} ===")
    
    # Debug session info
    log.info(f"Session type: {type(request.dbsession)}")
    log.info(f"Session bind: {request.dbsession.bind}")
    log.info(f"Transaction manager: {request.tm}")
    
    bus = request.dbsession.query(Bus).get(bus_id)
    if not bus:
        raise HTTPNotFound(json_body={'error': 'Bus not found'})

    log.info(f"ORIGINAL: name='{bus.name}', plate='{bus.license_plate}'")
    
    data = request.json_body
    log.info(f"UPDATE DATA: {data}")

    # Simpan nilai lama untuk perbandingan
    original_name = bus.name
    original_plate = bus.license_plate
    
    # Update attributes
    if 'name' in data:
        bus.name = data['name']
    if 'license_plate' in data:
        bus.license_plate = data['license_plate']
    
    log.info(f"UPDATED: name='{bus.name}', plate='{bus.license_plate}'")
    
    # Cek apakah benar-benar berubah
    name_changed = original_name != bus.name
    plate_changed = original_plate != bus.license_plate
    log.info(f"CHANGES: name_changed={name_changed}, plate_changed={plate_changed}")
    
    # Cek session state sebelum flush
    log.info(f"Session dirty before flush: {len(request.dbsession.dirty)} objects")
    log.info(f"Is bus dirty? {bus in request.dbsession.dirty}")
    
    # Flush untuk memastikan SQL dieksekusi
    try:
        request.dbsession.flush()
        log.info("FLUSH: Success")
    except Exception as e:
        log.error(f"FLUSH ERROR: {e}")
        raise
    
    # Verifikasi setelah flush (masih dalam transaksi yang sama)
    verify_bus = request.dbsession.query(Bus).get(bus_id)
    log.info(f"VERIFY AFTER FLUSH: name='{verify_bus.name}', plate='{verify_bus.license_plate}'")
    
    # TAMBAHAN: Cek apakah ada pending SQL
    log.info(f"Session new after flush: {len(request.dbsession.new)}")
    log.info(f"Session dirty after flush: {len(request.dbsession.dirty)}")
    
    log.info("=== UPDATE BUS END (Transaction will auto-commit) ===")
    
    return {
        'message': 'Bus updated', 
        'id': bus.id, 
        'updated_name': bus.name, 
        'updated_plate': bus.license_plate,
        'original_name': original_name,
        'original_plate': original_plate
    }


@view_config(route_name='bus_delete', renderer='json', request_method='DELETE')
def delete_bus(request):
    bus_id = request.matchdict.get('id')
    bus = request.dbsession.query(Bus).get(bus_id)
    if not bus:
        raise HTTPNotFound(json_body={'error': 'Bus not found'})

    request.dbsession.delete(bus)
    return {'message': 'Bus deleted'}
