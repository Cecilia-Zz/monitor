# -*- coding: utf-8 -*-
import cv2
import time
import subprocess as sp
from address import camera_address, rtmp_address
import multiprocessing as mp
from play import play


# 搭建流媒体服务器
def stream_server():
    # 管道配置
    # p = sp.Popen('ServiceInstall-easydarwin.exe', shell=True, stdout=sp.PIPE)
    p = sp.Popen('easydarwin.exe', shell=True, stdout=sp.PIPE)
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
def push_stream(camera_path, pushUrl):
    # ffmpeg command
    # rtmp
    command = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', camera_path,
        '-vcodec', 'copy',
        '-an',
        '-f', 'flv',
        pushUrl
    ]
    '''
    # rtsp
    command = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', camera_path,
        '-vcodec', 'copy',
        '-r', '15',
        '-s', '1080x720',
        '-an',
        '-f', 'rtsp',
        pushUrl
    ]
    '''

    # 管道配置
    p = sp.Popen(command, stdout=sp.PIPE)
    while True:
        if sp.Popen.poll(p) is not None:
            p = sp.Popen(command, stdout=sp.PIPE)


def operate_stream(camera_path, rtspUrl):
    fps, width, height = pull_stream(camera_path)
    print(f'fps: {fps} resolution: {width}x{height}')
    push_stream(camera_path, rtspUrl)


if __name__ == '__main__':
    # 搭建流媒体服务器
    # thread = threading.Thread(target=stream_server, args=())
    # thread.start()

    # 多进程推流
    processes = []
    for camera_path, rtmpUrl in zip(camera_address, rtmp_address):
        processes.append(mp.Process(target=push_stream, args=(camera_path, rtmpUrl)))
    for process in processes:
        process.start()
        time.sleep(2)
