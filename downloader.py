import yt_dlp
from config import YDL_OPTS

def clean_url(url):
    return url.strip()

def get_video_info(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        'title': info.get('title', '未知标题'), 
        'extractor': info.get('extractor', '未知平台')
    }

class VideoDownloader:
    def __init__(self, progress_callback):
        self.ydl_opts = YDL_OPTS.copy()
        self.ydl_opts['progress_hooks'] = [progress_callback]
    
    def download(self, url):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])