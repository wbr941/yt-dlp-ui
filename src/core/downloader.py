import yt_dlp
from typing import Dict, Any, Callable
import re

class VideoDownloader:
    def __init__(self, progress_callback: Callable[[Dict[str, Any]], None]):
        self.progress_callback = progress_callback
        self.download_info = {
            'video': {'size': 0, 'downloaded': 0, 'done': False},
            'audio': {'size': 0, 'downloaded': 0, 'done': False},
            'is_split': False,  # 是否是分离的视频和音频
            'merging': False
        }
        
    def _format_size(self, bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024
        return f"{bytes:.1f}TB"
        
    def _progress_hook(self, d: Dict[str, Any]) -> None:
        """处理下载进度回调"""
        try:
            status = d['status']
            
            if status == 'downloading':
                # 获取格式信息
                format_id = str(d.get('info_dict', {}).get('format_id', ''))
                
                # 第一次下载时确定是否是分离的视频和音频
                if not self.download_info['is_split']:
                    self.download_info['is_split'] = '+' in format_id
                
                # 确定当前下载的是视频还是音频
                current_type = 'video' if 'video' in format_id else 'audio'
                
                # 更新大小信息
                total_bytes = d.get('total_bytes', 0)
                if total_bytes == 0:
                    total_bytes = d.get('total_bytes_estimate', 0)
                
                if total_bytes > 0:
                    self.download_info[current_type]['size'] = total_bytes
                
                # 更新已下载大小
                downloaded = d.get('downloaded_bytes', 0)
                self.download_info[current_type]['downloaded'] = downloaded
                
                # 获取下载速度和剩余时间
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                
                # 计算进度并更新UI
                self._calculate_and_report_progress(speed, eta)
                
            elif status == 'finished':
                # 标记当前部分完成
                format_id = str(d.get('info_dict', {}).get('format_id', ''))
                current_type = 'video' if 'video' in format_id else 'audio'
                self.download_info[current_type]['done'] = True
                
                # 如果是分离的视频和音频，且两个都下载完成，则开始合并
                if (self.download_info['is_split'] and 
                    self.download_info['video']['done'] and 
                    self.download_info['audio']['done']):
                    self.download_info['merging'] = True
                    self.progress_callback({
                        'status': '处理中',
                        'progress': 99,
                        'detail': '正在合并音视频...',
                        'is_merging': True
                    })
                
        except Exception as e:
            print(f"Progress hook error: {str(e)}")
    
    def _format_speed(self, speed: float) -> str:
        """格式化下载速度"""
        if speed == 0:
            return "0 B/s"
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        while speed >= 1024 and unit_index < len(units) - 1:
            speed /= 1024
            unit_index += 1
        return f"{speed:.1f} {units[unit_index]}"
    
    def _format_time(self, seconds: int) -> str:
        """格式化剩余时间"""
        if seconds < 0:
            return "未知"
        if seconds < 60:
            return f"{seconds}秒"
        if seconds < 3600:
            return f"{seconds//60}分{seconds%60}秒"
        return f"{seconds//3600}时{(seconds%3600)//60}分"
    
    def _calculate_and_report_progress(self, speed: float = 0, eta: int = 0):
        """计算并报告总体进度"""
        try:
            if self.download_info['merging']:
                return
            
            if self.download_info['is_split']:
                # 分别计算视频和音频的进度
                total_size = (self.download_info['video']['size'] + 
                            self.download_info['audio']['size'])
                total_downloaded = (self.download_info['video']['downloaded'] + 
                                  self.download_info['audio']['downloaded'])
                
                if total_size > 0:
                    progress = (total_downloaded / total_size) * 100
                    
                    # 构建详细信息
                    video_progress = ((self.download_info['video']['downloaded'] / 
                                    self.download_info['video']['size']) * 100
                                    if self.download_info['video']['size'] > 0 else 0)
                    audio_progress = ((self.download_info['audio']['downloaded'] / 
                                    self.download_info['audio']['size']) * 100
                                    if self.download_info['audio']['size'] > 0 else 0)
                    
                    # 添加速度和剩余时间信息
                    speed_str = self._format_speed(speed)
                    eta_str = self._format_time(eta)
                    
                    detail = (f"视频: {video_progress:.1f}% "
                            f"音频: {audio_progress:.1f}% • "
                            f"{speed_str} • 剩余 {eta_str}")
                    
                    self.progress_callback({
                        'status': '下载中',
                        'progress': progress,
                        'detail': detail,
                        'total_size': self._format_size(total_size),
                        'downloaded_size': self._format_size(total_downloaded),
                        'speed': speed_str,
                        'eta': eta_str
                    })
            else:
                # 单文件下载
                current_type = 'video'
                total = self.download_info[current_type]['size']
                downloaded = self.download_info[current_type]['downloaded']
                
                if total > 0:
                    progress = (downloaded / total) * 100
                    speed_str = self._format_speed(speed)
                    eta_str = self._format_time(eta)
                    
                    detail = (f"已下载: {self._format_size(downloaded)} / "
                             f"{self._format_size(total)} • "
                             f"{speed_str} • 剩余 {eta_str}")
                    
                    self.progress_callback({
                        'status': '下载中',
                        'progress': progress,
                        'detail': detail,
                        'total_size': self._format_size(total),
                        'downloaded_size': self._format_size(downloaded),
                        'speed': speed_str,
                        'eta': eta_str
                    })
                    
        except Exception as e:
            print(f"Calculate progress error: {str(e)}")
    
    def download(self, url: str) -> None:
        """开始下载视频"""
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'progress_hooks': [self._progress_hook],
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            # 下载完成
            self.progress_callback({
                'status': '已完成',
                'progress': 100,
                'detail': '下载完成'
            })
            
        except Exception as e:
            self.progress_callback({
                'status': '失败',
                'detail': str(e)
            })
            raise 