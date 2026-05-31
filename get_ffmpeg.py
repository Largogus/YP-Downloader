import sys
import os


def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
        return os.path.join(base, "ffmpeg", "bin")

    return "ffmpeg/bin"