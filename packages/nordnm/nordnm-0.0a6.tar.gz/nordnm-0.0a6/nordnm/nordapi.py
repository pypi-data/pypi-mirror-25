import requests
from operator import itemgetter
import logging

API_ADDR = 'https://api.nordvpn.com'
TIMEOUT = 5

HEADERS = {
    'User-Agent': 'NordVPN_Client_5.56.780.0',
    'Host': 'api.nordvpn.com',
    'Connection': 'Close'
}

# Mapping of NordVPN category names to their short internal names
VPN_CATEGORIES = {
    'Standard VPN servers': 'normal',
    'P2P': 'p2p',
    'Double VPN': 'double',
    'Dedicated IP servers': 'dedicated',
    'Onion over VPN': 'onion',
    'Anti DDoS': 'ddos',
}

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.CRITICAL)  # Small hack to hide info logs from requests


def get_server_list(sort_by_load=False):
    try:
        resp = requests.get(API_ADDR + '/server', headers=HEADERS, timeout=TIMEOUT)
        server_list = resp.json()

        if sort_by_load:
            return sorted(server_list, key=itemgetter('load'))
        else:
            return server_list
    except Exception as ex:
        logger.error(ex)
        return None


def get_nameservers():
    return ['162.242.211.137', '78.46.223.24']

    # Apparently this is not the standard DNS endpoint, but something to do with 'smart-play' and no longer provides valid nameservers
    # so for now we will just return a static list...
    """
    try:
        resp = requests.get(API_ADDR + '/dns/smart', headers=HEADERS, timeout=TIMEOUT)
        return resp.json()
    except Exception as ex:
        logger.error(ex)
        return None
    """


def get_configs():
    try:
        resp = requests.get(API_ADDR + '/files/zipv2', headers=HEADERS, timeout=TIMEOUT)
        return resp.content
    except Exception as ex:
        logger.error(ex)
        return None
