import cv2


def streamer(queue, path):
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        while not queue.full():
            ret, frame = cap.read()
            queue.put(frame) # enqueue the frames

        while not queue.empty():
            pass
    cv2.destroyAllWindows()
    cap.release()
