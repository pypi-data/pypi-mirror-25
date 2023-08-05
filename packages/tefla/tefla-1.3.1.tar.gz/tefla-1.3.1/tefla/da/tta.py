# Original code from: https://github.com/sveitser/kaggle_diabetic
# Original MIT license:
# https://github.com/sveitser/kaggle_diabetic/blob/master/LICENSE
"""Test-time augmentation tools"""
from __future__ import division, print_function, absolute_import

import ghalton
import numpy as np
from scipy.special import erfinv

from . import data


def uniform(sample, lo=-1, hi=1):
    return lo + (hi - lo) * sample


def normal(sample, avg=0.0, std=1.0):
    return avg + std * np.sqrt(2) * erfinv(2 * sample - 1)


def bernoulli(sample, p=0.5):
    return (sample > p)


def build_quasirandom_transforms(num_transforms, color_sigma, zoom_range,
                                 rotation_range, shear_range,
                                 translation_range, do_flip=True,
                                 allow_stretch=False, skip=0):
    """Quasi Random transform for test images, determinastic random transform

    Args:
        num_transforms: a int, total numbers of transform
        color_sigma: a float, color noise
        zoom_range: a tuple (min_zoom, max_zoom)
        rotation_range: a tuple(min_angle, max_angle)
        shear_range: a tuple(min_shear, max_shear)
        translation_range: a tuple(min_shift, max_shift)
        do_flip: a bool, flip an image
        allow_stretch: a bool, allow stretching

    Returns:
        transform instance and color vecs

    """
    gen = ghalton.Halton(10)
    uniform_samples = np.array(gen.get(num_transforms + skip))[skip:]

    tfs = []
    for s in uniform_samples:
        rotation = uniform(s[0], *rotation_range)
        shift_x = uniform(s[1], *translation_range)
        shift_y = uniform(s[2], *translation_range)
        translation = (shift_x, shift_y)

        # setting shear last because we're not using it at the moment
        shear = uniform(s[9], *shear_range)

        if do_flip:
            flip = bernoulli(s[8], p=0.5)
        else:
            flip = False

        log_zoom_range = [np.log(z) for z in zoom_range]
        if isinstance(allow_stretch, float):
            log_stretch_range = [-np.log(allow_stretch), np.log(allow_stretch)]
            zoom = np.exp(uniform(s[6], *log_zoom_range))
            stretch = np.exp(uniform(s[7], *log_stretch_range))
            zoom_x = zoom * stretch
            zoom_y = zoom / stretch
        elif allow_stretch is True:  # avoid bugs, f.e. when it is an integer
            zoom_x = np.exp(uniform(s[6], *log_zoom_range))
            zoom_y = np.exp(uniform(s[7], *log_zoom_range))
        else:
            zoom_x = zoom_y = np.exp(uniform(s[6], *log_zoom_range))
        # the range should be multiplicatively symmetric, so [1/1.1, 1.1]
        # instead of [0.9, 1.1] makes more sense.

        tfs.append(data.build_augmentation_transform((zoom_x, zoom_y),
                                                     rotation, shear, translation, flip))

    color_vecs = [normal(s[3:6], avg=0.0, std=color_sigma)
                  for s in uniform_samples]

    return tfs, color_vecs
