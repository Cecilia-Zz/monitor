###一、配置NVR  
1. 登录NVR后台，【配置】-> 【音视频】-> 【视频】
2. 设置【分辨率】为【1280x720P】，【视频帧率】为【10】，【码率上线】为【1000】

###二、安装ffmpeg和easyDarwin

1.安装ffmpeg

 * [下载](http://www.ffmpeg.org/download.html#build-windows)  
 * 解压后将bin文件夹配置到环境变量里
<br/>

2.搭建easyDarwin 

- [下载](https://github.com/EasyDarwin/EasyDarwin)  
- 修改 ***easydarwin.ini*** 中需要的配置，如本地ffmpeg的可执行程序的路径  


3.在 ***address.py*** 中修改摄像头地址和推流地址

4.运行***main_win.py***  
####note:
1. 将#预览窗口 部分反注释，可预览推流视频  
2. 将#搭建流媒体服务器 部分注释，自行打开***EasyDarwin.exe***文件，可实时查看推流列表及推流进程数量  
