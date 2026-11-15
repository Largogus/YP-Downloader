import socket
from urllib.parse import urlparse
import requests


def get_proxy():
    url = "https://raw.githubusercontent.com/Largogus/yt-downloader/refs/heads/master/config.json"
    _proxy = requests.get(url).json()

    return _proxy['proxy']


def proxy_alive(proxy, timeout=5) -> bool:
    if not proxy:
        return False
    p = urlparse(proxy)
    try:
        with socket.create_connection((p.hostname, p.port), timeout=timeout):
            return True
    except (OSError, TypeError, ValueError):
        return False