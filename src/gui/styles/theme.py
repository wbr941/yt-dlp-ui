# 在 setup_styles 方法中添加
# 配置关于页面样式
style.configure('AboutTitle.TLabel',
    font=('微软雅黑', 20, 'bold'),
    foreground=COLORS['text']
)

style.configure('AboutDesc.TLabel',
    font=('微软雅黑', 12),
    foreground=COLORS['text_secondary']
)

style.configure('AboutLabel.TLabel',
    font=('微软雅黑', 11),
    foreground=COLORS['text']
)

style.configure('AboutLink.TLabel',
    font=('微软雅黑', 11),
    foreground=COLORS['primary']
)

style.configure('AboutCopyright.TLabel',
    font=('微软雅黑', 10),
    foreground=COLORS['text_secondary']
) 