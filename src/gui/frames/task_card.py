from ..widgets.rounded_frame import RoundedFrame
from tkinter import ttk
import tkinter as tk

class TaskCard(RoundedFrame):
    def __init__(self, parent, task_info, on_cancel=None, **kwargs):
        super().__init__(parent, radius=8, padding=2, **kwargs)
        
        self.task_info = task_info
        self.on_cancel = on_cancel
        self.video_progress = 0
        self.audio_progress = 0
        self.is_merging = False
        self.setup_ui()
        
    def setup_ui(self):
        # 创建进度条背景
        self.progress_bg = RoundedFrame(
            self.content_frame,
            radius=6,
            padding=0,
            style='Task.TFrame'
        )
        self.progress_bg.place(relwidth=1, relheight=1)
        
        # 创建进度条
        self.progress_fill = RoundedFrame(
            self.progress_bg.content_frame,
            radius=6,
            padding=0,
            style='TaskProgress.TFrame'
        )
        self.progress_fill.place(relwidth=0, relheight=1)
        
        # 创建内容区域
        content = ttk.Frame(self.content_frame, style='Task.TFrame')
        content.pack(fill='both', expand=True, padx=15, pady=10)
        
        # 左侧信息
        info_frame = ttk.Frame(content, style='Task.TFrame')
        info_frame.pack(side='left', fill='both', expand=True)
        
        title_frame = ttk.Frame(info_frame, style='Task.TFrame')
        title_frame.pack(fill='x')
        
        self.title_label = ttk.Label(
            title_frame,
            text=self.task_info['title'],
            style='TaskTitle.TLabel'
        )
        self.title_label.pack(side='left')
        
        # 右侧状态
        status_frame = ttk.Frame(content, style='Task.TFrame')
        status_frame.pack(side='right', padx=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="准备下载",
            style='TaskStatus.TLabel'
        )
        self.status_label.pack(side='left', padx=(0, 10))
        
        self.progress_label = ttk.Label(
            status_frame,
            text="0%",
            style='TaskProgress.TLabel'
        )
        self.progress_label.pack(side='left', padx=(0, 10))
        
        # 添加详细进度标签
        self.detail_label = ttk.Label(
            status_frame,
            text="",
            style='TaskDetail.TLabel'
        )
        self.detail_label.pack(side='left', padx=(0, 10))
        
        # 取消按钮
        self.cancel_btn = ttk.Button(
            status_frame,
            text="取消",
            style='TaskCancel.TButton',
            command=self._on_cancel
        )
        self.cancel_btn.pack(side='left')
        
    def update_progress(self, progress_info):
        """更新下载进度"""
        try:
            status = progress_info['status']
            self.status_label.config(text=status)
            
            # 更新详细信息
            if 'detail' in progress_info:
                self.detail_label.config(text=progress_info['detail'])
            
            # 处理进度
            if 'progress' in progress_info:
                progress = progress_info['progress']
                self.progress_label.config(text=f"{progress:.1f}%")
                self.progress_fill.place(relwidth=progress/100)
            
            # 处理状态
            if status == "已完成":
                self.progress_fill.configure(style='Success.TFrame')
                self.cancel_btn.pack_forget()
                self.detail_label.config(text="")
            elif status == "失败":
                self.progress_fill.configure(style='Error.TFrame')
                self.cancel_btn.pack_forget()
            
        except Exception as e:
            print(f"更新进度出错: {str(e)}")
    
    def _on_cancel(self):
        if self.on_cancel:
            self.on_cancel(self.task_info['id']) 