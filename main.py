import os, sys, threading, webbrowser, re
from pathlib import Path
from urllib.parse import urlparse
import eel
import yt_dlp as y
from base_options import base_opts
from build_format import build_format
from error import get_error
from get_deno import get_deno
from get_ffmpeg import get_ffmpeg_path
from proxy import get_proxy, proxy_alive

eel.init("web")

DOWNLOADS = Path.home() / "Downloads"
QUALITY_MAP = {
    "8k": 4320,
    "4k": 2160,
    "2k": 1440,
    "full hd": 1080,
    "hd": 720,
    "лучшее": 4320,
    "best": 4320,
    "максимальное": 4320,
}

deno = get_deno()

_busy = threading.Lock()

SITES = {
    "youtube": ("youtube.com", "youtu.be", "youtube-nocookie.com"),
    "pinterest": (
        "pinterest.com", "pinterest.ru", "pinterest.co.uk",
        "pinterest.de", "pinterest.fr", "pinterest.es",
        "pinterest.it", "pin.it",
    ),
}


def is_url(url: str) -> bool:
    parsed = urlparse(url or "")
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def get_site(url):
    host = (urlparse(url or "").hostname or "").lower()
    for site, domains in SITES.items():
        if any(host == d or host.endswith("." + d) for d in domains):
            return site
    return None


def _to_height(height: str):
    height = (height or "").strip().lower()
    if height in QUALITY_MAP:
        return QUALITY_MAP[height]

    m = re.search(r"(\d{3,4})\s*p\b", height)
    if m:
        return int(m.group(1))

    for key, h in QUALITY_MAP.items():
        if re.search(rf"\b{re.escape(key)}\b", height):
            return h

    return None


def fail(e):
    code, desc = get_error(e)
    return {"success": False, "error": f"{code} ({desc})"}


@eel.expose
def validate_download(url, quality):
    try:
        url = (url or "").strip()
        if url == "test":
            return {"success": True}
        if not is_url(url) or not get_site(url):
            return {"success": False, "error": "E-7001 (Ссылка не поддерживается.)"}
        if _to_height(quality) is None:
            return {"success": False, "error": "E-4002 (Не найдено доступных форматов.)"}
        return {"success": True}
    except Exception as e:
        return fail(e)


@eel.expose
def download_video(url, quality: str):
    if not _busy.acquire(blocking=False):
        return {"success": False, "error": "Уже идёт другая загрузка."}

    proxy = None

    try:
        url = (url or "").strip()
        site = get_site(url) if is_url(url) else None
        height = _to_height(quality)

        if not site:
            return {"success": False, "error": "E-7001 (Ссылка не поддерживается.)"}
        if height is None:
            return {"success": False, "error": "E-4002 (Не найдено доступных форматов.)"}

        opts = base_opts(DOWNLOADS, get_ffmpeg_path())

        if site == "youtube":
            opts["format"] = build_format(height)

            proxy = get_proxy()
            proxy = proxy if proxy_alive(proxy) else None
            opts["proxy"] = proxy

            if deno:
                opts["js_runtimes"] = {"deno": {"path": deno}}
        else:  # Pinterest
            opts["http_headers"] = {"User-Agent": "Mozilla/5.0"}

        with y.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)

        title = (info or {}).get("title")
        return {"success": True, "title": title}

    except y.utils.DownloadError as e:
        return fail(e)
    except Exception as e:
        return fail(e)
    finally:
        _busy.release()


@eel.expose
def open_tab(url):
    if is_url(url):
        webbrowser.open_new_tab(url)


@eel.expose
def open_downloads():
    if sys.platform == "win32":
        os.startfile(DOWNLOADS)


def main():
    kwargs = dict(disable_cache=True, size=(1000, 610))
    try:
        eel.start("index.html", **kwargs)
    except EnvironmentError:
        eel.start("index.html", mode="edge", **kwargs)


if __name__ == "__main__":
    main()