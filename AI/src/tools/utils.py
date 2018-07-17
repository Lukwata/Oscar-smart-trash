"""Utility for building dataset."""
import os
import sys
import json
import time
import random
import logging
import threading

import tensorflow as tf
import numpy as np


def valid_filename(filename):
    """Check if filename is of an image."""
    valid_exts = [".jpg", ".jpeg", ".png"]
    return os.path.splitext(filename.lower())[-1] in valid_exts


class ImageDecoder(object):
    """Helper class for decoding images in TensorFlow."""

    def __init__(self):
        # Create a single TensorFlow Session for all image decoding calls.
        self._sess = tf.Session()

        # TensorFlow ops for JPEG decoding.
        self._encoded_image = tf.placeholder(dtype=tf.string)
        self._decode_image = tf.image.decode_image(self._encoded_image,
                                                   channels=3)

    def decode_image(self, encoded_image):
        image = self._sess.run(self._decode_image,
                               feed_dict={self._encoded_image: encoded_image})
        assert len(image.shape) == 3
        assert image.shape[2] == 3
        return image


def _int64_feature(value):
    """Wrapper for inserting int64 features into Example proto"""
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _float_feature(value):
    """Wrapper for inserting float features into Example proto"""
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def _bytes_feature(value):
    """Wrapper for inserting bytes features into Example proto"""
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


def _float_feature_list(values):
    """Wrapper for inserting an int64 FeatureList into a SequenceExample"""
    return tf.train.FeatureList(feature=[_float_feature(v) for v in values])


def _bytes_feature_list(values):
    """Wrapper for inserting a bytes FeatureList into a SequenceExample"""
    return tf.train.FeatureList(feature=[_bytes_feature(v) for v in values])


def _convert_to_example(image_info, decoder):
    """Convert an image along with its label to Example proto

    Args:
        image_info (dict): Dictionary contains image information
        decoder (ImageDecoder): Decoder to check for image validity

    Returns:
        example (SequenceExample proto): Contains encoded image and label.
    """
    logger = logging.getLogger()

    image_name = image_info["filepath"]
    with tf.gfile.FastGFile(image_name, "rb") as f:
        encoded_image = f.read()

    try:
        decoded_image = decoder.decode_image(encoded_image)
    except (tf.errors.InvalidArgumentError, AssertionError):
        msg = "Skipping file with invalid JPEG data: %s" % image_name
        logger.warn(msg)
        return None

    height, width, channel = decoded_image.shape[:3]
    label = image_info["label"]

    features = tf.train.Features(feature={
        "image/filename": _bytes_feature(image_name.encode("utf-8")),
        "image/height": _int64_feature(height),
        "image/width": _int64_feature(width),
        "image/channel": _int64_feature(channel),
        "image/data": _bytes_feature(encoded_image),
        "label": _int64_feature(label)
    })

    sequence_example = tf.train.Example(features=features)
    return sequence_example


def _process_image_files_batch(data_name, thread_index, decoder, ranges,
                               image_infos, num_shards, num_threads, output_dir,
                               results):
    """Process and save a subset of images as TFRecord files in one thread

    Args:
        data_name (str): Unique name of the dataset
        thread_index (int): Index of the current thread;
            value in range [0, FLAGS.num_threads)
        decoder (ImageDecoder): Image decoder object to check for image
            validity
        ranges (list): List of 2 elements specifying the range of file_names to
            process for this thread
        image_infos (list): List of images information (filepath and label)
        num_shards (int): Number of shards to save for this dataset
        num_threads (int): Number of threads processing the dataset.
        output_dir (str): The output directory.
        results (list): List to store number of valid images per class that this
            thread processed

    Note:
        Each thread produces N shards where N = num_shards / num_threads. For
        instance, if num_shards = 128, and num_threads = 2, then the first
        thread would produce shards [0, 64).

    """
    logger = logging.getLogger()

    num_shards_per_batch = int(num_shards / num_threads)
    shard_ranges = np.linspace(ranges[0], ranges[1],
                               num_shards_per_batch + 1).astype(int)
    num_images_in_thread = ranges[1] - ranges[0]

    counter = 0
    # Loop through all shards that this thread manages and process all image
    # files belong to this shard
    convert_time = 0
    write_time = 0
    start_time = time.time()
    for shard_index_local in range(num_shards_per_batch):
        shard_index_global = shard_index_local \
            + num_shards_per_batch * thread_index

        shard_name = "{}-{:05d}-of-{:05d}".format(data_name,
                                                  shard_index_global,
                                                  num_shards)
        shard_dir = os.path.join(output_dir, shard_name)
        writer = tf.python_io.TFRecordWriter(shard_dir)

        # Loop through each image belong to this shard and write to file
        shard_counter = 0
        images_in_shard = np.arange(shard_ranges[shard_index_local],
                                    shard_ranges[shard_index_local + 1],
                                    dtype=int)
        for image_index in images_in_shard:
            image_info = image_infos[image_index]
            label = image_info["label"]

            convert_start_time = time.time()
            example = _convert_to_example(image_info, decoder)
            convert_end_time = time.time()
            convert_time += convert_end_time - convert_start_time

            if example is None:
                msg = "[thread {}]: Skip image {}".format(thread_index,
                                                          image_info["filepath"])
                logger.debug(msg)
                continue

            write_start_time = time.time()
            writer.write(example.SerializeToString())
            write_end_time = time.time()
            write_time += write_end_time - write_start_time

            counter += 1
            shard_counter += 1
            results[thread_index][label] += 1
            if not counter % 200:  # Log for every 200 images processed
                msg = "[thread {}]: Processed {} of {} images in thread " \
                      "batch".format(thread_index, counter,
                                     num_images_in_thread)
                logger.info(msg)
                sys.stdout.flush()

        writer.close()

        # Log for every shard this thread processed
        msg = "[thread {}]: Finished a shard, wrote {} images to {}" \
              "".format(thread_index, shard_counter, shard_name)
        logger.info(msg)
    end_time = time.time()
    total_time = end_time - start_time

    # Log timing
    msg = "[thread {}]: Total time: {}, convert time: {}, write time: {}" \
          "".format(thread_index, total_time, convert_time, write_time)
    logger.debug(msg)

    # Log for all images this thread processed
    msg = "[thread {}]: Finish thread, wrote {} images to {} shards" \
          "".format(thread_index, sum(results[thread_index]),
                    num_shards_per_batch)
    logger.info(msg)


def _process_image_files(data_name, image_infos, num_classes, num_shards,
                         num_threads, output_dir):
    """Process all images and write to TFRecord as Example proto

    Args:
        data_name (str): Unique name of the dataset
        image_infos (list): List of image info (filepath and label)
        num_classes (int): Number of classes in the dataset
        num_shards (int): Number of TFRecord files
        num_threads (int): Number of threads to build the records
        output_dir (str): The output directory.

    Returns:
        samples_per_class (list): Number of examples per class.

    """
    logger = logging.getLogger()

    num_threads = min(num_threads, num_shards)
    assert not num_shards % num_threads

    # Break all images into batches with a [ranges[i][0], ranges[i][1]].
    spacing = np.linspace(0, len(image_infos),
                          num_threads + 1).astype(np.int)
    ranges = []
    for i in range(len(spacing) - 1):
        ranges.append([spacing[i], spacing[i + 1]])

    msg = "Launching {} threads for spacings: {}".format(num_threads, ranges)
    logger.info(msg)

    # Use coordinator to monitor threads status
    coord = tf.train.Coordinator()

    decoder = ImageDecoder()
    threads = []
    results = [[0] * num_classes for _ in range(len(ranges))]
    for thread_index in range(len(ranges)):
        args = (data_name, thread_index, decoder, ranges[thread_index],
                image_infos, num_shards, num_threads, output_dir, results)
        t = threading.Thread(target=_process_image_files_batch, args=args)
        t.start()
        threads.append(t)

    # Wait until all threads terminate
    coord.join(threads)
    num_images_written = np.sum(results)
    msg = "Finished writing {}/{} images in data set.".format(
        num_images_written, len(image_infos))
    logger.info(msg)
    sys.stdout.flush()

    # Aggregate threads' result
    samples_per_class = [sum([results[j][i] for j in range(num_threads)])
                         for i in range(num_classes)]
    return samples_per_class


def process_dataset(data_name, num_shards, image_infos, num_classes,
                    num_threads, output_dir):
    """Iterate directories, read image and write to TFRecord files.

    Args:
        data_name: str, unique name of the dataset.
        num_shards: int number of TFRecord files.
        image_infos: list of image infos.
        num_classes: int number of classes of the dataset.
        num_threads: int number of theads to build the dataset.
        output_dir: str directory of the output files.

    """
    logger = logging.getLogger()
    logger.info("Start building %s data", data_name)

    # Shuffle dataset
    shuffled_index = list(range(len(image_infos)))
    random.shuffle(shuffled_index)
    image_infos = [image_infos[i] for i in shuffled_index]

    # Build TFRecords
    samples_per_class = _process_image_files(data_name, image_infos,
                                             num_classes, num_shards,
                                             num_threads, output_dir)

    # Write dataset statistics to file
    with open(os.path.join(output_dir, data_name + "_metadata.json"), "w") as f:
        f.write(json.dumps({
            "samples_per_class": samples_per_class
        }))
