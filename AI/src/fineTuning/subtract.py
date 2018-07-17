import os
import glob
import cv2
from datetime import datetime
from datetime import timedelta


img_dir = "/Users/mamacintoshc/Desktop/all_230_stack/"
background = "Background"
format = '%Y%m%d%H%M%S%f'

all_classes = glob.glob(img_dir + "*")

all_bg_date = []
all_bg_path = []

for class_i in all_classes:
    if background in class_i:
        all_class_i_imgs = glob.glob(class_i + "/*jpg")
        # for each img in class folder
        for img_path in all_class_i_imgs:
            img_path_correct = img_path[len(class_i)+1:]
            split = img_path_correct.split('_')
            #print (split[0])
            if len(all_bg_path) != 0:
                if split[0] not in all_bg_path[-1]:
                    date = datetime.strptime(split[0], format)
                    all_bg_date.append(date)
                    all_bg_path.append(split[0])
            else:
                date = datetime.strptime(split[0], format)
                all_bg_date.append(date)
                all_bg_path.append(split[0])

print (all_bg_date)
print (all_bg_path)

# for each class (folder)
for class_i in all_classes:
    if background not in class_i:
        all_class_i_imgs = glob.glob(class_i + "/*jpg")
        print (len(all_class_i_imgs))
        #print (all_class_i_imgs)
        # for each img in class folder
        for img_path in all_class_i_imgs:
            img_path_correct = img_path[len(class_i)+1:]
            split = img_path_correct.split('_')
            #print (split[0])
            date = datetime.strptime(split[0], format)
            delta = timedelta(hours=23, minutes = 59)
            path_bg = ''
            i = 0
            for bg_date in all_bg_date:
                dt = date - bg_date
                
                if dt.days == 0:
                    if dt.seconds < delta.seconds:
                        delta = dt
                        path_bg = all_bg_path[i]
                else:
                    dt = bg_date - date
                    if dt.days == 0:
                        if dt.seconds < delta.seconds:
                            delta = dt
                            path_bg = all_bg_path[i]
                i += 1
            if path_bg != '':
                #print path_bg
                path_img = class_i + "/" + split[0] + '_' + split[1]
                path_save = class_i + "/subtract/" + split[0] + '_sub_' + split[1]
                path_bg = img_dir + background + "/" + path_bg + '_' + split[1]
                print path_bg
                #print path_img
                bg_img = cv2.imread(path_bg)
                img = cv2.imread(path_img)
                # cv2.imshow('img', img)
                # cv2.imshow('bg_img', bg_img)
                # cv2.waitKey(3000)
                # cv2.destroyAllWindows()
                
                subtract_img = cv2.subtract(img, bg_img)
                cv2.imwrite(path_save, subtract_img)
                # cv2.imshow('img', subtract_img)
                # cv2.waitKey(300)
                # cv2.destroyAllWindows()

            #print date
            #img = cv2.imread(split[0])





    

