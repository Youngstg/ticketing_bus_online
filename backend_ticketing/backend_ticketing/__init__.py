from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny, Authenticated, Everyone, ALL_PERMISSIONS

from .security import MyBasicAuthPolicy # Import kebijakan baru Anda

# Definisikan RootFactory untuk ACL dasar
# Ini menentukan siapa yang memiliki izin apa secara default
class RootFactory:
    __acl__ = [
        (Allow, Authenticated, 'api_access'),  # Pengguna terautentikasi memiliki izin 'api_access'
        # (Allow, 'role:admin', 'admin_tasks'), # Contoh untuk izin admin
        # (Deny, Everyone, ALL_PERMISSIONS) # Jika Anda ingin lebih ketat, tapi default_permission lebih mudah
    ]

    def __init__(self, request):
        pass

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings, root_factory=RootFactory) as config:
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.include('.cors') # Pastikan CORS mengizinkan header 'Authorization'

        # Konfigurasi session (mungkin masih digunakan untuk bagian lain)
        session_secret = settings.get('pyramid.secret_key', 'defaultsecretkey') # Ganti dengan secret key yang kuat
        session_factory = SignedCookieSessionFactory(
            session_secret,
            secure=settings.get('pyramid.session.secure', 'true').lower() == 'true',
            httponly=settings.get('pyramid.session.httponly', 'true').lower() == 'true',
            samesite=settings.get('pyramid.session.samesite', 'Lax'),
            timeout=43200, # 12 jam, contoh
            reissue_time=4320 # 10% dari timeout
        )
        config.set_session_factory(session_factory)

        # Konfigurasi Kebijakan Autentikasi dan Otorisasi
        authn_policy = MyBasicAuthPolicy(realm="Ticketing API")
        authz_policy = ACLAuthorizationPolicy()

        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        config.set_default_permission('api_access')

        config.scan()
    return config.make_wsgi_app()