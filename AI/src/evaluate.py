"""Evaluate a trained models on recycle dataset."""
import json

import tensorflow as tf

from config import EvaluateConfig, ModelConfig
from models import model_fn
from input_utils import input_fn

tf.logging.set_verbosity(tf.logging.INFO)


###########################
# Pre-trained Model Flags #
###########################
tf.flags.DEFINE_string(
    "model_dir",
    "logs/REFTAUG00/",
    "The path to a checkpoint from which to evaluate.")


##############
# Data Flags #
##############
tf.flags.DEFINE_integer(
    "num_classes",
    30,
    "Total number of classes of recycle dataset.")

tf.flags.DEFINE_string(
    "eval_metadata",
    "data/interim/merged_v2/recycle-val_metadata.json",
    "JSON file stores the metadata of the validation set.")
tf.flags.DEFINE_string(
    "eval_file_pattern",
    "data/interim/merged_v2/recycle-val-*",
    "File pattern of validation set sharded TFRecord files.")
tf.flags.DEFINE_integer(
    "examples_per_eval_shard",
    750,
    "Number of evaluation examples per shard.")


def get_num_shards(file_pattern):
    """Get number of data shards to approximate training hyper-parameters"""
    data_files = []
    for pattern in file_pattern.split(","):
        data_files.extend(tf.gfile.Glob(pattern))
    return len(data_files)


def build_model_and_evaluate():
    """Build model and evaluate on recycle dataset."""
    FLAGS = tf.flags.FLAGS

    # Generate config object
    model_config = ModelConfig()
    eval_config = EvaluateConfig(get_num_shards(FLAGS.eval_file_pattern),
                                 FLAGS.examples_per_eval_shard)

    # Read metadata of the dataset
    with open(FLAGS.eval_metadata, "r") as f:
        metadata = json.loads(f.read())
    samples_per_class = metadata["samples_per_class"]

    # Build model
    run_config = tf.estimator.RunConfig()
    params = {
        "input_keep_prob": eval_config.input_keep_prob,
        "num_classes": FLAGS.num_classes,
        "samples_per_class":  samples_per_class,
        "network_name": model_config.network_name
    }
    estimator = tf.estimator.Estimator(model_fn, model_dir=FLAGS.model_dir,
                                       config=run_config, params=params)

    preprocess_config = {
        "network_name": model_config.network_name,
        "warp": model_config.warp
    }

    # Start evaluating
    def eval_input_fn():
        """First class function for evaluate input function."""
        return input_fn(FLAGS.eval_file_pattern, False, eval_config.batch_size,
                        preprocess_config)

    estimator.evaluate(eval_input_fn, steps=eval_config.num_iters)


def main(unused_argv):
    """Setup and evaluate."""
    build_model_and_evaluate()


if __name__ == '__main__':
    tf.app.run()
