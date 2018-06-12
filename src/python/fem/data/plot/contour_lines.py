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
from data.plot.poly_contour import plot as dplot

INTERPOLATION_NODES = 500


def draw_psi_2d(path, title, functions, times, mesh):
    os.makedirs(path + '/' + title, exist_ok=True)

    x_max = find.maximum(functions, 'x')
    x_min = find.minimum(functions, 'x')
    y_max = find.maximum(functions, 'y')
    y_min = find.minimum(functions, 'y')

    for func, time in zip(functions, times):
        plt.figure()

        ax = plt.subplot(111, aspect='equal')
        dplot(ax, **mesh.raw_splitting)

        x = func[:, 0]
        y = func[:, 1]
        z = func[:, 2]

        xi = np.linspace(x_min, x_max, INTERPOLATION_NODES)
        yi = np.linspace(y_min, y_max, INTERPOLATION_NODES)

        X, Y = np.meshgrid(xi, yi)
        Z = griddata((x, y), z, (X, Y), method='cubic')

        CS = plt.contour(X, Y, Z, colors='black')

        plt.clabel(CS, fontsize='small', inline=10)
        plt.imshow(Z, extent=[x_min, x_max, y_min, y_max],
                   origin='lower', cmap='RdBu',
                   interpolation='kaiser', alpha=0.5)

        plt.colorbar()
        plt.grid()
        plt.title('plot of $\%s$' % title + '\n' + 'time = %s' % time)

        buf = io.BytesIO()

        plt.savefig(buf, format='png')
        plt.close()

        buf.seek(0)
        im = Image.open(buf)
        im.save(path + '/' + title + '/%s.png' % datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S_%f'), 'PNG')
        buf.close()
