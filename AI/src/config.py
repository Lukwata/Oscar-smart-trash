"""Configuration for train/eval/test mode."""
import numpy as np


class ModelConfig(object):
    def __init__(self):
        self.network_name = "vgg_16"  # resnet_v1_101, nasnet_large, or inception_resnet_v2   vgg_16
        self.output_type = "softmax"  # softmax or sigmoid
        self.warp = False


class RunConfig(object):
    """Parent class for configuration of all running mode."""

    def __init__(self, num_shards, examples_per_shard):
        super(RunConfig, self).__init__()
        self.examples_per_shard = examples_per_shard
        self.examples = num_shards * examples_per_shard
        self.batch_size = 1  # Dummy value, child class will override
        self.num_inters_per_epoch = 0
        self.num_iters = 0
        self.num_epochs = 0

    def calc_num_iters(self):
        """Calculate number of iteration given the dataset."""
        # Number of iterations per epoch
        self.num_inters_per_epoch = max(self.examples // self.batch_size, 1)

        # Number of iterations to train
        self.num_iters = int(self.num_epochs * self.num_inters_per_epoch)


class TrainConfig(RunConfig):
    """Configuration for training mode."""

    def __init__(self, num_shards, examples_per_shard):
        super(TrainConfig, self).__init__(num_shards, examples_per_shard)
        # Name of the optimizer
        self.optimizer = 'Adam'  #Adam RMSProp

        # The starting learning rate
        self.initial_learning_rate = 0.001

        # The size of a training batch
        self.batch_size = 32

        # Momentum in case of Momemtum optimizer
        self.momentum = 0.9

        # The number of epoch before decaying learning rate
        self.num_epochs_per_decay = 35
        self.decay_rate = 0.8

        # Number of epochs to train
        self.num_epochs = 1000
        self.calc_num_iters()

        # Dropout's keep_prob for input layer
        self.input_keep_prob = 1.0

        # Dropout's keep_prob for the layer just before output layer
        self.output_keep_prob = 0.5

        # Number of steps to train while validation accuracy doesn't increase
        self.early_stopping_rounds = self.num_iters // 3

        # Probability of choosing a random label instead of the ground-truth
        self.label_smoothing = 0.0

        # Whether we should balance the class weights or not
        self.balance_loss = True

        # The maximum value of a loss balancing weight; None for infinity
        self.max_loss_weight = None

        # Thresholds to compute false positive/negative metrics
        self.thresholds = np.arange(0.0, 1.0, 0.1, dtype=np.float32)


class EvaluateConfig(RunConfig):
    """Configuration for evaluation mode."""

    def __init__(self, num_shards, examples_per_shard):
        super(EvaluateConfig, self).__init__(num_shards, examples_per_shard)
        # The size of a evaluation batch
        self.batch_size = 32

        # Each evaluation pass through some part of the dataset
        self.num_epochs = 1

        # Dropout's keep_prob for input layer
        self.input_keep_prob = 1.0

        self.calc_num_iters()
