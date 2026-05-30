from pathlib import Path
import re
from urllib.parse import urlparse
import eel
import yt_dlp as y


eel.init("web")


def is_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


# def progress_hook(d):
#     if d['status'] == 'downloading':
#         percent = d.get('_percent_str', '0%')
#
#         eel.update_progress(percent)


@eel.expose
def download_video(url, quality: str):
    try:
        state_url = is_url(url)
        eel.error_url(state_url)

        if not state_url:
            return

        eel.showModal()

        downloads = str(Path.home() / "Downloads")
        height = int(re.search(r'\d+', quality).group())

        ydl_opts = {
            "outtmpl": f'{downloads}/%(title)s.%(ext)s',
            "format": f"bestvideo[height<={height}]+bestaudio/best[ext=m4a]/best",
            'noplaylist': True,
            'quiet': False,
            'geo_bypass': True,
            "retries": 10,
            "fragment_retries": 10,
            "http_headers": {
                "User-Agent": "Mozilla/5.0"
            },
            "merge_output_format": "mp4",
            "ffmpeg_location": "ffmpeg/bin",
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"
            }],
            "nopart": False,
            "overwrites": False,
            "proxy": "http://144.79.35.11:3125",
            # "progress_hooks": [progress_hook],
        }

        with y.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        eel.hideModal()

        return {"success": True}
    except Exception as e:
        eel.showError()
        return {"success": False, "error": str(e)}


eel.start(
    "index.html",
    disable_cache=True,
    size=(1000, 500)
)