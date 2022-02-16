import cv2
from config import colors
import numpy as np


def draw(detection_queue):
    # Create a mask image for drawing purposes
    mask = np.zeros(shape=(540, 960, 3), dtype='uint8')  # create mask the size of image
    while True:
        tup = detection_queue.get() # dequeue
        ret = tup[0]
        if not ret:
            break
        frame, good_new, good_old, bboxs = tup[1], tup[2], tup[3], tup[4]  # unpack
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            a, b, c, d = int(a), int(b), int(c), int(d)
            mask = cv2.line(mask, (a, b), (c, d), colors[i].tolist(), 2)
            frame = cv2.circle(frame, (a, b), 7, colors[i].tolist(), -1)

        # draw the bounding box
        for (x, y, w, h) in bboxs:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        img = cv2.add(frame, mask)
        cv2.imshow('frame', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
