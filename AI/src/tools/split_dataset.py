"""Split raw dataset into train/val/test subset."""
import os
import argparse
import logging
import random
from shutil import copyfile

from logging_utils import setup_logging
from utils import valid_filename


def create_dir(*arg):
    """Create directory if not existed."""
    path = os.path.join(*arg)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def copy_data(filepaths, output_dir):
    """Copy data to output directory."""
    logger = logging.getLogger()

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        subclass_name = os.path.basename(os.path.normpath(os.path.dirname(
            filepath)))
        filename = subclass_name.strip().replace(' ', '_') + '_' + filename
        output_filepath = os.path.join(output_dir, filename)
        copyfile(filepath, output_filepath)
        logger.info("Copy file: %s to %s", filepath, output_filepath)


def process_class(root_dir, class_dirs, class_names, train_dir, val_dir,
                  test_dir, train_percentage, val_percentage):
    """Split all object class's data with a given ratio."""
    logger = logging.getLogger()
    logger.info("Processing class")

    for class_dir, class_name in zip(class_dirs, class_names):
        image_in_class = []

        for dirpath, _, filenames in os.walk(os.path.join(root_dir, class_dir)):

            for filename in filenames:
                if not valid_filename(filename):
                    filepath = os.path.join(dirpath, filename)
                    logger.warning("Invalid file: %s", filepath)
                    continue

                image_in_class.append(os.path.join(dirpath, filename))

        num_images = len(image_in_class)
        num_trains = int(train_percentage * num_images)
        num_vals = int(val_percentage * num_images)
        num_tests = num_images - num_trains - num_vals
        logger.info("Class %s split: %s/%s/%s = %s",
                    class_name, num_trains, num_vals, num_tests, num_images)

        # Create output dirs for this class
        train_class_dir = create_dir(train_dir, class_name)
        val_class_dir = create_dir(val_dir, class_name)
        test_class_dir = create_dir(test_dir, class_name)

        # Copy files for this class
        shuffled_idxs = list(range(num_images))
        random.shuffle(shuffled_idxs)
        copy_data([image_in_class[idx] for idx in shuffled_idxs[:num_trains]],
                  train_class_dir)
        copy_data([image_in_class[idx] for idx in shuffled_idxs[num_trains: num_trains + num_vals]],
                  val_class_dir)
        copy_data([image_in_class[idx] for idx in shuffled_idxs[-num_tests:]],
                  test_class_dir)


def parse_args():
    """Parse arguments for splitting dataset."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--recycle_image_dir', type=str,
                        default="data/raw/non_dup_v1/full/TRASH_DATASET_[re]")
    parser.add_argument('--non_recycle_image_dir', type=str,
                        default="data/raw/non_dup_v1/full/TRASH_DATASET_[non]")
    parser.add_argument('--split_output_dir', type=str,
                        default="data/raw/non_dup_v1/split/")

    parser.add_argument('--train_percentage', type=float, default=0.8)
    parser.add_argument('--val_percentage', type=float, default=0.1)

    args = parser.parse_args()
    return args


def main():
    """Split dataset."""
    # Parse arguments
    random.seed(333)
    setup_logging(filename="split_data.log")
    args = parse_args()
    recycle_image_dir = args.recycle_image_dir
    non_recycle_image_dir = args.non_recycle_image_dir
    split_output_dir = args.split_output_dir

    # Create output dirs
    create_dir(split_output_dir)
    train_output_dir = create_dir(split_output_dir, "train")
    val_output_dir = create_dir(split_output_dir, "val")
    test_output_dir = create_dir(split_output_dir, "test")

    # Get all recyclable classes
    recycle_dirs = [f for f in os.listdir(recycle_image_dir)
                    if not os.path.isfile(os.path.join(recycle_image_dir, f))]
    recycle_classes = ["re_" + dir_name.replace(' ', '_').strip()
                       for dir_name in recycle_dirs]
    process_class(recycle_image_dir, recycle_dirs, recycle_classes,
                  train_output_dir, val_output_dir, test_output_dir,
                  args.train_percentage, args.val_percentage)

    # Get all non-recyclable classes
    non_recycle_dirs = [f for f in os.listdir(non_recycle_image_dir)
                        if not os.path.isfile(os.path.join(non_recycle_image_dir, f))]
    non_recycle_classes = ["non_" + dir_name.replace(' ', '_').strip()
                           for dir_name in non_recycle_dirs]
    process_class(non_recycle_image_dir, non_recycle_dirs, non_recycle_classes,
                  train_output_dir, val_output_dir, test_output_dir,
                  args.train_percentage, args.val_percentage)


if __name__ == '__main__':
    main()
