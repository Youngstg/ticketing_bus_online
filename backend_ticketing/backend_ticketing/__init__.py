from pyramid.config import Configurator
from pyramid.events import NewRequest



def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        })
        return response
    event.request.add_response_callback(cors_headers)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('pyramid_tm')  # penting untuk commit otomatis
        config.include('.routes')
        config.include('.models')     # akan menjalankan models.includeme
        config.scan('backend_ticketing.views')

        def add_cors_headers_response_callback(event):
            def cors_headers(request, response):
                response.headers.update({
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                })
                return response
            event.request.add_response_callback(cors_headers)

        config.add_subscriber(add_cors_headers_response_callback, NewRequest)
        config.set_default_permission(None)

    return config.make_wsgi_app()


