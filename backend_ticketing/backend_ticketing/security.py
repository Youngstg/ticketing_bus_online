# backend_ticketing/backend_ticketing/security.py
import base64
import binascii
import bcrypt
from pyramid.authentication import IAuthenticationPolicy
from pyramid.security import Authenticated, Everyone
from zope.interface import implementer

from .models import User  # Sesuaikan path jika model Anda ada di tempat lain

def get_user_by_username(request, username):
    """Mendapatkan user dari database berdasarkan username."""
    try:
        return request.dbsession.query(User).filter_by(username=username).first()
    except Exception: # Tangani jika dbsession belum ada di request (misalnya saat testing awal)
        return None

def get_user_by_id(request, userid_str):
    """Mendapatkan user dari database berdasarkan ID."""
    try:
        userid = int(userid_str)
        return request.dbsession.query(User).get(userid)
    except (ValueError, TypeError, Exception):
        return None

@implementer(IAuthenticationPolicy)
class MyBasicAuthPolicy:
    def __init__(self, realm="Protected API"):
        self.realm = realm

    def _get_credentials(self, request):
        """Mengekstrak username dan password dari header Authorization."""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            scheme, credentials = auth_header.split(' ', 1)
            if scheme.lower() != 'basic':
                return None
            
            decoded_credentials = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            return username, password
        except (ValueError, binascii.Error, UnicodeDecodeError):
            # Header atau kredensial tidak valid
            return None

    def authenticated_userid(self, request):
        """
        Memverifikasi kredensial dan mengembalikan userid jika valid.
        Userid di sini adalah ID user dari database.
        """
        creds = self._get_credentials(request)
        if creds is None:
            return None
        
        username, password = creds
        user = get_user_by_username(request, username)
        
        if user and user.password_hash and \
           bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            request.user = user # Menyimpan objek user di request untuk penggunaan selanjutnya jika perlu
            return str(user.id) # Pyramid mengharapkan userid sebagai string
        return None

    def unauthenticated_userid(self, request):
        """
        Mengembalikan userid yang diklaim (tanpa verifikasi password penuh di sini),
        atau None jika tidak ada header yang sesuai.
        Metode authenticated_userid akan melakukan verifikasi password.
        """
        creds = self._get_credentials(request)
        if creds:
            username, _ = creds
            # Cukup kembalikan username sebagai klaim awal, atau ID jika ditemukan
            # Untuk konsistensi dengan authenticated_userid, kita bisa cari user ID
            user = get_user_by_username(request, username)
            if user:
                return str(user.id)
        return None
        

    def effective_principals(self, request):
        """
        Mengembalikan daftar principal untuk request saat ini.
        Ini termasuk Everyone, dan jika terautentikasi, Authenticated, userid, dan role.
        """
        principals = [Everyone]
        userid = self.authenticated_userid(request) # Ini akan memanggil verifikasi
        
        if userid is not None:
            principals.append(Authenticated)
            principals.append(userid) # User ID sebagai principal
            
            # Mengambil user dari request.user jika sudah di-set oleh authenticated_userid
            # atau mengambil ulang dari DB.
            user = getattr(request, 'user', None)
            if not user: # Fallback jika request.user belum di-set
                 user = get_user_by_id(request, userid)

            if user and user.role:
                principals.append(f'role:{user.role}') # Contoh: 'role:admin', 'role:user'
        return principals

    def remember(self, request, userid, **kw):
        """
        HTTP Basic Auth bersifat stateless, jadi 'remember' tidak melakukan apa-apa
        (tidak ada cookie yang di-set).
        """
        return []

    def forget(self, request, **kw):
        """
        Mengembalikan header untuk "menantang" klien (menyebabkan browser memunculkan dialog login).
        Ini akan dipanggil oleh Pyramid saat akses ditolak (misalnya, HTTPUnauthorized).
        """
        return [('WWW-Authenticate', f'Basic realm="{self.realm}"')]