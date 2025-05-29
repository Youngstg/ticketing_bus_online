from pyramid.events import NewRequest, subscriber
from pyramid.response import Response

@subscriber(NewRequest)
def add_cors_headers(event):
    """Add CORS headers to all responses"""
    def cors_response_callback(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true',
        })
    event.request.add_response_callback(cors_response_callback)

def cors_preflight_view(request):
    """Handle OPTIONS preflight requests"""
    return Response(
        status=200,
        headers={
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true',
        }
    )

def includeme(config):
    """Configure CORS for the application"""
    # Add the subscriber for automatic CORS headers
    config.scan(__name__)  # This will pick up the @subscriber decorator
    
    # Handle preflight OPTIONS requests
    config.add_route('cors_preflight', '/{path:.*}')
    config.add_view(cors_preflight_view, route_name='cors_preflight', request_method='OPTIONS')