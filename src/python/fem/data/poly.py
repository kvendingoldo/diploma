# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from numpy import array


def read_pts(file_name):
    file = open(file_name, 'r')

    lines = file.readlines()
    file.close()
    lines = [x.strip('\n').split() for x in lines]

    vertices = []
    N_vertices, dimension, _, _ = [int(x) for x in lines[0]]
    for k in range(N_vertices):
        label, x, y = [items for items in lines[k + 1]]
        vertices.append([float(x), float(y)])
    output = array(vertices)

    return output


def read_tri(file_name):
    """
    Simple poly-file reader, that creates a python dictionary
    with information about vertices, edges and holes.
    It assumes that vertices have no attributes or boundary markers.
    It assumes that edges have no boundary markers.
    No regional attributes or area constraints are parsed.
    """

    output = {'vertices': None, 'holes': None, 'segments': None}

    # open file and store lines in a list
    file = open(file_name, 'r')

    lines = file.readlines()
    file.close()
    lines = [x.strip('\n').split() for x in lines]

    # store vertices
    vertices = []
    N_vertices, dimension, attr, bdry_markers = [int(x) for x in lines[0]]
    # We assume attr = bdrt_markers = 0
    for k in range(N_vertices):
        label, x, y = [items for items in lines[k + 1]]
        vertices.append([float(x), float(y)])
    output['vertices'] = array(vertices)

    # store segments
    segments = []
    N_segments, bdry_markers = [int(x) for x in lines[N_vertices + 1]]
    for k in range(N_segments):
        label, pointer_1, pointer_2 = [items for items in lines[N_vertices + k + 2]]
        segments.append([int(pointer_1) - 1, int(pointer_2) - 1])
    output['segments'] = array(segments)

    # Store holes
    N_holes = int(lines[N_segments + N_vertices + 2][0])
    holes = []
    for k in range(N_holes):
        label, x, y = [items for items in lines[N_segments + N_vertices + 3 + k]]
        holes.append([float(x), float(y)])

    output['holes'] = array(holes)

    return output
