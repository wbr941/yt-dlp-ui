import tkinter as tk
from tkinter import ttk

class RoundedFrame(ttk.Frame):
    def __init__(self, parent, radius=10, padding=10, **kwargs):
        super().__init__(parent, **kwargs)
        
        # 创建圆角效果的画布
        self.canvas = tk.Canvas(
            self,
            background=self['style'] and ttk.Style().lookup(self['style'], 'background') or 'white',
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # 创建内容框架
        self.content_frame = ttk.Frame(self.canvas, style=self['style'])
        
        # 存储参数
        self._radius = radius
        self._padding = padding
        
        # 绑定重绘事件
        self.bind('<Configure>', self._on_resize)
        
    def _on_resize(self, event):
        width = event.width
        height = event.height
        
        # 清除画布
        self.canvas.delete('all')
        
        # 绘制圆角矩形
        self.canvas.create_rounded_rectangle(
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

def _create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

# 添加圆角矩形方法到 Canvas
tk.Canvas.create_rounded_rectangle = _create_rounded_rectangle 