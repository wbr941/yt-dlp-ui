import threading
from tkinter import messagebox, Tk, StringVar, Menu
from tkinter.ttk import Frame, Label, Entry, Button, Progressbar, Treeview, Scrollbar, Style
from downloader import VideoDownloader, get_video_info, clean_url
from datetime import datetime
from queue import Queue
import time
from styles import Styles, COLORS
from rounded_frame import RoundedFrame
from src.gui.frames.about_frame import AboutFrame

class VideoDownloaderGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("yt-dlp-ui")
        self.root.geometry("1000x600")
        
        # 设置窗口样式
        Styles.setup_window_style(self.root)
        Styles.setup_styles()
        
        # 创建任务队列和更新队列
        self.download_queue = Queue()
        self.update_queue = Queue()
        self.info_queue = Queue()  # 新增：用于获取视频信息的队列
        
        self.download_tasks = {}
        self.is_running = True  # 用于控制线程
        
        # 启动工作线程
        self.start_worker_threads()
        
        self.setup_ui()
        
    def start_worker_threads(self):
        """启动所有工作线程"""
        # UI更新线程
        self.update_thread = threading.Thread(target=self.update_ui_thread, daemon=True)
        self.update_thread.start()
        
        # 下载处理线程
        self.download_thread = threading.Thread(target=self.download_worker, daemon=True)
        self.download_thread.start()
        
        # 视频信息获取线程
        self.info_thread = threading.Thread(target=self.info_worker, daemon=True)
        self.info_thread.start()
        
        # 定期刷新UI
        self.root.after(100, self.periodic_ui_update)

    def periodic_ui_update(self):
        """定期刷新UI，保持界面响应"""
        if self.is_running:
            self.root.update_idletasks()
            self.root.after(100, self.periodic_ui_update)

    def info_worker(self):
        """处理视频信息获取的线程"""
        while self.is_running:
            try:
                if not self.info_queue.empty():
                    url, callback = self.info_queue.get()
                    try:
                        info = get_video_info(url)
                        self.root.after(0, callback, info)
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror("错误", f"获取视频信息失败：{str(e)}"))
                    self.info_queue.task_done()
                time.sleep(0.1)
            except:
                continue

    def update_ui_thread(self):
        """处理UI更新的线程"""
        while self.is_running:
            try:
                if not self.update_queue.empty():
                    task_id, status, progress = self.update_queue.get_nowait()
                    try:
                        self.update_task_status(task_id, status, progress)
                    except:
                        pass
                    self.update_queue.task_done()
                time.sleep(0.05)  # 减少检查间隔
            except:
                continue

    def download_worker(self):
        """处理下载任务的线程"""
        while self.is_running:
            try:
                if not self.download_queue.empty():
                    url, task_id = self.download_queue.get()
                    
                    def progress_hook(d):
                        if not self.is_running:
                            return
                        if d['status'] == 'downloading':
                            try:
                                total = d.get('total_bytes')
                                downloaded = d.get('downloaded_bytes', 0)
                                
                                if total is None:
                                    total = d.get('total_bytes_estimate', 0)
                                
                                if total > 0:
                                    percent = min(downloaded / total * 100, 100)
                                    progress = f"{percent:.1f}%"
                                    self.update_queue.put((task_id, "下载中", progress))
                                else:
                                    progress = f"已下载: {downloaded/1024/1024:.1f}MB"
                                    self.update_queue.put((task_id, "下载中", progress))
                            except:
                                self.update_queue.put((task_id, "下载中", "计算中..."))

                    try:
                        downloader = VideoDownloader(progress_hook)
                        downloader.download(url)
                        self.update_queue.put((task_id, "已完成", "100%"))
                        self.root.after(0, lambda: messagebox.showinfo("成功", "下载完成！"))
                    except Exception as e:
                        self.update_queue.put((task_id, "失败", "0%"))
                        error_msg = str(e)
                        self.root.after(0, lambda: messagebox.showerror("错误", f"下载失败：{error_msg}"))
                    
                    self.download_queue.task_done()
                time.sleep(0.1)
            except:
                continue

    def setup_ui(self):
        # 创建主框架
        self.main_frame = Frame(self.root, style='TFrame')
        self.main_frame.pack(fill="both", expand=True)
        
        # 创建左侧导航栏
        self.nav_frame = Frame(self.main_frame, style='Nav.TFrame')
        Styles.setup_nav_frame(self.nav_frame)
        self.nav_frame.pack(side="left", fill="y")
        
        # 创建内容区域
        self.content_frame = Frame(self.main_frame, style='Content.TFrame')
        Styles.setup_content_frame(self.content_frame)
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        # 添加导航按钮
        self.home_btn = Button(
            self.nav_frame,
            text="主页",
            style='Nav.TButton',
            command=lambda: self.show_frame("home")
        )
        self.home_btn.pack(pady=5, padx=10, fill='x')
        
        self.downloads_btn = Button(
            self.nav_frame,
            text="下载管理",
            style='Nav.TButton',
            command=lambda: self.show_frame("downloads")
        )
        self.downloads_btn.pack(pady=5, padx=10, fill='x')
        
        # 添加关于按钮
        self.about_btn = Button(
            self.nav_frame,
            text="关于",
            style='Nav.TButton',
            command=lambda: self.show_frame("about")
        )
        self.about_btn.pack(pady=5, padx=10, fill='x')
        
        # 创建不同的页面
        self.frames = {}
        self.setup_home_frame()
        self.setup_downloads_frame()
        self.setup_about_frame()
        self.show_frame("home")
        
    def setup_home_frame(self):
        home_frame = Frame(self.content_frame, style='TFrame')
        self.frames["home"] = home_frame
        
        # 标题
        title_label = Label(
            home_frame, 
            text="yt-dlp-ui", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 30))

        
        # 创建搜索框容器
        search_container = Frame(home_frame, style='TFrame')
        search_container.pack(pady=(0, 20), fill='x', padx=50)
        
        # 输入框和下载按钮在同一行
        self.url_entry = Entry(
            search_container,
            width=50,
            style='Search.TEntry'
        )
        self.url_entry.pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        # 绑定回车键
        self.url_entry.bind('<Return>', lambda e: self.start_download())
        
        # 下载按钮
        download_button = Button(
            search_container,
            text="开始下载",
            style='Accent.TButton',
            command=self.start_download
        )
        download_button.pack(side='left')
        
        # 创建右键菜单
        self.right_click_menu = Menu(self.root, tearoff=0)
        self.right_click_menu.add_command(label="复制", command=self.copy_text)
        self.right_click_menu.add_command(label="粘贴", command=self.paste_text)
        self.url_entry.bind("<Button-3>", self.show_menu)
        
        # 创建两个卡片容器
        title_card = Frame(home_frame, style='Card.TFrame')
        title_card.pack(pady=(10, 5), padx=50, fill='x')
        
        platform_card = Frame(home_frame, style='Card.TFrame')
        platform_card.pack(pady=(5, 10), padx=50, fill='x')
        
        # 视频标题卡片
        self.video_title_label = Label(
            title_card,
            text="视频标题: ",
            style='Card.TLabel'
        )
        self.video_title_label.pack(fill='x', expand=True)
        
        # 平台信息卡片
        self.platform_label = Label(
            platform_card,
            text="平台: ",
            style='Card.TLabel'
        )
        self.platform_label.pack(fill='x', expand=True)

    def setup_downloads_frame(self):
        downloads_frame = Frame(self.content_frame, style='TFrame')
        self.frames["downloads"] = downloads_frame
        
        # 标题
        title_label = Label(
            downloads_frame, 
            text="下载管理", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 30))
        
        # 创建任务列表容器
        self.tasks_container = Frame(downloads_frame, style='TFrame')
        self.tasks_container.pack(fill='both', expand=True, padx=20)
        
        # 存储任务卡片的字典
        self.task_cards = {}

    def setup_about_frame(self):
        """设置关于页面"""
        self.frames["about"] = AboutFrame(self.content_frame)

    def show_frame(self, frame_name):
        # 隐藏所有框架
        for frame in self.frames.values():
            frame.pack_forget()
        
        # 显示选中的框架
        self.frames[frame_name].pack(fill="both", expand=True)
        
    def show_menu(self, event):
        self.right_click_menu.tk_popup(event.x_root, event.y_root)

    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.url_entry.get())

    def paste_text(self):
        try:
            text = self.root.clipboard_get()
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, text)
        except:
            pass
            
    def add_download_task(self, info):
        """添加新的下载任务到列表"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # 创建圆角任务卡片
        task_card = RoundedFrame(
            self.tasks_container,
            radius=8,
            padding=2,
            style='Task.TFrame'
        )
        task_card.pack(fill='x', pady=5, padx=10)
        
        # 使用内容框架
        content = task_card.content_frame
        
        # 创建进度条背景（使用圆角框架）
        progress_bg = RoundedFrame(
            content,
            radius=6,
            padding=0,
            style='Task.TFrame'
        )
        progress_bg.place(relwidth=1, relheight=1)
        
        # 创建进度条填充
        progress_fill = RoundedFrame(
            progress_bg.content_frame,
            radius=6,
            padding=0,
            style='TaskProgress.TFrame'
        )
        progress_fill.place(relwidth=0, relheight=1)
        
        # 添加任务信息
        info_frame = Frame(content, style='Task.TFrame')
        info_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        time_label = Label(info_frame, text=current_time, style='Task.TLabel')
        time_label.pack(side='left', padx=(0, 20))
        
        title_label = Label(info_frame, text=info['title'], style='Task.TLabel')
        title_label.pack(side='left', padx=(0, 20), fill='x', expand=True)
        
        platform_label = Label(info_frame, text=info['extractor'], style='Task.TLabel')
        platform_label.pack(side='left', padx=(0, 20))
        
        status_label = Label(info_frame, text="准备下载", style='Task.TLabel')
        status_label.pack(side='left', padx=(0, 20))
        
        progress_label = Label(info_frame, text="0%", style='Task.TLabel')
        progress_label.pack(side='left')
        
        # 存储任务信息
        task_id = str(len(self.task_cards))
        self.task_cards[task_id] = {
            'card': task_card,
            'progress_fill': progress_fill,
            'status_label': status_label,
            'progress_label': progress_label,
            'value': 0
        }
        
        return task_id

    def update_task_status(self, task_id, status, progress):
        """更新任务状态和进度"""
        if task_id in self.task_cards:
            task_info = self.task_cards[task_id]
            
            # 更新状态文本
            task_info['status_label'].config(text=status)
            
            try:
                if '%' in progress:
                    percent = float(progress.strip('%'))
                    task_info['value'] = percent
                    task_info['progress_label'].config(text=f"{percent:.1f}%")
                    
                    # 更新进度条
                    task_info['progress_fill'].place(relwidth=percent/100)
                    
                    # 设置完成状态的特殊样式
                    if status == "已完成":
                        task_info['progress_fill'].configure(style='Success.TFrame')
                    elif status == "失败":
                        task_info['progress_fill'].configure(style='Error.TFrame')
                else:
                    task_info['progress_label'].config(text=progress)
            except:
                task_info['progress_label'].config(text=progress)

    def start_download(self):
        """开始下载任务"""
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("错误", "请输入有效的 URL！")
            return
        
        cleaned_url = clean_url(url)
        
        def on_info_received(info):
            """当获取到视频信息后的回调"""
            # 更新标签显示
            self.video_title_label.config(
                text=f"视频标题: {info['title']}"
            )
            self.platform_label.config(
                text=f"平台: {info['extractor']}"
            )
            
            # 检查是否是合集视频
            entries = info.get('entries', [])
            if entries:
                # 是合集视频，为每个分P创建下载任务
                main_title = info.get('title', '未知标题')
                for entry in entries:
                    part_info = {
                        'title': f"{main_title} - P{entry.get('playlist_index', '?')} {entry.get('title', '未知标题')}",
                        'extractor': info.get('extractor', '未知平台')
                    }
                    task_id = self.add_download_task(part_info)
                    self.download_queue.put((entry.get('webpage_url', cleaned_url), task_id))
            else:
                # 单个视频
                task_id = self.add_download_task(info)
                self.download_queue.put((cleaned_url, task_id))
            
            # 切换到下载页面
            self.show_frame("downloads")
        
        # 将视频信息获取请求添加到队列
        self.info_queue.put((cleaned_url, on_info_received))

    def on_closing(self):
        """窗口关闭时的处理"""
        self.is_running = False
        self.root.destroy()

    def run(self):
        """运行应用"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()