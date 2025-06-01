def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    # AUTH ROUTES
    config.add_route('login', '/api/auth/login')
    config.add_route('register', '/api/auth/register')
    config.add_route('logout', '/api/auth/logout')

    # BUSES
    config.add_route('bus_list', '/api/buses')                    # GET semua
    config.add_route('bus_create', '/api/buses/create')           # POST baru
    config.add_route('bus_detail', '/api/buses/detail/{id}')      # GET satu
    config.add_route('bus_update', '/api/buses/update/{id}')      # PUT
    config.add_route('bus_delete', '/api/buses/delete/{id}')      # DELETE

    # ROUTES
    config.add_route('route_list', '/api/routes')
    config.add_route('route_create', '/api/routes/create')
    config.add_route('route_detail', '/api/routes/detail/{id}')
    config.add_route('route_update', '/api/routes/update/{id}')
    config.add_route('route_delete', '/api/routes/delete/{id}')

    # SCHEDULES
    config.add_route('schedule_list', '/api/schedules')
    config.add_route('schedule_create', '/api/schedules/create')
    config.add_route('schedule_detail', '/api/schedules/detail/{id}')
    config.add_route('schedule_update', '/api/schedules/update/{id}')
    config.add_route('schedule_delete', '/api/schedules/delete/{id}')
    config.add_route('schedule_search', '/api/schedules/search')

    # SEATS
    config.add_route('seat_list', '/api/seats/{schedule_id}')
    config.add_route('seat_create', '/api/seats/create')
    config.add_route('seat_detail', '/api/seats/detail/{id}')
    config.add_route('seat_update', '/api/seats/update/{id}')
    config.add_route('seat_delete', '/api/seats/delete/{id}')

    # TICKETS
    config.add_route('ticket_list', '/api/tickets')
    config.add_route('ticket_create', '/api/tickets/create')
    config.add_route('ticket_detail', '/api/tickets/detail/{id}')
    config.add_route('ticket_update', '/api/tickets/update/{id}')
    config.add_route('ticket_delete', '/api/tickets/delete/{id}')