"""Visualize to choose the corner of the box in real images."""
import os
import copy
import random

import cv2
import numpy as np


original_image = None
draw_image = None
points = []
final_points = []


def coord_type(x, y):
    if x < 320:
        return int(y < 240)
    else:
        return 2 + int(y < 240)


def click(event, x, y, flags, param):
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    global points, final_points
    if event == cv2.EVENT_LBUTTONDOWN:
        t = coord_type(x, y)
        points[t] = [x, y]
        print("f", final_points)
        if final_points[t] is None:
            print("setting")
            final_points[t] = points[t]

        if t < 2:
            final_points[t][0] = min(final_points[t][0], x)
        else:
            final_points[t][0] = max(final_points[t][0], x)

        draw_image = np.copy(original_image)
        for p in points:
            if p is not None:
                cv2.circle(draw_image, tuple(p), radius=3, color=(0, 255, 0),
                           thickness=-1)

        print(points[t])
        cv2.imshow("image", draw_image)


def main():
    root_path = "/media/ubuntu/Data/dataset/recycle/all_split/real_dataset/train/"
    filepaths = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            filepaths.append(os.path.join(dirpath, filename))

    num_images = 100
    samples = random.choices(filepaths, k=num_images)
    global final_points
    final_points = [None] * 4
    for sample in samples:
        global points, original_image, draw_image
        points = [None] * 4
        draw_image = cv2.imread(sample)
        original_image = np.copy(draw_image)
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", click)
        cv2.imshow("image", draw_image)

        while True:
            key = cv2.waitKey(0) & 0xff
            if key == ord('e'):
                break
            elif key == ord('n'):
                if all([p is not None for p in points]):
                    break

        print("final_points", final_points)

    # [[5, 478], [78, 4], [612, 477], [541, 5]]

if __name__ == '__main__':
    main()
