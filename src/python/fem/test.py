from db import mongo

#####

DATA_DIR = '/Users/ashraov/home/asharov/data/22_04_2018_18_17_14_647414'

MESH_TYPE = 'pqas.001D'
MESH_FILENAME = 'lake_elton.poly'

mongo.write(DATA_DIR, MESH_TYPE, 0, 419, MESH_FILENAME)
