from pyramid.httpexceptions import HTTPUnauthorized, HTTPForbidden
import base64

# Admin credentials yang bisa kamu ganti nanti
ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'
}

def check_basic_auth(request):
    """
    Validasi HTTP Basic Auth untuk akses admin.

    - Jika tidak ada Authorization header → 401
    - Jika format salah → 401
    - Jika username/password salah → 403
    - Jika cocok → return True
    """

    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.lower().startswith('basic '):
        raise HTTPUnauthorized(headers={'WWW-Authenticate': 'Basic realm="Admin Area"'})

    try:
        # Decode base64 username:password
        encoded = auth_header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        username, password = decoded.split(':', 1)
    except Exception:
        raise HTTPUnauthorized(json_body={'error': 'Invalid Authorization header format'})

    if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
        return True

    raise HTTPForbidden(json_body={'error': 'Invalid credentials'})
