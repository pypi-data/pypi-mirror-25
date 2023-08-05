"""
interface to the IaaS service from GYUN.
"""

from gyun.iaas.connection import APIConnection


def connect_to_zone(zone, access_key_id, secret_access_key, lowercase=True):
    """ Connect to one of zones in gyun by access key.
    """
    if lowercase:
        zone = zone.strip().lower()
    return APIConnection(access_key_id, secret_access_key, zone)
