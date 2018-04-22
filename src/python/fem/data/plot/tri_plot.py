# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib.pyplot as plt
import datetime
import numpy as np
import os
import scipy.interpolate as interp
import io

from PIL import Image
from mpl_toolkits.mplot3d import Axes3D

from utils import find


# This option needs for escaping 'RuntimeWarning: More than 20 figures have been opened'
plt.rcParams.update({'figure.max_open_warning': 0})


def draw_3d_frame(path, title, functions, times):
    os.makedirs(path + '/' + title, exist_ok=True)

    z_max = find.z_max(functions)

    for func, time in zip(functions, times):
        date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        X = func[:, 0]
        Y = func[:, 1]
        Z = func[:, 2]

        ax.set_xlim3d(np.min(X), np.max(X))
        ax.set_ylim3d(np.min(Y), np.max(Y))
        ax.set_zlim3d(0, z_max)

        ax.plot(X, Y, Z)

        plt.title('график функции %s' % title + '\n' + 'time = %s' % time)
        buf = io.BytesIO()

        plt.savefig(buf, format='png')
        plt.close()

        buf.seek(0)
        im = Image.open(buf)
        im.save(path + '/' + title + '/%s.png' % datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f"), "PNG")
        buf.close()


def draw_3d_surf(path, title, functions, times, view='surface'):
    os.makedirs(path + '/' + title, exist_ok=True)

    z_max = find.z_max(functions)

    for func, time in zip(functions, times):
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        X = func[:, 0]
        Y = func[:, 1]
        Z = func[:, 2]

        ax.set_xlim3d(np.min(X), np.max(X))
        ax.set_ylim3d(np.min(Y), np.max(Y))
        ax.set_zlim3d(0, z_max)

        plotx, ploty, = np.meshgrid(np.linspace(np.min(X), np.max(X), 10), \
                                    np.linspace(np.min(Y), np.max(Y), 10))
        plotz = interp.griddata((X, Y), Z, (plotx, ploty), method='linear')

        # Explanation: TODO
        plotz[plotz < 0.] = 0

        if view == 'surface':
            ax.plot_surface(plotx, ploty, plotz, cstride=1, rstride=1, cmap='viridis')
        elif view == 'wireframe':
            ax.plot_wireframe(plotx, ploty, plotz, cstride=1, rstride=1, cmap='viridis')

        plt.title('график функции $%s$' % title + '\n' + 'time = %s' % time)

        buf = io.BytesIO()

        plt.savefig(buf, format='png')
        plt.close()

        buf.seek(0)
        im = Image.open(buf)
        im.save(path + '/' + title + '/%s.png' % datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f"), "PNG")
        buf.close()
