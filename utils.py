# utils.py
import os
import yt_dlp

def download_reel(url: str, download_path: str = "downloads") -> str:
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title).30s.%(ext)s'),
        'format': 'mp4',
        'quiet': True,
        'cookies': 'cookies.txt'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename
