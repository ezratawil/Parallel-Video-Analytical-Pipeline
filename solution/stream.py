import cv2


def streamer(queue, path):
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        while not queue.full():
            ret, frame = cap.read()
            queue.put((ret, frame))  # enqueue
            if not ret:
                print("exit stream")
                cap.release()
                break
