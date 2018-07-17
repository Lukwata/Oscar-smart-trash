"""Utility functions for parsing and preprocessing input data."""
import cv2
import numpy as np
import tensorflow as tf
import tensorflow.contrib as contrib

from slim_models.preprocessing import vgg_preprocessing
from slim_models.preprocessing.preprocessing_factory import get_preprocessing
from slim_models.nets.nets_factory import get_network_fn


def decode_image_string_tensor(encoded_image_string_tensor):
    """Decode an a string of bytes represent an image Tensor."""
    image_tensor = tf.image.decode_image(encoded_image_string_tensor,
                                         channels=3)
    image_tensor.set_shape((None, None, 3))
    return image_tensor


def parser_with_label(record):
    """Parse tf.Example protobuf with label for training/evaluation."""
    keys_to_features = {
        "image/data": tf.FixedLenFeature((), tf.string),
        "label": tf.FixedLenFeature((), tf.int64)
    }
    parsed = tf.parse_single_example(record, features=keys_to_features)

    image = tf.image.decode_image(parsed["image/data"], channels=3)
    image.set_shape((None, None, 3))
    label = parsed["label"]

    return image, label


def preprocess_image(image, is_training, config):
    """Preprocess image for the network."""
    network_name = config.get('network_name')
    warp = config.get('warp')

    # Transform image for top-down view
    if warp:
        image = warp_image(image)

    # Get network function to get input image size
    network_fn = get_network_fn(network_name, None)
    image_size = network_fn.default_image_size

    # Get preprocessing function
    preprocessing_fn = get_preprocessing(network_name, is_training=is_training)
    image = preprocessing_fn(image, image_size, image_size)
    return image


def preprocess(image, label, is_training, config):
    """Preprocess image and label for Resnet."""
    image = preprocess_image(image, is_training, config)
    if label is not None:
        label = tf.to_int32(label)
    return {"image": image}, label


def input_fn(file_patterns, is_training, batch_size, preprocess_config):
    """Input function for Resnet Estimator."""
    filenames = []
    for pattern in file_patterns.split(","):
        filenames.extend(tf.gfile.Glob(pattern))

    # Create the dataset
    dataset = tf.data.TFRecordDataset(filenames, buffer_size=256 * 2 ** 20)
    dataset = dataset.map(parser_with_label,
                          num_parallel_calls=batch_size * 5)
    dataset = dataset.map(
        lambda image, label: preprocess(image, label, is_training,
                                        preprocess_config),
        num_parallel_calls=batch_size * 4)
    # Shuffle before repeat: repeat the shuffle op at the beginning of each
    # epoch (truer to SGD than repeat before shuffle; see here for more info
    # https://stackoverflow.com/questions/47403407/is-tensorflow-dataset-api-slower-than-queues/47946271#47946271)
    dataset = dataset.shuffle(buffer_size=1000)
    dataset = dataset.repeat()
    dataset = dataset.batch(batch_size=batch_size)
    dataset = dataset.prefetch(1)

    # Create iterator for the dataset
    iterator = dataset.make_one_shot_iterator()
    features, labels = iterator.get_next()

    return features, labels


def denormalize_vgg_preprocessing(image):
    """Do mean-addition to get image with values in range [0, 255]."""
    return vgg_preprocessing._mean_image_subtraction(
        image, [-vgg_preprocessing._R_MEAN,
                -vgg_preprocessing._G_MEAN,
                -vgg_preprocessing._B_MEAN])


def denormalize_inception_preprocessing(image):
    """Rescale pixel values to [0, 255]."""
    return (image / 2.0 + 0.5) * 255


def denormalize_image(image, network_name):
    """Reverse the effect of mean-subtraction and normalization."""
    denormalize_fn_map = {
        # 'inception': denormalize_inception_preprocessing,
        # 'inception_v1': denormalize_inception_preprocessing,
        # 'inception_v2': denormalize_inception_preprocessing,
        'inception_v3': denormalize_inception_preprocessing,
        # 'inception_v4': denormalize_inception_preprocessing,
        'inception_resnet_v2': denormalize_inception_preprocessing,
        # 'lenet': lenet_preprocessing,
        # 'mobilenet_v1': denormalize_inception_preprocessing,
        'nasnet_mobile': denormalize_inception_preprocessing,
        'nasnet_large': denormalize_inception_preprocessing,
        'resnet_v1_50': denormalize_vgg_preprocessing,
        'resnet_v1_101': denormalize_vgg_preprocessing,
        'resnet_v1_152': denormalize_vgg_preprocessing,
        'resnet_v1_200': denormalize_vgg_preprocessing,
        # 'resnet_v2_50': denormalize_vgg_preprocessing,
        # 'resnet_v2_101': denormalize_vgg_preprocessing,
        # 'resnet_v2_152': denormalize_vgg_preprocessing,
        # 'resnet_v2_200': denormalize_vgg_preprocessing,
        # 'vgg': denormalize_vgg_preprocessing,
        # 'vgg_a': denormalize_vgg_preprocessing,
        # 'vgg_16': denormalize_vgg_preprocessing,
        # 'vgg_19': denormalize_vgg_preprocessing,
    }
    return denormalize_fn_map[network_name](image)


def preprocess_image_for_visualization(image, config):
    """Preprocess image without mean-subtraction and normalization."""
    network_name = config['network_name']
    warp = config.get('warp')

    # Transform image for top-down view
    if warp:
        image = warp_image(image)

    # Get network function to get input image size
    network_fn = get_network_fn(network_name, None)
    image_size = network_fn.default_image_size

    # Get preprocessing function
    preprocessing_fn = get_preprocessing(network_name, is_training=False)
    image = preprocessing_fn(image, image_size, image_size)
    image = denormalize_image(image, network_name)
    return image


def vgg_normalization(image):
    """Do mean-subtraction to get image with values in range [-127, 128]."""
    return vgg_preprocessing._mean_image_subtraction(
        image, [vgg_preprocessing._R_MEAN,
                vgg_preprocessing._G_MEAN,
                vgg_preprocessing._B_MEAN])


def inception_normalization(image):
    """Scale pixel values to [-1, 1]."""
    return (image / 255.0 - 0.5) * 2.0


def normalize_image(image, network_name):
    """Perform image normalization to get pixel values in appropriate range."""
    normalize_fn_map = {
        # 'inception': inception_normalization,
        # 'inception_v1': inception_normalization,
        # 'inception_v2': inception_normalization,
        'inception_v3': inception_normalization,
        # 'inception_v4': inception_normalization,
        'inception_resnet_v2': inception_normalization,
        # 'lenet': lenet_preprocessing,
        # 'mobilenet_v1': inception_normalization,
        'nasnet_mobile': inception_normalization,
        'nasnet_large': inception_normalization,
        'resnet_v1_50': vgg_normalization,
        'resnet_v1_101': vgg_normalization,
        'resnet_v1_152': vgg_normalization,
        'resnet_v1_200': vgg_normalization,
        # 'resnet_v2_50': vgg_normalization,
        # 'resnet_v2_101': vgg_normalization,
        # 'resnet_v2_152': vgg_normalization,
        # 'resnet_v2_200': vgg_normalization,
        # 'vgg': vgg_normalization,
        # 'vgg_a': vgg_normalization,
        # 'vgg_16': vgg_normalization,
        # 'vgg_19': vgg_normalization,
    }
    return normalize_fn_map[network_name](image)


def warp_image(image):
    """Transform image from angled-view to top-down view."""
    final_points = [[5, 478], [78, 4], [612, 477], [541, 5]]
    rect = np.array([final_points[0], final_points[1],
                     final_points[3], final_points[2]], dtype=np.float32)
    dst = np.array([[0, 480 - 1],
                    [0, 0],
                    [640 - 1, 0],
                    [640 - 1, 480 - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(dst, rect)
    with tf.device('/cpu:0'):
        image = contrib.image.transform(image, M.reshape((-1))[:-1],
                                        interpolation="BILINEAR")

    return image
