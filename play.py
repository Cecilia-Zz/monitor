import cv2
import subprocess as sp
import threading
import time


camera_path = "rtsp://admin:Admin123@192.168.9.12/Streaming/Channels/1"
rtspUrl = "rtsp://192.168.4.244/12.dsp"
rtmpUrl = "rtmp://localhost:1935/live/11"

def play(rtspUrl):
    cap = cv2.VideoCapture(rtspUrl)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f'fps: {fps} resolution: {width}x{height}')
    ret, frame = cap.read()
    while ret:
        ret, frame = cap.read()
        cv2.imshow('play', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


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


thread1 = threading.Thread(target=push_stream, name='1', args=(camera_path, rtmpUrl, ))
thread2 = threading.Thread(target=play, name='2', args=(rtmpUrl,))

# 开启线程
thread1.start()
time.sleep(4)
thread2.start()
