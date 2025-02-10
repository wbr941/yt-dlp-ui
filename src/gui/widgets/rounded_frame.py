import tkinter as tk
from tkinter import ttk

class RoundedFrame(ttk.Frame):
    def __init__(self, parent, radius=10, padding=4, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.canvas = tk.Canvas(
            self,
            background=self['style'] and ttk.Style().lookup(self['style'], 'background') or 'white',
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        self.content_frame = ttk.Frame(self.canvas, style=self['style'])
        
        self._radius = radius
        self._padding = padding
        
        self.bind('<Configure>', self._on_resize)
        
    def _on_resize(self, event):
        width = event.width
        height = event.height
        
        self.canvas.delete('all')
        
        # 绘制主要圆角矩形
        self._draw_rounded_rect(
            self._padding,
            self._padding,
            width - self._padding,
            height - self._padding,
            self._radius,
            fill=ttk.Style().lookup(self['style'], 'background'),
            outline=ttk.Style().lookup(self['style'], 'bordercolor', default='')
        )
        
        # 更新内容框架位置
        self.canvas.create_window(
            width//2,
            height//2,
            window=self.content_frame,
            width=width - self._padding*2,
            height=height - self._padding*2
        )
    
    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        # 使用贝塞尔曲线创建更平滑的圆角
        self.canvas.create_polygon(
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1,
            smooth=True,
            **kwargs
        ) 