from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('pyramid_tm')
        config.include('.routes')
        config.include('.models')
        
        # Include CORS handling (this will run the includeme function in cors.py)
        config.include('.cors')  # Assuming your cors.py is in the same package
        
        config.scan('backend_ticketing.views')
        config.set_default_permission(None)

    return config.make_wsgi_app()