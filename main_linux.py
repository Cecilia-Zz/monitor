# -*- coding: utf-8 -*-
import cv2
import threading
import time
import subprocess as sp
from address import camera_address, rtsp_address
import multiprocessing as mp

''''''
# 搭建流媒体服务器
def stream_server():
    # 管道配置
    command = [
        'cd', 'EasyDarwin;',
        './start.sh'
    ]
    p = sp.Popen(command,  stdout=sp.PIPE)
    p.stdout.read()
    time.sleep(3)


# opencv取流
def pull_stream(camera_path):
    cap = cv2.VideoCapture(camera_path)
    # Get video information
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, width, height


# ffmpeg推流
def push_stream(camera_path, rtspUrl):
    # ffmpeg command
    command = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', camera_path,
        '-vcodec', 'copy',
        '-r', '15',
        '-s', '1080x720',
        '-an',
        '-f', 'rtsp',
        rtspUrl
    ]
    # 管道配置
    p = sp.Popen(command, stdout=sp.PIPE)
    while True:
        if sp.Popen.poll(p) is not None:
            p = sp.Popen(command, stdout=sp.PIPE)


'''
def operate_stream(camera_path, rtspUrl):
    fps, width, height = pull_stream(camera_path)
    print(f'fps: {fps} resolution: {width}x{height}')
    push_stream(camera_path, rtspUrl)
'''


# 播放拉流视频
def play(windowsname,rtspUrl):
    cap = cv2.VideoCapture(rtspUrl)
    ret, frame0= cap.read()
    while ret:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1080, 720))
        cv2.imshow(windowsname, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    # camera_path = "rtsp://admin:Admin123@192.168.9.12/Streaming/Channels/1"
    # rtspUrl = "rtsp://192.168.4.226/test.dsp"

    # 运行服务器
    stream_server()
    # 多进程推流
    processes = []
    for camera_path, rtspUrl in zip(camera_address, rtsp_address):
        processes.append(mp.Process(target=push_stream, args=(camera_path, rtspUrl)))
    for process in processes:
        process.start()
        time.sleep(2)