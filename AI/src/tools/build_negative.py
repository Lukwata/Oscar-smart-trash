"""Build TFRecords from ImageNet dataset."""
import os
import csv
import random
import logging
import xml.etree.ElementTree as ET

import tensorflow as tf

from logging_utils import setup_logging
from utils import process_dataset


FLAGS = tf.flags.FLAGS


def define_flags():
    """Define flags to config building process."""
    # Output data Flags
    tf.flags.DEFINE_string(
        "tfrecord_output_dir",
        "/media/ubuntu/Data/dataset/recycle/data/interim/test",
        "Output directory for TFRecord files."
    )

    # Input data Flags
    tf.flags.DEFINE_string("image_list",
                           "resources/negative_images.csv",
                           "File contains list of images to build dataset from.")
    tf.flags.DEFINE_string("image_dir",
                           "data/ILSVRC2012_val/",
                           "Directory of ImageNet's images.")
    tf.flags.DEFINE_string("label_dir",
                           "data/val/",
                           "Directory of ImageNet's labels.")

    # Build config Flags
    tf.flags.DEFINE_float(
        "min_area",
        0.4,
        "Minimum area of the object to consider valid."
    )

    tf.flags.DEFINE_string(
        "subset_to_build",
        "all",
        "The ImageNet dataset to build (train/val/test/all)."
    )

    tf.flags.DEFINE_float(
        "train_percentage",
        0.8,
        "Percentage of images to put in training set."
    )
    tf.flags.DEFINE_integer(
        "train_shards",
        4,
        "Number of shards for negative training set."
    )

    tf.flags.DEFINE_float(
        "val_percentage",
        0.1,
        "Percentage of images to put in validation set."
    )
    tf.flags.DEFINE_integer(
        "val_shards",
        2,
        "Number of shards for negative validation set."
    )

    tf.flags.DEFINE_integer(
        "test_shards",
        2,
        "Number of shards for negative test set."
    )

    tf.flags.DEFINE_integer(
        "num_threads",
        4,
        "Number of threads to write images in TFRecord files."
    )


def convert_to_infos(images):
    """Convert to image infos format with label -1."""
    image_infos = []
    for filepath in images:
        label = -1
        image_infos.append({"filepath": filepath, "label": label})
    return image_infos


def parse_bbox_xml(file_name):
    """Get image info and list of bounding boxes from a xml file"""
    logger = logging.getLogger()

    try:
        tree = ET.parse(file_name)
    except Exception as e:
        msg = "Failed to parse {}: {}".format(file_name, e)
        logger.warning(msg)
        return None, None

    root = tree.getroot()
    image_size = root.find("size")
    image_width = int(image_size.find("width").text)
    image_height = int(image_size.find("height").text)

    image_info = {
        "width": image_width,
        "height": image_height
    }

    # Loop through each bbox, get coordinates and object WordNet ID
    bbox = []
    for obj in root.iter("object"):
        name = obj.find("name").text
        bndbox = obj.find("bndbox")

        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        bbox.append({"name": name,
                     "xmin": xmin,
                     "ymin": ymin,
                     "xmax": xmax,
                     "ymax": ymax})
    return image_info, bbox


def is_valid(label_name, wnid, label_dir, min_area):
    """Check if an image is valid by checking the size of the largest object.

    A valid image contains at least one object of interest with area larger than
    a threshold.

    Args:
        label_name: str, name of the file contains the description of the image.
        wnid: str, the WordNetID of interest.
        label_dir: str directory of the label files.
        min_area: float minimum percentage of object to consider valid.

    Returns:
        valid: bool, whether the image is considered as valid.

    """
    image_info, bbox = parse_bbox_xml(
        os.path.join(label_dir, label_name))
    if not image_info:
        return False

    image_size = image_info["width"] * image_info["height"] * 1.0
    max_size = 0.0
    for b in bbox:
        if b["name"].strip().lower() != wnid:
            continue

        obj_size = abs((b["xmax"] - b["xmin"]) * (b["ymax"] - b["ymin"]) * 1.0)
        if obj_size > max_size:
            max_size = obj_size

    return max_size / image_size > min_area


def split_images(images, train_percentage, val_percentage):
    """Split the images dataset into train/val/test set."""
    image_train, image_val, image_test = [], [], []
    for iid in images:
        num_images = len(images[iid])
        num_trains = int(train_percentage * num_images)
        num_vals = int(val_percentage * num_images)
        num_tests = num_images - num_trains - num_vals

        image_train.extend(images[iid][:num_trains])
        image_val.extend(images[iid][num_trains: num_trains + num_vals])
        image_test.extend(images[iid][-num_tests:])

    return image_train, image_val, image_test


def get_valid_images(image_list, image_dir, label_dir, min_area):
    """Get all valid images and sort by classes to build balance datasets.

    Args:
        image_list: list of string name of the images.
        image_dir: string path to the folder contains the images.
        label_dir: str directory of the label files.
        min_area: float minimum percentage of object to consider valid.

    Returns:
        valid_images: dict with key is the id of the classes and value is the
        list of the path of valid images.

    """
    valid_images = {}
    with open(image_list, "rt") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header

        for i, row in enumerate(csv_reader):
            image_name, label_name, wnid, iid = row
            if not is_valid(label_name, wnid, label_dir, min_area):
                continue

            image_path = os.path.join(image_dir, image_name)
            if iid in valid_images:
                valid_images[iid].append(image_path)
            else:
                valid_images[iid] = [image_path]

    return valid_images


def get_image_infos(image_list, image_dir, train_percentage, val_percentage,
                    label_dir, min_area):
    """Get lists of train/val/test image infos."""
    valid_images = get_valid_images(image_list, image_dir, label_dir, min_area)

    image_train, image_val, image_test = split_images(valid_images,
                                                      train_percentage,
                                                      val_percentage)

    image_train = convert_to_infos(image_train)
    image_val = convert_to_infos(image_val)
    image_test = convert_to_infos(image_test)
    return image_train, image_val, image_test


def main(unused_argv):
    """Build TFRecords."""
    random.seed(333)

    setup_logging(filename="tfrecord_negative.log")
    logger = logging.getLogger()
    logger.info("Start building negative dataset")

    if not tf.gfile.IsDirectory(FLAGS.tfrecord_output_dir):
        tf.gfile.MakeDirs(FLAGS.tfrecord_output_dir)

    subset = FLAGS.subset_to_build.lower().strip()
    assert subset == "all" or subset == "train" or subset == "val" or \
        subset == "test"

    image_train, image_val, image_test = get_image_infos(
        FLAGS.image_list, FLAGS.image_dir,
        FLAGS.train_percentage, FLAGS.val_percentage,
        FLAGS.label_dir, FLAGS.min_area)

    if subset == "train" or subset == "all":
        process_dataset("negative-train", FLAGS.train_shards, image_train,
                        1, FLAGS.num_threads, FLAGS.tfrecord_output_dir)

    if subset == "val" or subset == "all":
        process_dataset("negative-val", FLAGS.val_shards, image_val,
                        1, FLAGS.num_threads, FLAGS.tfrecord_output_dir)

    if subset == "test" or subset == "all":
        process_dataset("negative-test", FLAGS.test_shards, image_test,
                        1, FLAGS.num_threads, FLAGS.tfrecord_output_dir)

    logger.info("Finish building negative dataset")


if __name__ == '__main__':
    define_flags()
    tf.app.run()
