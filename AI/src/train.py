"""Finetune pretrained models on recycle dataset."""
import json

import tensorflow as tf
from tensorflow.contrib import learn

try:
    import horovod.tensorflow as hvd
except:
    hvd = None

from config import TrainConfig, EvaluateConfig, ModelConfig
from models import model_fn
from input_utils import input_fn

tf.logging.set_verbosity(tf.logging.INFO)


##################
# Training Flags #
##################
tf.flags.DEFINE_string(
    "train_dir",
    "logs/TRASHNET2CLASS_VGG16",
    "Directory for saving and loading model checkpoints."
)
tf.flags.DEFINE_string(
    "trainable_scopes",
    #None,
    #"output_layer",
    # "resnet_v1_101/logits",
    "vgg_16/fc8, vgg_16/conv5/conv5_3",   #aux_11
    # "InceptionResnetV2/Logits",
    "Comma-separated list of scopes to filter the set of variables to train."
    "By default, None would train all the variables."
)
tf.flags.DEFINE_bool(
    "horovod",
    False,
    # True,
    "Use Horovod for multi-gpu training."
)


###########################
# Pre-trained Model Flags #
###########################
tf.flags.DEFINE_string(
    "checkpoint_path",
    # "/media/data/dbao/recycle/logs/NODROP06/",
    # "pretrained_models/resnet_v1_101/resnet_v1_101.ckpt",
    #"pretrained_models/nasnet-a_large_04_10_2017/model.ckpt",
    "pretrained_models/vgg_16/vgg_16.ckpt",
    # "/media/data/dbao/recycle/pretrained_models/inception_resnet_v2_2016_08_30.ckpt",
    "The path to a checkpoint from which to fine-tune."
)
tf.flags.DEFINE_string(
    "checkpoint_exclude_scopes",
    # None,
    # "resnet_v1_101/logits,output_layer",
    "vgg_16/fc8, vgg_16/conv5/conv5_3", #aux_11
    # "InceptionResnetV2/Logits,InceptionResnetV2/AuxLogits,output_layer",
    "Comma-separated list of scopes of variables to exclude when restoring."
    "from a checkpoint."
)


##############
# Data Flags #
##############
tf.flags.DEFINE_integer(
    "num_classes",
    2,
    "Total number of classes of recycle dataset."
)

tf.flags.DEFINE_string(
    "obj_to_class_file",
    "data/interim/trashnet_2/obj_to_class.json",
    "Path to the JSON file contains the mapping from object to class."
)

tf.flags.DEFINE_string(
    "train_metadata",
    "data/interim/trashnet_2/trashnet-train_metadata.json",
    "JSON file stores the metadata of the training set."
)
tf.flags.DEFINE_string(
    "train_file_pattern",
    "data/interim/trashnet_2/trashnet-train-*",
    "File pattern of training set sharded TFRecord files."
)
tf.flags.DEFINE_integer(
    "examples_per_train_shard",
    150,
    "Number of training examples per shard."
)

tf.flags.DEFINE_string(
    "eval_file_pattern",
    "data/interim/trashnet_2/trashnet-val-*",
    "File pattern of validation set sharded TFRecord files."
)
tf.flags.DEFINE_integer(
    "examples_per_eval_shard",
    124,
    "Number of evaluation examples per shard."
)


def get_num_shards(file_pattern):
    """Get number of data shards to approximate training hyper-parameters"""
    data_files = []
    for pattern in file_pattern.split(","):
        data_files.extend(tf.gfile.Glob(pattern))
    return len(data_files)


def build_model_and_train():
    """Build model and finetune on recycle dataset."""
    FLAGS = tf.flags.FLAGS
    horovod = FLAGS.horovod

    config = None
    bcast_hook = None
    model_dir = FLAGS.train_dir
    if horovod:
        hvd.init()

        # Horovod: pin GPU to be used to process local rank (one GPU per
        # process)
        config = tf.ConfigProto()
        config.gpu_options.visible_device_list = str(hvd.local_rank())

        # Horovod: save checkpoints only on worker 0 to prevent other workers
        # from corrupting them.
        model_dir = FLAGS.train_dir if hvd.rank() == 0 else None

        # Horovod: BroadcastGlobalVariablesHook broadcasts initial variable
        # states from rank 0 to all other processes. This is necessary to ensure
        # consistent initialization of all workers when training is started with
        # random weights or restored from a checkpoint.
        bcast_hook = hvd.BroadcastGlobalVariablesHook(0)

    # Generate config object
    model_config = ModelConfig()
    train_config = TrainConfig(get_num_shards(FLAGS.train_file_pattern),
                               FLAGS.examples_per_train_shard)
    eval_config = EvaluateConfig(get_num_shards(FLAGS.eval_file_pattern),
                                 FLAGS.examples_per_eval_shard)

    # Read metadata of the dataset
    with open(FLAGS.train_metadata, "r") as f:
        metadata = json.loads(f.read())
    samples_per_class = metadata["samples_per_class"]

    # Check if there's negative class in the dataset
    num_negatives = 0
    if len(samples_per_class) > FLAGS.num_classes:
        num_negatives = samples_per_class[-1]
        samples_per_class.pop()

    # Read mapping from object to class (recycle/non-recycle)
    with open(FLAGS.obj_to_class_file, "r") as f:
        data = json.loads(f.read())
        obj_to_class = [0] * len(data)
        for obj_id in data:
            obj_to_class[int(obj_id)] = data[obj_id]

    # Build model
    run_config = tf.estimator.RunConfig(save_checkpoints_secs=1200,
                                        session_config=config)
    params = {
        "num_classes": FLAGS.num_classes,
        "network_name": model_config.network_name,
        "output_type": model_config.output_type,
        "obj_to_class": obj_to_class,
        "num_negatives": num_negatives,
        "samples_per_class":  samples_per_class,
        "train_config": train_config,
        "horovod": horovod
    }
    estimator = tf.estimator.Estimator(model_fn, model_dir=model_dir,
                                       config=run_config, params=params)

    preprocess_config = {
        "network_name": model_config.network_name,
        "warp": model_config.warp
    }

    # Start training and evaluating
    def train_input_fn():
        """First class function for train input function."""
        return input_fn(FLAGS.train_file_pattern, True,
                        train_config.batch_size, preprocess_config)

    def eval_input_fn():
        """First class function for evaluate input function."""
        return input_fn(FLAGS.eval_file_pattern, False,
                        eval_config.batch_size, preprocess_config)

    # Scale number of training and evaluation steps if needed
    train_steps = train_config.num_iters
    eval_steps = eval_config.num_iters
    if horovod:
        train_steps = train_steps // hvd.size()
        eval_steps = eval_steps // hvd.size()

    # Set min_eval_frequency to 0 to ignore default ValidationMonitor
    min_eval_frequency = 0
    experiment = learn.Experiment(
        estimator,
        train_input_fn,
        eval_input_fn,
        min_eval_frequency=min_eval_frequency,
        train_steps=train_steps,
        eval_steps=eval_steps)

    # We create our own monitor to do early stopping
    validation_monitor = learn.monitors.ValidationMonitor(
        input_fn=experiment._eval_input_fn,
        eval_steps=experiment._eval_steps,
        metrics=experiment._eval_metrics,
        every_n_steps=1,  # Evaluate as soon as a new checkpoint is available
        hooks=experiment._eval_hooks,
        early_stopping_rounds=train_config.early_stopping_rounds,
        early_stopping_metric_minimize=False,  # Maxmize accuracy
        early_stopping_metric="accuracy/full/object")

    # Add to the list of train hooks
    train_hooks = [validation_monitor]
    if horovod:
        train_hooks += bcast_hook
    experiment.extend_train_hooks(train_hooks)

    # Train and evaluate model
    experiment.train_and_evaluate()


def main(unused_argv):
    """Setup and train."""
    train_dir = tf.flags.FLAGS.train_dir
    if not tf.gfile.IsDirectory(train_dir):
        tf.gfile.MakeDirs(train_dir)

    build_model_and_train()


if __name__ == '__main__':
    tf.app.run()
