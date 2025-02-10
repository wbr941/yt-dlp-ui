from tkinter import ttk
import webbrowser
from ..widgets.rounded_frame import RoundedFrame

class AboutFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Content.TFrame', **kwargs)
        self.setup_ui()
        
    def setup_ui(self):
        # 标题
        title_label = ttk.Label(
            self, 
            text="关于", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 30))
        
        # 创建内容卡片
        content_card = RoundedFrame(self, radius=10, padding=4, style='Card.TFrame')
        content_card.pack(fill='x', padx=50, pady=10)
        
        content = content_card.content_frame
        
        # 项目名称
        name_label = ttk.Label(
            content,
            text="yt-dlp-ui",
            style='AboutTitle.TLabel'
        )
        name_label.pack(pady=(20, 10))
        
        # 项目描述
        desc_label = ttk.Label(
            content,
            text="基于 tkinter 和 yt-dlp 的视频下载工具，支持多平台视频下载",
            style='AboutDesc.TLabel'
        )
        desc_label.pack(pady=(0, 20))
        
        # GitHub 链接
        github_frame = ttk.Frame(content, style='Card.TFrame')
        github_frame.pack(pady=(0, 20))
        
        github_label = ttk.Label(
            github_frame,
            text="GitHub: ",
            style='AboutLabel.TLabel'
        )
        github_label.pack(side='left')
        
        github_link = ttk.Label(
            github_frame,
            text="https://github.com/wbr941/yt-dlp-ui",
            style='AboutLink.TLabel',
            cursor="hand2"
        )
        github_link.pack(side='left')
        github_link.bind('<Button-1>', lambda e: webbrowser.open("https://github.com/wbr941/yt-dlp-ui")) 