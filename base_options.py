def base_opts(downloads_path, ffmpeg):
    return {
        "outtmpl": str(downloads_path / "%(title).150B [%(id)s].%(ext)s"),
        "windowsfilenames": True,
        "noplaylist": True,
        "merge_output_format": "mp4",
        "retries": 5,
        "fragment_retries": 10,
        "socket_timeout": 15,
        "ffmpeg_location": ffmpeg,
        "quiet": False,
        "verbose": True,
        "noprogress": True,
        "postprocessor_args": {"merger": ["-movflags", "+faststart"]},
    }