"""Build TFRecords from ImageNet and recycle dataset."""
import random
import logging

import tensorflow as tf

from logging_utils import setup_logging
from utils import process_dataset
import build_negative
import build_tfrecord


FLAGS = tf.flags.FLAGS


def define_flags():
    """Define flags to config building process."""
    # Output data Flags
    tf.flags.DEFINE_string(
        "tfrecord_output_dir",
        "data/interim/both_v1",
        "Output directory for TFRecord files."
    )

    # Input data Flags
    tf.flags.DEFINE_string(
        "negative_image_list",
        "resources/negative_images.csv",
        "File contains list of images to build dataset from."
    )
    tf.flags.DEFINE_string(
        "negative_image_dir",
        "data/ILSVRC2012_val/",
        "Directory of ImageNet's images."
    )
    tf.flags.DEFINE_string(
        "negative_label_dir",
        "data/val/",
        "Directory of ImageNet's labels."
    )

    tf.flags.DEFINE_string(
        "positive_train_dir",
        "/media/ubuntu/Data/dataset/recycle/data/raw/non_dup_v1/split/train",
        "Image directory of recycle training set."
    )
    tf.flags.DEFINE_string(
        "positive_val_dir",
        "/media/ubuntu/Data/dataset/recycle/data/raw/non_dup_v1/split/val",
        "Image directory of recycle validation set."
    )
    tf.flags.DEFINE_string(
        "positive_test_dir",
        "/media/ubuntu/Data/dataset/recycle/data/raw/non_dup_v1/split/test",
        "Image directory of recycle test set."
    )

    # Build config Flags
    tf.flags.DEFINE_float(
        "negative_min_area",
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
        16,
        "Number of shards for negative training set."
    )

    tf.flags.DEFINE_float(
        "val_percentage",
        0.1,
        "Percentage of images to put in validation set."
    )
    tf.flags.DEFINE_integer(
        "val_shards",
        4,
        "Number of shards for negative validation set."
    )

    tf.flags.DEFINE_integer(
        "test_shards",
        4,
        "Number of shards for negative test set."
    )

    tf.flags.DEFINE_integer(
        "num_threads",
        8,
        "Number of threads to write images in TFRecord files."
    )


def _merge_datasets(positive_data, negative_data):
    """Merge positive and negative datasets."""
    return positive_data + negative_data


def main(unused_argv):
    """Build TFRecords."""
    random.seed(333)

    setup_logging(filename="tfrecord_both.log")
    logger = logging.getLogger()
    logger.info("Start building both datasets")

    if not tf.gfile.IsDirectory(FLAGS.tfrecord_output_dir):
        tf.gfile.MakeDirs(FLAGS.tfrecord_output_dir)

    # Get negative samples
    negative_train, negative_val, negative_test = \
        build_negative.get_image_infos(FLAGS.negative_image_list,
                                       FLAGS.negative_image_dir,
                                       FLAGS.train_percentage,
                                       FLAGS.val_percentage,
                                       FLAGS.negative_label_dir,
                                       FLAGS.negative_min_area)

    logger.info("Negative images split: %d/%d/%d",
                len(negative_train), len(negative_val), len(negative_test))

    # Get positive samples
    positive_train, positive_val, positive_test, num_classes = \
        build_tfrecord.get_image_infos(FLAGS.positive_train_dir,
                                       FLAGS.positive_val_dir,
                                       FLAGS.positive_test_dir,
                                       FLAGS.tfrecord_output_dir)

    logger.info("Positive images split: %d/%d/%d",
                len(positive_train), len(positive_val), len(positive_test))

    # Merge both datasets
    image_train = _merge_datasets(positive_train, negative_train)
    image_val = _merge_datasets(positive_val, negative_val)
    image_test = _merge_datasets(positive_test, negative_test)

    subset = FLAGS.subset_to_build.lower().strip()
    assert subset == "all" or subset == "train" or subset == "val" or \
        subset == "test"

    if subset == "train" or subset == "all":
        process_dataset("both-train", FLAGS.train_shards, image_train,
                        num_classes + 1, FLAGS.num_threads,
                        FLAGS.tfrecord_output_dir)

    if subset == "val" or subset == "all":
        process_dataset("both-val", FLAGS.val_shards, image_val,
                        num_classes + 1, FLAGS.num_threads,
                        FLAGS.tfrecord_output_dir)

    if subset == "test" or subset == "all":
        process_dataset("both-test", FLAGS.test_shards, image_test,
                        num_classes + 1, FLAGS.num_threads,
                        FLAGS.tfrecord_output_dir)

    logger.info("Finish building both datasets.")


if __name__ == '__main__':
    define_flags()
    tf.app.run()
