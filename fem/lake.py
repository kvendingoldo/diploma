# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import matplotlib

matplotlib.use('TkAgg')

import json  # reading geojson files
import matplotlib.pyplot as plt  # plotting data
from shapely.geometry import asShape  # manipulating geometry
from descartes import PolygonPatch  # integrating geom object to matplot

import io

with io.open('baikal.json', 'r', encoding='utf8') as f:
    data = json.load(f)

# initiate the plot axes
fig = plt.figure()
ax = fig.gca(xlabel="Longitude", ylabel="Latitude")

for feat in data["features"]:
    print(feat)
    geom = asShape(feat["geometry"])
    x, y = geom.centroid.x, geom.centroid.y
    ax.plot(x, y, 'ro')
    ax.add_patch(PolygonPatch(feat["geometry"], fc='blue', ec='brown',
                              alpha=0.5, lw=0.5, ls='--', zorder=2))

plt.savefig("data\siaya_wards.png")
plt.show()
