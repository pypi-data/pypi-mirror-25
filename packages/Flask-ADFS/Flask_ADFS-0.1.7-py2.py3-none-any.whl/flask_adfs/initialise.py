from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from flask_login import LoginManager

_public_key = None
login_mgr = LoginManager()
adfs_access = {}


def pk():
    return _public_key


def adfs_init(app):
    global _public_key
    global login_mgr
    login_mgr.init_app(app)
    login_mgr.session_protection = "strong"
    try:
        with open(app.config.get('ADFS_CERT_LOCATION')) as cert:
            cert_str = cert.read().encode()
        # extract public key
        cert_obj = load_pem_x509_certificate(cert_str, default_backend())
        _public_key = cert_obj.public_key()
        app.logger.debug('ADFS public key cached')
    except:
        app.logger.error('Could not get ADFS public key')

def set_access(access):
    global adfs_access
    adfs_access = access


def get_access():
    global adfs_access
    return adfs_access
