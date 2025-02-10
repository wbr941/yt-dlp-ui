from tkinter import ttk
from tkinter.ttk import Style

# Windows 11 主题颜色
COLORS = {
    'primary': '#0067C0',        # Win11 蓝色
    'primary_light': '#0078D4',  # 亮蓝色
    'secondary': '#FFFFFF',      # 白色背景
    'text': '#202020',          # 深色文本
    'text_secondary': '#666666', # 次要文本
    'success': '#0F7B0F',       # 成功绿色
    'warning': '#9D5D00',       # 警告橙色
    'error': '#C42B1C',         # 错误红色
    'white': '#FFFFFF',         # 纯白
    'gray': '#F3F3F3',          # 浅灰背景
    'border': '#E5E5E5',        # 边框颜色
    'search_border': '#E5E5E5',      # 搜索框边框
    'search_bg': '#FFFFFF',          # 搜索框背景
    'progress_bg': '#E5E5E5',        # 进度条背景
    'progress_fill': '#0078D4',      # Win11 进度填充色
    'card_bg': '#F5F5F5',        # 卡片背景色
    'card_border': '#E5E5E5',    # 卡片边框色
    'button_text': '#000000',    # 按钮文字颜色
    'progress_0': '#F5F5F5',     # 0% 进度颜色
    'progress_100': '#0078D4',   # 100% 进度颜色
    'task_bg': '#FFFFFF',        # 任务卡片背景色
    'task_border': '#E5E5E5',    # 任务卡片边框色
    'task_hover': '#F5F5F5',     # 任务卡片悬停色
}

class Styles:
    @staticmethod
    def setup_styles():
        """设置全局样式"""
        style = Style()
        
        # 修改所有字体为微软雅黑
        default_font = ('微软雅黑', 10)
        title_font = ('微软雅黑', 16, 'bold')
        
        # 配置全局主题
        style.configure('.',
            background=COLORS['secondary'],
            foreground=COLORS['text'],
            font=default_font
        )
        
        # 配置Frame样式
        style.configure('Nav.TFrame',
            background=COLORS['secondary']
        )
        
        style.configure('Content.TFrame',
            background=COLORS['secondary']
        )
        
        # 修改按钮样式，使用黑色文字
        style.configure('Accent.TButton',
            background=COLORS['primary'],
            foreground=COLORS['button_text'],
            padding=(20, 8),
            font=default_font
        )
        
        # 配置导航按钮样式
        style.configure('Nav.TButton',
            background=COLORS['secondary'],
            foreground=COLORS['text'],
            padding=(20, 10),
            font=('微软雅黑', 10, 'bold')
        )
        
        # 配置输入框样式
        style.configure('TEntry',
            fieldbackground=COLORS['white'],
            padding=(10, 8),
            font=default_font
        )
        
        # 配置Treeview样式
        style.configure('Treeview',
            background=COLORS['white'],
            foreground=COLORS['text'],
            fieldbackground=COLORS['white'],
            font=('微软雅黑', 9),
            rowheight=30
        )
        
        style.configure('Treeview.Heading',
            background=COLORS['gray'],
            foreground=COLORS['text'],
            font=('微软雅黑', 9, 'bold')
        )
        
        # 配置Label样式
        style.configure('TLabel',
            background=COLORS['secondary'],
            foreground=COLORS['text'],
            font=default_font
        )
        
        # 配置标题Label样式
        style.configure('Title.TLabel',
            font=title_font
        )
        
        # 配置搜索框样式
        style.configure('Search.TEntry',
            fieldbackground=COLORS['search_bg'],
            borderwidth=0,
            relief='flat',
            font=('微软雅黑', 11)
        )
        
        # 配置进度条样式
        style.configure("Download.Horizontal.TProgressbar",
            troughcolor=COLORS['progress_bg'],
            background=COLORS['progress_fill'],
            bordercolor=COLORS['progress_bg'],
            lightcolor=COLORS['progress_fill'],
            darkcolor=COLORS['progress_fill']
        )
        
        # 配置卡片样式
        style.configure('Card.TFrame',
            background=COLORS['card_bg'],
            borderwidth=1,
            relief='solid'
        )
        
        # 配置卡片标签样式
        style.configure('Card.TLabel',
            background=COLORS['card_bg'],
            foreground=COLORS['text'],
            font=default_font,
            padding=(10, 5)
        )

        # 添加进度颜色标签配置
        for i in range(0, 101, 5):  # 创建20个渐变色标签
            r1, g1, b1 = int('F5', 16), int('F5', 16), int('F5', 16)  # 起始颜色
            r2, g2, b2 = 0x00, 0x78, 0xD4  # 结束颜色
            
            # 计算渐变色
            r = int(r1 + (r2 - r1) * i / 100)
            g = int(g1 + (g2 - g1) * i / 100)
            b = int(b1 + (b2 - b1) * i / 100)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            tag_name = f'progress_{i}'
            style.configure(tag_name, background=color)

        # 配置任务卡片样式
        style.configure('Task.TFrame',
            background=COLORS['task_bg'],
            bordercolor=COLORS['task_border'],
            lightcolor=COLORS['task_bg'],
            darkcolor=COLORS['task_bg']
        )
        
        # 配置任务内容样式
        style.configure('Task.TLabel',
            background=COLORS['task_bg'],
            foreground=COLORS['text'],
            font=('微软雅黑', 9),
            padding=(5, 2)
        )
        
        # 配置进度条容器样式
        style.configure('TaskProgress.TFrame',
            background=COLORS['progress_fill'],
            borderwidth=0
        )

        # 配置成功状态样式
        style.configure('Success.TFrame',
            background=COLORS['success']
        )
        
        # 配置错误状态样式
        style.configure('Error.TFrame',
            background=COLORS['error']
        )

        # 配置关于页面样式
        style.configure('AboutTitle.TLabel',
            font=('微软雅黑', 20, 'bold'),
            foreground=COLORS['text'],
            background=COLORS['card_bg']  # 添加背景色
        )
        
        style.configure('AboutDesc.TLabel',
            font=('微软雅黑', 12),
            foreground=COLORS['text_secondary'],
            background=COLORS['card_bg']  # 添加背景色
        )
        
        style.configure('AboutLabel.TLabel',
            font=('微软雅黑', 11),
            foreground=COLORS['text'],
            background=COLORS['card_bg']  # 添加背景色
        )
        
        style.configure('AboutLink.TLabel',
            font=('微软雅黑', 11),
            foreground=COLORS['primary'],
            background=COLORS['card_bg']  # 添加背景色
        )
        
        style.configure('AboutCopyright.TLabel',
            font=('微软雅黑', 10),
            foreground=COLORS['text_secondary'],
            background=COLORS['card_bg']  # 添加背景色
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