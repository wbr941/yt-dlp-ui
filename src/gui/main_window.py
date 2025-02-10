def setup_ui(self):
    # ... 其他代码保持不变 ...
    
    # 添加关于按钮到导航栏
    self.about_btn = ttk.Button(
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
    self.setup_about_frame()  # 添加关于页面
    self.show_frame("home")

def setup_about_frame(self):
    """设置关于页面"""
    from .frames.about_frame import AboutFrame
    self.frames["about"] = AboutFrame(self.content_frame) 