### 一、配置NVR  
1. 登录NVR后台，`配置` -> `音视频` -> `视频`
2. 设置`分辨率`为`1280x720P`，`视频帧率`为`10`，`码率上限`为`1000`

### 二、安装ffmpeg和程序需要的库 

1. [下载](http://www.ffmpeg.org/download.html#build-windows) ffmpeg
2. 解压下载的文件夹，将其中的`bin`文件夹配置到环境变量里
3. 安装cv2库  
```
> pip install opencv-python 
#如果安装不上，尝试用豆瓣源
> pip install opencv-python-i https://pypi.douban.com/simple
```

### 三、程序运行
1. 在 `address.py` 中修改摄像头地址和推流地址
2. 运行 `main_win.py` 推流
3. 运行 `play.py` 可拉取推流至服务器的监控视频流预览

