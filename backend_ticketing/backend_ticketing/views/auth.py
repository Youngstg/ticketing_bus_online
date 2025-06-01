from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import NO_PERMISSION_REQUIRED # Import ini
import bcrypt
import json
from sqlalchemy.exc import IntegrityError
from ..models import User, DBSession # Sesuaikan path jika perlu

# ... (kode lainnya jika ada) ...

@view_config(route_name='login', request_method='POST', renderer='json', permission=NO_PERMISSION_REQUIRED)
def login_view(request):
    # ... (isi fungsi login Anda saat ini)
    # Fungsi login ini mungkin masih relevan jika Anda ingin Basic Auth untuk API
    # dan session auth untuk interaksi web UI admin (jika ada),
    # atau jika Anda ingin Basic Auth me-return token sesi.
    # Untuk API murni Basic Auth, endpoint login ini mungkin tidak diperlukan
    # jika klien selalu mengirim header Authorization.
    # Namun, jika klien (frontend) mendapatkan username/password lalu menggunakannya
    # untuk Basic Auth di request berikutnya, maka ini tetap relevan untuk validasi awal.
    try:
        data = request.json_body
        username = data.get('username')
        password = data.get('password')
    except json.JSONDecodeError:
        request.response.status_code = 400
        return {'error': 'Invalid JSON'}

    if not username or not password:
        request.response.status_code = 400
        return {'error': 'Username and password are required'}

    user = request.dbsession.query(User).filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        # Untuk Basic Auth murni, kita tidak perlu session di sini.
        # Klien akan mengirim header Authorization di setiap request.
        # request.session['user_id'] = user.id
        # request.session.flash('Logged in successfully!', 'success')
        return {
            'message': 'Login successful (Basic Auth credentials can now be used)',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }
    else:
        request.response.status_code = 401
        return {'error': 'Invalid username or password'}


@view_config(route_name='register', request_method='POST', renderer='json', permission=NO_PERMISSION_REQUIRED)
def register_view(request):
    # ... (isi fungsi register Anda saat ini)
    try:
        data = request.json_body
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'user') # Default role 'user'
    except json.JSONDecodeError:
        request.response.status_code = 400
        return {'error': 'Invalid JSON'}

    if not username or not password or not email:
        request.response.status_code = 400
        return {'error': 'Username, password, and email are required'}

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    new_user = User(
        username=username,
        password_hash=hashed_password.decode('utf-8'), # Simpan sebagai string
        email=email,
        role=role
    )
    
    try:
        request.dbsession.add(new_user)
        request.dbsession.flush() # Untuk mendapatkan ID user jika diperlukan segera
        # Biasanya, flush terjadi sebelum commit oleh transaction manager.
        # Untuk API, commit/rollback biasanya diurus oleh transaction manager (seperti pyramid_tm)
        # atau secara manual jika tidak menggunakan transaction manager.
        return {
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'role': new_user.role
            }
        }
    except IntegrityError:
        request.dbsession.rollback()
        request.response.status_code = 409 # Conflict
        return {'error': 'Username or email already exists'}
    except Exception as e:
        request.dbsession.rollback()
        request.response.status_code = 500
        return {'error': f'An internal error occurred: {str(e)}'}


@view_config(route_name='logout', request_method='POST', renderer='json', permission=NO_PERMISSION_REQUIRED)
def logout_view(request):
    # Untuk Basic Auth, logout sejati terjadi di sisi klien (berhenti mengirim header).
    # Jika Anda juga menggunakan sesi, Anda bisa menginvalidasi sesi di sini.
    if 'user_id' in request.session:
        request.session.invalidate()
        return {'message': 'Session invalidated. For Basic Auth, client must stop sending Authorization header.'}
    return {'message': 'No active session to invalidate. For Basic Auth, client must stop sending Authorization header.'}