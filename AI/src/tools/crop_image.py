"""Crop real images and perform perspective transform."""
import os

import cv2
import numpy as np


def main():
    final_points = [[5, 478], [78, 4], [612, 477], [541, 5]]
    rect = np.array([final_points[0], final_points[1],
                     final_points[3], final_points[2]], dtype=np.float32)
    dst = np.array([[0, 480 - 1],
                    [0, 0],
                    [640 - 1, 0],
                    [640 - 1, 480 - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(rect, dst)

    root_path = "/home/ubuntu/Pictures/image_original"
    filepaths = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            filepaths.append(os.path.join(dirpath, filename))

    output_dir = "/home/ubuntu/Pictures/image_crop"
    for filepath in filepaths:
        output_subdir = os.path.join(output_dir,
                                     os.path.dirname(filepath).split('/')[-1])
        if not os.path.exists(output_subdir):
            os.mkdir(output_subdir)

        image = cv2.imread(filepath)
        warped = cv2.warpPerspective(image, M, (640, 480))

        filename = os.path.basename(filepath)
        cv2.imwrite(os.path.join(output_subdir, filename), warped)


if __name__ == '__main__':
    main()
