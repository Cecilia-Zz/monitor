### 一、配置NVR  
1. 登录NVR后台，`配置` -> `音视频` -> `视频`
2. 设置`分辨率`为`1280x720P`，`视频帧率`为`10`，`码率上限`为`1000`

### 二、安装ffmpeg和程序需要的库 
#### Windows系统
1. [下载](http://www.ffmpeg.org/download.html#build-windows) ffmpeg
2. 解压下载的文件夹，将其中的`bin`文件夹配置到环境变量里
3. 安装cv2库  
```
> pip install opencv-python 
#如果安装不上，尝试用豆瓣源
> pip install opencv-python -i https://pypi.douban.com/simple
```
#### Linux系统
1. 安装ffmpeg  
`$ apt install ffmpeg`
2. 安装cv2库  
`$ apt install python3-opencv`

### 三、程序运行
1. 在 `address.py` 中修改摄像头地址和推流地址
2. 运行 `push_stream.py` 推流
3. 运行 `play.py` 可拉取推流至服务器的监控视频流预览
4. 在web端: `http://服务器ip地址:8080/stat` 查看推流情况

#### note:
1. 如果推流频繁断流或预览时画面卡顿、掉帧，则需根据推流服务器/PC的CPU占用情况，适量减少推流的数量（可分成多个服务器/PC进行推流）。
2. 如果预览画面花屏、有大量马赛克，则检查网络是否有波动、网速慢、带宽不足等情况，可尝试将NVR设备的 `分辨率`、`视频帧率`和`码率上限` 降低。

