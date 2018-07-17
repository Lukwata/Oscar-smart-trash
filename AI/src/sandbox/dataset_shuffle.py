import tensorflow as tf


def repeat_before_shuffle(N, batch_size, buffer_size):
    # Repeat the data for N epochs before shuffling
    dataset = tf.data.Dataset.range(batch_size)
    dataset = dataset.repeat(N)
    dataset = dataset.shuffle(buffer_size=buffer_size)

    # Get each element sequentially from buffer
    iterator = dataset.make_one_shot_iterator()
    next_element = iterator.get_next()

    # Results
    d = []
    with tf.Session() as sess:
        for _ in range(N):
            d.append([])
            for _ in range(batch_size):
                d[-1].append(sess.run(next_element))

    print("Expectation: each batch may see duplicate samples because "
          "shuffling only done once at the beginning.")
    print("Results:", d)


def shuffle_before_repeat(N, batch_size, buffer_size):
    # Shuffle the dataset and repeat the dataset operation for N epochs
    dataset = tf.data.Dataset.range(batch_size)
    dataset = dataset.shuffle(buffer_size=buffer_size)
    dataset = dataset.repeat(N)

    # Get each element sequentially from buffer
    iterator = dataset.make_one_shot_iterator()
    next_element = iterator.get_next()

    # Results
    d = []
    with tf.Session() as sess:
        for _ in range(N):
            d.append([])
            for _ in range(batch_size):
                d[-1].append(sess.run(next_element))

    print("Expectation: the samples are not duplicated in each epoch and the "
          "order of samples in each epoch is different. The repeat op repeats "
          "the ops (not the dataset) that makes the dataset. Hence each epoch "
          "is reshuffled at the beginning.")
    print("Results:", d)


def main():
    # Number of epochs, batch_size and shuffle buffer size
    N = 3
    batch_size = 4
    buffer_size = 100

    repeat_before_shuffle(N, batch_size, buffer_size)
    shuffle_before_repeat(N, batch_size, buffer_size)


if __name__ == '__main__':
    main()
