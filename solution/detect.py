import cv2
import numpy as np

from config import (NUM_OF_FRAMES_TO_STACK,
                    lk_params)


def get_points_from_cnts(cnts):
    points = []
    bboxs = []
    for c in cnts:
        # print(cv2.contourArea(c))   # uncomment tis for testing
        # if the contour is too small or too big, ignore it
        if cv2.contourArea(c) < 500 or cv2.contourArea(c) > 50000:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        (x, y, w, h) = cv2.boundingRect(c)
        center_x, center_y = (x + x + w) / 2, (y + y + h) / 2
        points.append([[center_x, center_y]])  # insert the centroid
        bboxs.append((x, y, w, h))

    return np.array(points).astype("float32"), bboxs


def detect(frame_queue, detection_queue):
    # mog background subtraction
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

    # initiate the mog2 to learn the background
    for i in range(1, NUM_OF_FRAMES_TO_STACK):
        # Take first NUM_OF_FRAMES_TO_STACK frame and find corners in it

        ret, frame = frame_queue.get()
        old_blur = cv2.GaussianBlur(frame, (21, 21), 0)
        fgmask = fgbg.apply(old_blur, learningRate=1)
        threshold_frame = cv2.dilate(fgmask, None, iterations=2)
        cnts = cv2.findContours(threshold_frame, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        p0, _ = get_points_from_cnts(cnts[0])

        old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = frame_queue.get()
        if not ret:
            detection_queue.put((ret, [], [], [], []))
            # print("exiting detect...")
            break
        frame_blur = cv2.GaussianBlur(frame, (21, 21), 0)
        fgmask = fgbg.apply(frame_blur, learningRate=0.2)
        threshold_frame = cv2.dilate(fgmask, None, iterations=2)
        cnts = cv2.findContours(threshold_frame, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

        p0, bboxs = get_points_from_cnts(cnts[0])

        if not p0.size:
            continue

        # calculate optical flow
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Select good points
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        if not detection_queue.full():
            detection_queue.put((ret, frame, good_new, good_old, bboxs))

        # Now update the previous frame
        old_gray = frame_gray.copy()
