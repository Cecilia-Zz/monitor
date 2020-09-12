import cv2
from address import rtmp_address, camera_address
import multiprocessing as mp


def play(win_name, rtspUrl):
    cap = cv2.VideoCapture(rtspUrl)
    ret, frame = cap.read()
    while ret:
        ret, frame = cap.read()
        cv2.imshow(win_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    # 预览推流
    pc_play = []
    for camera_path, rtmpUrl in zip(camera_address, rtmp_address):
        pc_play.append(mp.Process(target=play, args=(camera_path, rtmpUrl)))
    for process in pc_play:
        process.start()

