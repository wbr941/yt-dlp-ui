from tkinter import ttk
from tkinter.ttk import Style

# Windows 11 主题颜色
COLORS = {
    'primary': '#0067C0',        # Win11 蓝色
    'primary_light': '#0078D4',  # 亮蓝色
    'secondary': '#FFFFFF',      # 白色背景
    'text': '#202020',          # 深色文本
    'success': '#0F7B0F',       # 成功绿色
    'warning': '#9D5D00',       # 警告橙色
    'error': '#C42B1C',         # 错误红色
    'white': '#FFFFFF',         # 纯白
    'gray': '#F3F3F3',          # 浅灰背景
    'border': '#E5E5E5',        # 边框颜色
}

class Styles:
    @staticmethod
    def setup_styles():
        """设置全局样式"""
        style = Style()
        
        # 配置全局主题
        style.configure('.',
            background=COLORS['secondary'],
            foreground=COLORS['text'],
            font=('Segoe UI', 10)
        )
        
        # 配置Frame样式
        style.configure('Nav.TFrame',
            background=COLORS['secondary']
        )
        
        style.configure('Content.TFrame',
            background=COLORS['secondary']
        )
        
        # 配置按钮样式
        style.configure('Accent.TButton',
            background=COLORS['primary'],
            foreground=COLORS['white'],
            padding=(20, 8),
            font=('Segoe UI', 10)
        )
        
        # 配置导航按钮样式
        style.configure('Nav.TButton',
            background=COLORS['secondary'],
            foreground=COLORS['text'],
            padding=(20, 10),
            font=('Segoe UI', 10, 'bold')
        )
        
        # 配置输入框样式
        style.configure('TEntry',
            fieldbackground=COLORS['white'],
            padding=(10, 8)
        )
        
        # 配置Treeview样式
        style.configure('Treeview',
            background=COLORS['white'],
            foreground=COLORS['text'],
            fieldbackground=COLORS['white'],
            font=('Segoe UI', 9),
            rowheight=30
        )
        
        style.configure('Treeview.Heading',
            background=COLORS['gray'],
            foreground=COLORS['text'],
            font=('Segoe UI', 9, 'bold')
        )
        
        # 配置Label样式
        style.configure('TLabel',
            background=COLORS['secondary'],
            foreground=COLORS['text'],
            font=('Segoe UI', 10)
        )
        
        # 配置标题Label样式
        style.configure('Title.TLabel',
            font=('Segoe UI', 16, 'bold')
        )

    @staticmethod
    def setup_window_style(window):
        """设置窗口样式"""
        window.configure(bg=COLORS['secondary'])
        
    @staticmethod
    def setup_nav_frame(frame):
        """设置导航栏样式"""
        frame.configure(
            style='Nav.TFrame',
            width=200  # 加宽导航栏
        )
        
    @staticmethod
    def setup_content_frame(frame):
        """设置内容区域样式"""
        frame.configure(
            style='Content.TFrame',
            padding=(30, 30)  # 使用padding代替padx和pady
        )
        
    @staticmethod
    def setup_treeview(tree):
        """设置树形视图样式和标签"""
        tree.tag_configure('success', foreground=COLORS['success'])
        tree.tag_configure('warning', foreground=COLORS['warning'])
        tree.tag_configure('error', foreground=COLORS['error']) 