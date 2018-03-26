# -*- coding: utf-8 -*-
# @Author: Alexander Sharov


# todo
def get_data():
    return NotImplementedError()

import geopandas

# Query for the highways within the `sg_boundary` we obtained earlier from the sg_admin.
# NB this does take on the order of minutes to run
df = geopandas.osm.query_osm('way', sg_boundary, recurse='down', tags='highway')

# This gives us lots of columns we don't need, so we'll isolate it to the ones we do need
df = df[df.type == 'LineString'][['highway', 'name', 'geometry']]

df.plot()
