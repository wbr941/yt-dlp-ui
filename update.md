# yt-dlp-ui v1.2 更新公告 - 全新界面与功能升级

![软件截图](https://image.wujiyan.cc/imgs/2025/01/01/67750c4920c51.gif)

## 🚀 主要更新亮点

### 1. 全新视觉设计（基于styles.py优化）
- **Windows 11风格界面**：采用Fluent设计语言，全面升级圆角控件和卡片式布局
- **动态进度条**：实现从浅灰到蓝色的平滑渐变效果
- **智能深色模式**：优化各界面元素的对比度表现

### 2. 增强型下载管理（gui.py:265-268）
```python
class VideoDownloaderGUI:
    def add_download_task(self, info):
        # 新增分P下载支持
        if info.get('entries'):
            for entry in info['entries']:
                self._create_task_card(entry)
        else:
            self._create_task_card(info)


### 3. 核心功能升级
- **智能格式识别**：自动选择最佳视频/音频组合
- **分P下载支持**：自动识别合集视频并创建多个下载任务
- **实时速度监控**：显示即时下载速度与剩余时间

## 🛠️ 技术改进

### 下载引擎优化（downloader.py）
```python
class VideoDownloader:
    def download(self, url):
        # 新增分片下载支持
        self.ydl_opts.update({
            'external_downloader': 'aria2c',
            'external_downloader_args': ['-x16', '-s16', '-k5M']
        })
```

## 🆕 新增功能详解

### 1. 智能合集处理
- 自动识别YouTube播放列表/B站合集
- 支持批量添加多个分P任务
- 可单独管理每个分P的下载进度

### 2. 增强型右键菜单
```python
# 新增上下文菜单支持（gui.py:195-203）
self.right_click_menu.add_command(label="复制链接", command=self.copy_url)
self.right_click_menu.add_command(label="粘贴链接", command=self.paste_url)
self.right_click_menu.add_separator()
self.right_click_menu.add_command(label="打开下载目录", command=self.open_download_folder)
```

### 3. 关于页面（about_frame.py）
![](https://img2024.cnblogs.com/blog/3588176/202502/3588176-20250210200142310-1162990817.png)


## 📥 安装与升级

```bash
# 全新安装
git clone https://github.com/wbr941/yt-dlp-ui.git
cd yt-dlp-ui
pip install -r requirements.txt

# 升级现有版本
git pull origin master
pip install --upgrade yt-dlp
```

## 📅 后续计划
- [ ] 浏览器扩展支持
- [ ] 下载队列优先级管理
- [ ] 自动更新功能



