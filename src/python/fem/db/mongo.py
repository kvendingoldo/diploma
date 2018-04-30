# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

import json
import gridfs

from pymongo import MongoClient
from datetime import datetime


def connect(url='mongodb://localhost:27017/', db_name='experiments'):
    client = MongoClient(url)
    db = client[db_name]
    return db


def write(db, collection, data_dir, mesh_type, mesh_name, time, quantity_of_fe):
    fs = gridfs.GridFS(db)

    frame_q1_id = fs.put(open('%s/frame/q_1/image.gif' % data_dir, 'rb'))
    frame_q2_id = fs.put(open('%s/frame/q_2/image.gif' % data_dir, 'rb'))
    frame_H_id = fs.put(open('%s/frame/H/image.gif' % data_dir, 'rb'))

    surf_q1_id = fs.put(open('%s/surf/q_1/image.gif' % data_dir, 'rb'))
    surf_q2_id = fs.put(open('%s/surf/q_2/image.gif' % data_dir, 'rb'))
    surf_H_id = fs.put(open('%s/surf/H/image.gif' % data_dir, 'rb'))

    wave_psi1_id = fs.put(open('%s/wave/psi_1/image.gif' % data_dir, 'rb'))
    wave_psi2_id = fs.put(open('%s/wave/psi_2/image.gif' % data_dir, 'rb'))

    record = {
        "date": datetime.now().strftime("%Y-%m-%d-%H-%M"),
        "images": {
            "frame": {
                "fluid_flow": {
                    "1": frame_q1_id,
                    "2": frame_q2_id
                },
                "surface_elevation": frame_H_id
            },
            "surface": {
                "fluid_flow": {
                    "1": surf_q1_id,
                    "2": surf_q2_id
                },
                "surface_elevation": surf_H_id
            },
            "stream_function": {
                "1": wave_psi1_id,
                "2": wave_psi2_id
            }
        },
        "solution": {
            "matrix": json.load(open('%s/json/solution.json' % data_dir)),
            "times": json.load(open('%s/json/times.json' % data_dir))
        },
        "meta": {
            "mesh": {
                "type": mesh_type,
                "name": mesh_name
            },
            "execution_time": str(time),
            "quantity_of_basis_functions": str(quantity_of_fe)
        }
    }
    db[collection].insert(record)


def read(db, collection, date):
    return db[collection].find_one({"date": date})


def save(db, data, dir):
    fs = gridfs.GridFS(db)

    print(data)
    print(data['meta'])

    with open('%s/solution.json' % dir, 'w') as f:
        json.dump(data['solution'], f)

    with open('%s/meta.json' % dir, 'w') as f:
        json.dump(data['meta'], f)

    with open('%s/frame_fluid_flow_1.gif' % dir, 'wb') as f:
        f.write(fs.get(data['images']['frame']['fluid_flow']['1']).read())

    with open('%s/frame_fluid_flow_2.gif' % dir, 'wb') as f:
        f.write(fs.get(data['images']['frame']['fluid_flow']['2']).read())

    with open('%s/frame_surface_elevation.gif' % dir, 'wb') as f:
        f.write(fs.get(data['images']['frame']['surface_elevation']).read())

    with open('%s/surf_fluid_flow_1.gif' % dir, 'wb') as f:
        f.write(fs.get(data['images']['surf']['fluid_flow']['1']).read())

    with open('%s/surf_fluid_flow_2.gif' % dir, 'wb') as f:
        f.write(fs.get(data['images']['surf']['fluid_flow']['2']).read())

    with open('%s/surf_surface_elevation.gif' % dir, 'wb') as f:
        f.write(fs.get(data['images']['surf']['surface_elevation']).read())

    with open('%s/stream_function_1.gif' % dir, 'wb') as f:
        f.write(fs.get(data['images']['stream_function']['1']).read())

    with open('%s/stream_function_2.gif' % dir, 'wb') as f:
        f.write(fs.get(data['images']['stream_function']['2']).read())
