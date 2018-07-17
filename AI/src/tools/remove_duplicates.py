import os
import cv2
import pandas as pd


def delete_files():
    input_file = "./deletes.txt"
    with open(input_file, "rt") as f:
        for line in f:
            line = line.replace("merged_v2", "non_dup_v1").strip()
            if not os.path.exists(line):
                print(line)
            else:
                os.remove(line)


def main():
    input_file = "./notebooks/duplicate_2.csv"
    output_file = "./deletes.txt"
    df = pd.read_csv(input_file, header=None)

    deletes = []
    done = False
    with open(output_file, "wt") as f:
        for i in range(len(df)):
            path1 = df.iloc[i][1]
            path2 = df.iloc[i][2]
            img1 = cv2.imread(path1)
            img2 = cv2.imread(path2)
            cv2.namedWindow('a',cv2.WINDOW_NORMAL)
            cv2.namedWindow('b',cv2.WINDOW_NORMAL)
            cv2.imshow("a", img1)
            cv2.imshow("b", img2)
            cv2.resizeWindow('a', 600, 600)
            cv2.resizeWindow('b', 600, 600)

            key = None
            while True:
                key = cv2.waitKey(0) & 0xff
                if key == ord(' '):
                    deletes.append(path2)
                    f.writelines(path2 + "\n")
                    break
                elif key == ord('n'):
                    break
                elif key == ord('e'):
                    done = True
                    break

            if done:
                print("Last entry:", i)
                break


if __name__ == '__main__':
    delete_files()
