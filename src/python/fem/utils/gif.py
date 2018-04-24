# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import glob
import datetime
import imageio


def build_file(directory, file_list, duration):
    images = list()
    for filename in file_list:
        images.append(imageio.imread(filename))
    output_file = directory + '/image.gif'
    imageio.mimsave(output_file, images, duration=duration)


def create(directory, duration=1):
    file_list = glob.glob(directory + '/*.png')
    build_file(directory, file_list, duration)
