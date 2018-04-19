# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import gc
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from sympy import Symbol, lambdify


def draw_3d(func, filename='contour_lines.png'):
    x_lim = (-100, 100)
    y_lim = (-100, 100)
    z_lim = (-100, 100)

    a = np.linspace(x_lim[0], x_lim[1], 1000)
    b = np.linspace(y_lim[0], y_lim[1], 1000)
    x, y = np.meshgrid(a, b)

    func = lambdify((Symbol('x_1'), Symbol('x_1')), func, 'numpy')

    fig = plt.figure()

    ax = fig.gca(projection='3d')
    ax.plot_surface(x, y, func(x, y), rstride=8, cstride=8, alpha=0.3)
    cset = ax.contour(x, y, func(x, y), zdir='z', offset=-100, cmap=mpl.winter)
    cset = ax.contour(x, y, func(x, y), zdir='x', offset=-40, cmap=mpl.winter)
    cset = ax.contour(x, y, func(x, y), zdir='y', offset=40, cmap=mpl.winter)

    ax.set_xlabel('X')
    ax.set_xlim(x_lim[0], x_lim[1])
    ax.set_ylabel('Y')
    ax.set_ylim(y_lim[0], y_lim[1])
    ax.set_zlabel('Z')
    ax.set_zlim(z_lim[0], z_lim[1])

    plt.title('contour lines')
    plt.savefig(filename)

    fig.clf()
    plt.close()

    del a, b
    gc.collect()


def draw_2d(func, filename='contour_lines.png'):
    x_lim = (-5, 5)
    y_lim = (-5, 5)

    a = np.linspace(x_lim[0], x_lim[1], 1000)
    b = np.linspace(y_lim[0], y_lim[1], 1000)
    x, y = np.meshgrid(a, b)

    func = lambdify((Symbol('x_1'), Symbol('x_2')), func, 'numpy')

    fig = plt.figure()
    CS = plt.contour(x, y, func(x, y))
    plt.clabel(CS, fontsize='small', inline=10)
    plt.grid()

    ax = fig.gca()
    ax.set_xlabel('X')
    ax.set_xlim(x_lim[0], x_lim[1])
    ax.set_ylabel('Y')
    ax.set_ylim(y_lim[0], y_lim[1])

    plt.title('contour lines')
    plt.savefig(filename)

    fig.clf()
    plt.close()

    del a, b
    gc.collect()

