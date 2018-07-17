"""Export trained model for serving."""
import json
import tensorflow as tf

from models import model_fn
from input_utils import decode_image_string_tensor, preprocess_image
from config import ModelConfig


tf.flags.DEFINE_string('checkpoint_dir', 'logs/CROP_NEW_00',
                       "Directory where to read training checkpoints.")
tf.flags.DEFINE_string('output_dir', 'saved_models/CROP_NEW_00/',
                       "Directory where to export inference model.")
tf.flags.DEFINE_integer('num_classes', 10,
                        "Total number of classes of recycle dataset.")
tf.flags.DEFINE_string("obj_to_class_file",
                       "data/interim/real_crop_v1/obj_to_class.json",
                       "Path to the JSON file contains the mapping from object to class.")

FLAGS = tf.app.flags.FLAGS
model_config = ModelConfig()


def serving_input_receiver_fn():
    """Parse and preprocess for serving model."""
    encoded_image_string_tensor = tf.placeholder(
        dtype=tf.string, shape=[None], name='encoded_image_string_tensor')
    receiver_tensors = {
        'image': encoded_image_string_tensor
    }

    preprocess_config = {
        "network_name": model_config.network_name,
        "warp": model_config.warp
    }

    images = tf.map_fn(decode_image_string_tensor, encoded_image_string_tensor,
                       back_prop=False, dtype=tf.uint8)
    images = tf.map_fn(lambda image: preprocess_image(image, False, preprocess_config),
                       images, back_prop=False, dtype=tf.float32)

    features = {
        'image': images
    }
    return tf.estimator.export.ServingInputReceiver(features, receiver_tensors)


def main(unused_argv=None):
    """Build estimator and export saved model."""
    # Create output directory if not existed
    if not tf.gfile.IsDirectory(FLAGS.output_dir):
        tf.gfile.MakeDirs(FLAGS.output_dir)

    # Read mapping from object to class (recycle/non-recycle)
    with open(FLAGS.obj_to_class_file, "r") as f:
        data = json.loads(f.read())
        obj_to_class = [0] * len(data)
        for obj_id in data:
            obj_to_class[int(obj_id)] = data[obj_id]

    # Build estimator
    params = {
        "num_classes": FLAGS.num_classes,
        "network_name": model_config.network_name,
        "output_type": model_config.output_type,
        "obj_to_class": obj_to_class
    }
    estimator = tf.estimator.Estimator(model_fn, model_dir=FLAGS.checkpoint_dir,
                                       params=params)

    # Export SavedModel
    estimator.export_savedmodel(FLAGS.output_dir, serving_input_receiver_fn)


if __name__ == '__main__':
    tf.app.run()
