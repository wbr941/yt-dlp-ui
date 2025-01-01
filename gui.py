import threading
from tkinter import messagebox, Tk, Label, Entry, Button, StringVar
from tkinter.ttk import Progressbar
from downloader import VideoDownloader, get_video_info, clean_url

class VideoDownloaderGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("wbr941's视频下载器")
        self.setup_ui()
        
    def setup_ui(self):
        # 创建输入框和标签
        prompt_label = Label(self.root, text="请输入视频链接:")
        prompt_label.pack(pady=5)
        
        self.url_entry = Entry(self.root, width=50)
        self.url_entry.pack(pady=10)
        
        self.video_info_label = Label(self.root, text="视频标题: \n平台: ")
        self.video_info_label.pack(pady=10)
        
        # 进度显示
        self.progress_var = StringVar()
        self.percent_label = Label(self.root, textvariable=self.progress_var)
        self.percent_label.pack(pady=10)
        
        self.progress_bar = Progressbar(
            self.root, 
            orient='horizontal', 
            length=400, 
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)
        
        # 下载按钮
        download_button = Button(
            self.root, 
            text="下载视频", 
            command=self.download_video
        )
        download_button.pack(pady=20)
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes')
                downloaded = d.get('downloaded_bytes', 0)
                
                if total is None:
                    total = d.get('total_bytes_estimate', 0)
                
                if total > 0:
                    percent = min(downloaded / total * 100, 100)
                    self.progress_var.set(f"{percent:.1f}%")
                    self.progress_bar['value'] = percent
                else:
                    self.progress_var.set(f"已下载: {downloaded/1024/1024:.1f}MB")
                    self.progress_bar['value'] = 0
                    
            except Exception:
                self.progress_var.set("下载中...")
                self.progress_bar['value'] = 0

    def download_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("错误", "请输入有效的 URL！")
            return
        
        cleaned_url = clean_url(url)
        
        try:
            info = get_video_info(cleaned_url)
            self.video_info_label.config(
                text=f"视频标题: {info['title']}\n平台: {info['extractor']}"
            )
        except Exception as e:
            messagebox.showerror("错误", f"获取视频信息失败：{str(e)}")
            return

        def run_download():
            try:
                self.progress_bar['value'] = 0
                self.progress_var.set("0.00%")
                
                downloader = VideoDownloader(self.progress_hook)
                downloader.download(cleaned_url)
                
                self.progress_var.set("下载完成")
                self.percent_label.config(text="100.00%")
                messagebox.showinfo("成功", "下载完成！")
            except Exception as e:
                messagebox.showerror("错误", f"下载失败：{str(e)}")

        threading.Thread(target=run_download).start()

    def run(self):
        self.root.mainloop()