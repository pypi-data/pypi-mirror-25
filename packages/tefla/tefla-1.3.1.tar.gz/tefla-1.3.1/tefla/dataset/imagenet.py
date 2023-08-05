import os
import numpy as np
import scipy.misc
import math
from ..da.preprocessor import ImagenetPreprocessor
from ..da.standardizer import SamplewiseStandardizer
import tensorflow as tf


class Imagenet(object):

    def __init__(self, name='imagenet', data_dir=None, is_label_filename=None, is_train=None, standardizer=SamplewiseStandardizer(clip=6), batch_size=32, extension='.jpg', capacity=1024, min_queue_examples=256, num_preprocess_threads=8):
        self.name = name
        self.data_dir = data_dir
        self.is_train = is_train
        self.preprocessor = ImagenetPreprocessor()
        self.standardizer = standardizer
        self.label_filename = is_label_filename
        self.batch_size = batch_size
        self.extension = extension
        self.capacity = capacity
        self.min_queue_examples = min_queue_examples
        self.num_preprocess_threads = num_preprocess_threads
        if is_train:
            self._num_examples_per_epoch = len(
                open(os.path.join(data_dir, 'train.txt'), 'r').readlines())
        else:
            self._num_examples_per_epoch = len(
                open(os.path.join(data_dir, 'val.txt'), 'r').readlines())

    @property
    def n_iters_per_epoch(self):
        return int(math.ceil(self._num_examples_per_epoch / float(self.batch_size)))

    def decode_file(self, filename_queue, height, width):
        imageValue = tf.read_file(filename_queue[0])
        image_bytes = tf.image.decode_jpeg(imageValue)
        image = tf.reshape(image_bytes, (height, width, 3))
        image = tf.to_float(image)
        return image

    def datafiles(self, height):
        if self.is_train:
            with open(self.data_dir + 'train.txt', 'r') as f:
                files = f.readlines()
            image_files = [os.path.join(self.data_dir, 'images_' + str(
                height), filename.strip('\n') + self.extension) for filename in files]

            filename_queue = tf.train.slice_input_producer(
                [image_files], shuffle=True)
        else:
            with open(self.data_dir + 'val.txt', 'r') as f:
                files = f.readlines()
            image_files = [os.path.join(self.data_dir, 'images_' + str(
                height), filename.strip('\n') + self.extension) for filename in files]
        filename_queue = tf.train.slice_input_producer(
            [image_files], shuffle=True)
        return filename_queue

    def get_batch(self, batch_size=32, height=None, width=None, output_height=None, output_width=None):
        """Construct a queued batch of images and labels.
        Args:
            image: 3-D Tensor of [height, width, 3] of type.float32.
            label: 3-D Tensor of [height, width, 1] type.int32
                min_queue_examples: int32, minimum number of samples to retain
                in the queue that provides of batches of examples.
            batch_size: Number of images per batch.
            shuffle: boolean indicating whether to use a shuffling queue.
        Returns:
            images: Images. 4D tensor of [batch_size, height, width, 3] size.
            labels: Labels. 3D tensor of [batch_size, height, width] size.
        """
        if self.is_train:
            filename_queue = self.datafiles(height)
            image = self.decode_file(filename_queue, height, width)
            image = self.preprocessor.preprocess_image(
                image, output_height, output_width, True, standardizer=self.standardizer)
            image = tf.transpose(image, perm=[1, 0, 2])
            image_batch = tf.train.shuffle_batch(
                [image],
                batch_size=batch_size,
                num_threads=self.num_preprocess_threads,
                capacity=self.capacity,
                min_after_dequeue=self.min_queue_examples)
        else:
            filename_queue = self.datafiles(height)
            image = self.decode_file(
                filename_queue, height=height, width=width)
            image = self.preprocessor.preprocess_image(
                image, output_height, output_width, False, standardizer=self.standardizer)
            image = tf.transpose(image, perm=[1, 0, 2])
            image = seg_input_aug(image, label)
            image_batch = tf.train.batch(
                [image],
                batch_size=batch_size,
                num_threads=self.num_preprocess_threads,
                capacity=self.capacity)

        return image_batch


if __name__ == '__main__':
    sess = tf.Session()
    data_voc = PascalVoc(name='pascal_voc', data_dir='/home/artelus_server/data/VOCdevkit/segment/', batch_size=1,
                         height=224, extension='.jpg', is_train=True, capacity=1024, min_queue_examples=256, num_preprocess_threads=8)
    images, labels = data_voc.get_batch(
        batch_size=1, label_filename=None)
    coord = tf.train.Coordinator()
    tf.train.start_queue_runners(sess=sess, coord=coord)
    import itertools
    for i in itertools.count():
        image, label = sess.run([images, labels])
        import matplotlib.pyplot as plt
        plt.imshow(label.squeeze())
        plt.show()
        print(image.shape)
        print(label.shape)
        print(sum(sum(label)))
    coord.request_stop()
    coord.join(stop_grace_period_secs=0.05)
    # sess.close()
