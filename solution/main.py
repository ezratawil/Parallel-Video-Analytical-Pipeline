import multiprocessing as mp
import stream
import draw
import detect
from config import video_file_path


def parallelize(path):
    manager = mp.Manager()
    frame_queue = manager.Queue(500)
    detection_queue = manager.Queue(500)

    streamer = mp.Process(target=stream.streamer, args=(frame_queue, path))
    detector = mp.Process(target=detect.detect, args=(frame_queue, detection_queue))
    drawer = mp.Process(target=draw.draw, args=(detection_queue,))

    processes = [streamer, detector, drawer]
    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()


if __name__ == '__main__':
    parallelize(video_file_path)
