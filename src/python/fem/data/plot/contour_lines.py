# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import os
import numpy as np
import matplotlib.pyplot as plt
import io
import datetime

from PIL import Image
from scipy.interpolate import griddata
from utils import find


def draw_psi_2d(path, title, functions, times):
    os.makedirs(path + '/' + title, exist_ok=True)

    x_max = find.maximum(functions, 'x')
    y_max = find.maximum(functions, 'y')

    for func, time in zip(functions, times):
        fig = plt.figure()

        x = func[:, 0]
        y = func[:, 1]
        z = func[:, 2]

        xi = np.linspace(0., x_max, 10)
        yi = np.linspace(0., y_max, 10)

        X, Y = np.meshgrid(xi, yi)
        Z = griddata((x, y), z, (X, Y), method='cubic')

        CS = plt.contour(X, Y, Z, colors='black')

        plt.clabel(CS, fontsize='small', inline=10)
        plt.imshow(Z, extent=[0., x_max, 0, y_max],
                   origin='lower', cmap='coolwarm',
                   interpolation='gaussian', alpha=0.5)

        plt.colorbar()
        plt.grid()
        plt.title('график функции $\%s$' % title + '\n' + 'time = %s' % time)

        buf = io.BytesIO()

        plt.savefig(buf, format='png')
        plt.close()

        buf.seek(0)
        im = Image.open(buf)
        im.save(path + '/' + title + '/%s.png' % datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S_%f'), 'PNG')
        buf.close()
