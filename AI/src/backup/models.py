"""Implementation of CNN model for classification."""
import tensorflow as tf
from tensorflow.contrib import slim
try:
    import horovod.tensorflow as hvd
except:
    hvd = None

from slim_models.nets.nets_factory import get_network_fn


def get_init_fn():
    """Returns a function run by the chief worker to warm-start the training.

    Note that the init_fn is only run when initializing the model during the
    very first global step.

    Returns:
        An init function run by the supervisor.

    """
    FLAGS = tf.flags.FLAGS
    if FLAGS.checkpoint_path is None:
        return None

    # Warn the user if a checkpoint exists in the train_dir. Then we"ll be
    # ignoring the checkpoint anyway.
    if tf.train.latest_checkpoint(FLAGS.train_dir):
        tf.logging.info(
            "Ignoring --checkpoint_path because a checkpoint "
            "already exists in {}".format(FLAGS.train_dir))
        return None

    exclusions = []
    if FLAGS.checkpoint_exclude_scopes:
        exclusions = [scope.strip()
                      for scope in FLAGS.checkpoint_exclude_scopes.split(",")]

    variables_to_restore = []
    for var in slim.get_model_variables():
        excluded = False
        for exclusion in exclusions:
            if var.op.name.startswith(exclusion):
                excluded = True
                break
        if not excluded:
            variables_to_restore.append(var)

    # for restore_var in variables_to_restore:
    #     tf.logging.info("Restoring variable {}".format(restore_var.name))

    if tf.gfile.IsDirectory(FLAGS.checkpoint_path):
        checkpoint_path = tf.train.latest_checkpoint(FLAGS.checkpoint_path)
    else:
        checkpoint_path = FLAGS.checkpoint_path

    tf.logging.info("Fine-tuning from %s" % checkpoint_path)

    init_fn = slim.assign_from_checkpoint_fn(checkpoint_path,
                                             variables_to_restore)

    def init_fn_wrapper(scaffold, sess):
        """Scaffold's init_fn call provide self object, wrap to bypass it."""
        return init_fn(sess)

    return init_fn_wrapper


def _get_variables_to_train():
    """Returns a list of variables to train.

    Returns:
        A list of variables to train by the optimizer.

    """
    FLAGS = tf.flags.FLAGS

    if FLAGS.trainable_scopes is None:
        return tf.trainable_variables()
    else:
        scopes = [scope.strip() for scope in FLAGS.trainable_scopes.split(",")]

    variables_to_train = []
    for scope in scopes:
        variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope)
        variables_to_train.extend(variables)
    return variables_to_train


def _get_optimizer_by_name(name, learning_rate, momentum=None):
    """Get optimizer from string name."""
    OPTIMIZER_CLS_NAMES = {
        'Adagrad': tf.train.AdagradOptimizer(learning_rate),
        'Adam': tf.train.AdamOptimizer(learning_rate),
        'Ftrl': tf.train.FtrlOptimizer(learning_rate),
        'Momentum': tf.train.MomentumOptimizer(learning_rate, momentum,
                                               use_nesterov=True),
        'RMSProp': tf.train.RMSPropOptimizer(learning_rate),
        'SGD': tf.train.GradientDescentOptimizer(learning_rate),
    }
    if name not in OPTIMIZER_CLS_NAMES:
        name = 'Adam'
    return OPTIMIZER_CLS_NAMES[name]


def build_eval_metric_ops(labels, logits, learning_rate, is_training,
                          obj_to_class, train_config):
    """Build the metric ops for evaluation in train and eval mode.

    Args:
        labels: Tensor with shape [B,]; stores the labels of the images.
        logits: Tensor with shape [B, num_classes]; stores the logits of the
            images.
        learning_rate: A float32 Tensor representing the current learning rate.
        is_training: bool indicates whether we are in training mode.
        obj_to_class: list of int mapping from object id to class
            (recycle/non-recycle).
        train_config: object with attribute threshold (list of threshold to
            compute false positive/negative metrics).

    Returns:
        eval_metric_ops: dict of the metric ops to monitor during training and
            evaluation mode.

    """
    # Don't use negative samples to calculate accuracy
    weights = tf.to_float(tf.greater_equal(labels, 0))  # Mask of postive ones
    predict_classes = tf.to_int32(tf.argmax(logits, axis=1))
    accuracy = tf.metrics.accuracy(labels, predict_classes, weights=weights)
    predict_equals = tf.to_float(tf.equal(labels, predict_classes))
    sum_accuracy = tf.reduce_sum(weights * predict_equals)
    batch_accuracy = sum_accuracy / tf.maximum(1.0, tf.reduce_sum(weights))

    # Calculate binary accuracy
    binary_predicts = tf.gather(obj_to_class, predict_classes)
    binary_labels = tf.gather(obj_to_class, labels)
    binary_acc = tf.metrics.accuracy(binary_labels, binary_predicts,
                                     weights=weights)
    binary_equals = tf.to_float(tf.equal(binary_labels, binary_predicts))
    sum_binary_acc = tf.reduce_sum(weights * binary_equals)
    batch_binary_accuracy = sum_binary_acc / tf.maximum(1.0,
                                                        tf.reduce_sum(weights))

    # Error counts
    false_negatives = tf.metrics.false_negatives(binary_labels,
                                                 binary_predicts,
                                                 weights=weights)
    false_positives = tf.metrics.false_positives(binary_labels,
                                                 binary_predicts,
                                                 weights=weights)
    # false_negatives_at_t = tf.metrics.false_negatives_at_thresholds(
    #     binary_labels, binary_predicts, train_config.thresholds,
    #     weights=weights)
    # false_positives_at_t = tf.metrics.false_positives_at_thresholds(
    #     binary_labels, binary_predicts, train_config.thresholds,
    #     weights=weights)
    # tf.summary.histogram()

    # The same as average recall of each class
    # mpc_accuracy = tf.metrics.mean_per_class_accuracy(
    #     labels, predict_classes, num_classes=num_classes)

    eval_metric_ops = None
    if not is_training:
        eval_metric_ops = {
            "accuracy/full/object": accuracy,
            "accuracy/full/binary": binary_acc,
            "accuracy/batch/object": (batch_accuracy, tf.no_op()),
            "accuracy/full/false_negatives": false_negatives,
            "accuracy/full/false_positives": false_positives
            # "accuracy/mean_per_class": mpc_accuracy
        }
    else:
        tf.summary.scalar("accuracy/batch/object", batch_accuracy)
        tf.summary.scalar("accuracy/batch/binary", batch_binary_accuracy)
        tf.summary.scalar("learning_rate", learning_rate)
        # for var in variables_to_train:
        #     tf.summary.histogram(var.op.name, var)

    return eval_metric_ops


def build_prediction_output(logits, probs, obj_to_class):
    """Build the output of prediction mode and the output for serving.

    Args:
        logits: float32 Tensor with shape [batch_size, num_classes] represents
            the score (unnormalized log probabilities) of a batch of data.
        probs: the same as logits but with genuine probabilities.
        obj_to_class: list of int mapping from object id to class
            (recycle/non-recycle).

    Returns:
        predictions: dict contains the output for prediction mode:
            - logits: the same as input but with shape [1, batch_size,
            num_classes] to return the whole batch results at a time.
            - probs: the same as logits but for input probs.
            - class_id: int32 Tensor with shape [1, batch_size] represents the
            class with highest probability of each sample in the batch.
        export_outputs: dict contains the output for serving:
            - scores: PredictOutput with probability and class id.

    """
    class_id = tf.argmax(logits, axis=1)  # Single class_id for serving
    batch_range = tf.range(tf.shape(class_id)[0])
    class_id_mat = tf.stack((batch_range, tf.to_int32(class_id)), axis=1)
    binary_predicts = tf.gather(obj_to_class, tf.to_int32(class_id))

    # Single probablity for serving
    prob = tf.gather_nd(probs, class_id_mat)

    export_outputs = {
        "scores": tf.estimator.export.PredictOutput({
            "prob": prob,
            "class_id": class_id,
            "binary_class_id": binary_predicts
        })
    }

    # Additional dim to return a batch at a time (TF returns single example of
    # the batch at a time)
    probs_batch = tf.expand_dims(probs, axis=0)
    logits_batch = tf.expand_dims(logits, axis=0)
    class_id_batch = tf.expand_dims(class_id, axis=0)
    binary_predicts_batch = tf.expand_dims(binary_predicts, axis=0)

    predictions = {
        "logits": logits_batch,
        "probs": probs_batch,
        "class_id": class_id_batch,
        "binary_class_id": binary_predicts_batch
    }
    return predictions, export_outputs


def build_train_op(total_loss, train_config, horovod):
    """Build the training op for training mode.

    This function requires the total_loss so only train and evaluate mode should
    use this.

    Args:
        total_loss: 0D float32 Tensor stores the total loss of the network.
        train_config: object with attributes:
            - initial_learning_rate: float starting learning rate.
            - num_epochs_per_decay: int number of epochs to train before decay
            learning rate.
            - num_inters_per_epoch: int number of iterations of each epoch.
            - decay_rate: float multiplier for each decay of learning rate.
            - optimizer: str representing the name of the optimizer to use.
        horovod: bool indicates whether we use Horovod for multi-gpu training.

    Returns:
        train_op: A Tensor op used for training purpose.
        variables_to_train: list of variables to train.
        learning_rate: A float32 Tensor representing the current learning rate.

    """
    initial_learning_rate = train_config.initial_learning_rate
    num_epochs_per_decay = train_config.num_epochs_per_decay
    num_inters_per_epoch = train_config.num_inters_per_epoch
    decay_rate = train_config.decay_rate
    optimizer_name = train_config.optimizer

    decay_steps = int(num_inters_per_epoch * num_epochs_per_decay)
    global_step = tf.train.get_or_create_global_step()

    # Scale number of decay steps
    if horovod:
        decay_steps = decay_steps // hvd.size()
    learning_rate = tf.train.exponential_decay(
        initial_learning_rate, global_step, decay_steps,
        decay_rate, staircase=True)

    # Scale learning rate by effective batch_size
    if horovod:
        learning_rate = learning_rate * hvd.size()

    optimizer = _get_optimizer_by_name(optimizer_name, learning_rate)

    # Horovod: add Horovod Distributed Optimizer.
    if horovod:
        optimizer = hvd.DistributedOptimizer(optimizer)

    variables_to_train = _get_variables_to_train()
    train_op = slim.learning.create_train_op(
        total_loss, optimizer, variables_to_train=variables_to_train)

    return train_op, variables_to_train, learning_rate


def build_loss(logits, labels, params):
    """Build the loss function for a batch of images.

    For softmax output_type, we calculate the multi-class cross entropy loss.
    For sigmoid output_type, we calculate the binary cross entropy loss for each
    class and average them to get the total_loss.

    Args:
        logits: Tensor with shape [B, num_classes]; stores the logits of the
            images.
        labels: Tensor with shape [B,]; stores the labels of the images.
        params: dict contains the parameters of the model with keys:
            - num_classes: int number of classes of the network.
            - output_type: str representing the type of the output layer units;
            either "softmax" or "sigmoid".
            - num_negatives: int number of negative samples.
            - samples_per_class: list of int representing number of examples for
            each class; used to balance class loss.
            - train_config: object with attribute label_smoothing: float between
            [0, 1] representing the coefficient for label smoothing.

    Returns:
        total_loss (Tensor): The total loss of the network.

    """
    num_classes = params["num_classes"]
    output_type = params["output_type"]
    num_negatives = params["num_negatives"]
    train_config = params["train_config"]
    label_smoothing = train_config.label_smoothing
    one_hot_labels = slim.one_hot_encoding(labels, num_classes)

    # Compute weights of each class to balance classes
    samples_per_class = params["samples_per_class"]
    max_samples = max(samples_per_class) * 1.0

    if output_type == "softmax":
        weights = 1.0
        if train_config.balance_loss:
            # Compute loss weight for each example in batch
            class_weights = [max_samples / v for v in samples_per_class]
            weights = tf.gather(class_weights, labels)

            if train_config.max_loss_weight:
                weights = tf.minimum(weights, train_config.max_loss_weight)

        tf.losses.softmax_cross_entropy(one_hot_labels, logits,
                                        weights=weights,
                                        label_smoothing=label_smoothing)

    elif output_type == "sigmoid":
        weights = 1.0
        if train_config.balance_loss:
            samples_per_class = tf.convert_to_tensor(samples_per_class,
                                                     dtype=tf.float32)
            num_left_out = tf.reduce_sum(samples_per_class) \
                - samples_per_class + num_negatives
            pos_neg_ratio = num_left_out / samples_per_class
            mask = pos_neg_ratio * one_hot_labels
            # Negative samples have weights 1.0
            weights = tf.maximum(mask, 1.0)

            # Thresholding weights if needed
            if train_config.max_loss_weight:
                weights = tf.minimum(weights, train_config.max_loss_weight)

        # The same loss weights for all examples in the batch
        # weights = tf.constant([class_weights], dtype=tf.float32)

        tf.losses.sigmoid_cross_entropy(one_hot_labels, logits,
                                        weights=weights,
                                        label_smoothing=label_smoothing)
    else:
        raise ValueError("Unrecognized output_type: {}".format(output_type))

    # Build loss
    total_loss = tf.losses.get_total_loss()
    return total_loss


def build_logits(image, params, is_training):
    """Build the logits for a batch of images.

    For softmax output_type, the logits correspond to the score of each class
    independently.
    For sigmoid output_type, the logits correspond to the unnormalized log
    likelihood of each class.

    Args:
        image: Tensor with shape [B, H, W, C]; stores the preprocessed images.
        params: dict contains the parameters of the model with keys:
            - network_name: str name of the network.
            - num_classes: int number of classes of the network.
            - output_type: str representing the type of the output layer units;
            either "softmax" or "sigmoid".
            - train_config: object with attribute output_keep_prob (float;
            keep_prob for the layer before output; None for prediction mode.

        is_training: bool indicates whether this is training or evaluation mode.

    Returns:
        logits: Tensor with shape [N, num_classes]; the logits of the batch of
            data.
        probs: Tensor with the same shape as logits; the corresponding
            probabilities of the logits.

    """
    network_name = params["network_name"]
    num_classes = params["num_classes"]
    output_type = params["output_type"]
    train_config = params.get("train_config")
    output_keep_prob = 1.0
    if train_config:
        output_keep_prob = train_config.output_keep_prob

    if output_type == "softmax":
        network_fn = get_network_fn(network_name, num_classes,
                                    is_training=is_training)
        logits, end_points = network_fn(image)
        probs = tf.nn.softmax(logits)  # All class probabilities

    elif output_type == "sigmoid":
        network_fn = get_network_fn(network_name, None,
                                    is_training=is_training)
        features, _ = network_fn(image)
        with tf.variable_scope("output_layer"):
            features = slim.flatten(features)
            features = slim.dropout(features, keep_prob=output_keep_prob,
                                    scope='dropout', is_training=is_training)
            logits = slim.fully_connected(features, num_classes,
                                          activation_fn=None)
            probs = tf.nn.sigmoid(logits)

    else:
        raise ValueError("Unrecognized output_type: {}".format(output_type))

    return logits, probs


def model_fn(features, labels, mode, params, config):
    """Model function for Resnet Estimator."""
    num_classes = params["num_classes"]
    train_config = params.get("train_config")
    obj_to_class = params.get("obj_to_class")
    is_training = mode == tf.estimator.ModeKeys.TRAIN

    image = features["image"]
    if train_config:
        image = slim.dropout(image,
                             keep_prob=train_config.input_keep_prob,
                             is_training=is_training)

    # Build logits
    logits, probs = build_logits(image, params, is_training)

    # Build loss function
    total_loss = None
    if (mode == tf.estimator.ModeKeys.TRAIN or
            mode == tf.estimator.ModeKeys.EVAL):
        total_loss = build_loss(logits, labels, params)

    # Build train_op
    train_op = None
    variables_to_train = None
    learning_rate = None
    if mode == tf.estimator.ModeKeys.TRAIN:
        horovod = params["horovod"]
        train_op, variables_to_train, learning_rate = build_train_op(
            total_loss, train_config, horovod)

    # Build prediction op
    predictions = None
    export_outputs = None
    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions, export_outputs = build_prediction_output(logits, probs, obj_to_class)

    # Build metrics and add summary
    eval_metric_ops = None
    if (mode == tf.estimator.ModeKeys.EVAL or
            mode == tf.estimator.ModeKeys.TRAIN):
        eval_metric_ops = build_eval_metric_ops(labels, logits, learning_rate,
                                                is_training, obj_to_class,
                                                train_config)

    # Scaffold with init_fn to restore from pretrained model
    scaffold = None
    if mode == tf.estimator.ModeKeys.TRAIN:
        scaffold = tf.train.Scaffold(init_fn=get_init_fn())

    return tf.estimator.EstimatorSpec(mode, predictions=predictions,
                                      loss=total_loss, train_op=train_op,
                                      eval_metric_ops=eval_metric_ops,
                                      scaffold=scaffold,
                                      export_outputs=export_outputs)
