import requests


def get_proxy():
    url = "https://raw.githubusercontent.com/Largogus/yt-downloader/refs/heads/master/config.json"

    _proxy = requests.get(url).json()

    return _proxy['proxy']