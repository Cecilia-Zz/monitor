# -*- coding: utf-8 -*-
import cv2
import time
import subprocess as sp
from address import camera_address, rtmp_address
import multiprocessing as mp


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
    command = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', camera_path,
        '-vcodec', 'copy',
        '-an',
        '-f', 'flv',
        pushUrl
    ]

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

    # 多进程推流
    processes = []
    for camera_path, rtmpUrl in zip(camera_address, rtmp_address):
        processes.append(mp.Process(target=push_stream, args=(camera_path, rtmpUrl)))
    for process in processes:
        process.start()
        time.sleep(2)
