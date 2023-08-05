"""
Interface to GomeStor (Gome Object Storage).
"""

from gyun.gomestor.connection import QSConnection


def connect(host, access_key_id=None, secret_access_key=None):
    """ Connect to gomestor by access key.
    """
    return QSConnection(access_key_id, secret_access_key, host)
