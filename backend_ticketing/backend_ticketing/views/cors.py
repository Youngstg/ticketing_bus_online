from pyramid.view import view_config
from pyramid.response import Response


@view_config(request_method='OPTIONS', route_name='bus_create')
def bus_create_options(request):
    return Response(status=200)


@view_config(route_name='route_create', request_method='OPTIONS')
def route_create_options(request):
    return Response(status=200)

@view_config(route_name='schedule_create', request_method='OPTIONS')
def schedule_create_options(request):
    return Response(status=200)

@view_config(route_name='seat_create', request_method='OPTIONS')
def seat_create_options(request):
    return Response(status=200)



