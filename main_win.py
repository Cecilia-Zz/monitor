# -*- coding: utf-8 -*-
import cv2
import threading
import time
import subprocess as sp
from address import camera_address, rtsp_address, rtmp_address
import multiprocessing as mp


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


# 播放拉流视频
def play(win_name, rtspUrl):
    cap = cv2.VideoCapture(rtspUrl)
    ret, frame0= cap.read()
    while ret:
        ret, frame = cap.read()
        cv2.imshow(win_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()


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

    # 预览窗口
    '''
    processes1 = []
    for camera_path, rtspUrl in zip(camera_address, rtsp_address):
        processes1.append(mp.Process(target=play, args=(camera_path, rtspUrl)))
    for process in processes1:
        process.start()
    '''

    '''
    # 多线程
    threads1 = []
    for camera_path, rtspUrl in zip(camera_address, rtsp_address):
        threads1.append(threading.Thread(target=operate_stream, args=(camera_path, rtspUrl,)))

    for thread in threads1:
        thread.start()
    threads2 = []
    for camera_path, rtspUrl in zip(camera_address, rtsp_address):
        threads2.append(threading.Thread(target=play, args=(camera_path, rtspUrl,)))

    for thread in threads2:
        thread.start()

    thread1 = threading.Thread(target=operate_stream, name='1', args=(camera_path, rtspUrl, ))
    thread2 = threading.Thread(target=play, name='2', args=(camera_path, rtspUrl,))

    # 开启线程
    thread1.start()
    time.sleep(4)
    thread2.start()
    '''