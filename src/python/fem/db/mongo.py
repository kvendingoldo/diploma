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


def write(db, collection, data_dir, mesh_type, time, quantity_of_fe, mesh_file_path):
    fs = gridfs.GridFS(db)

    frame_q1_id = fs.put(open('%s/frame/q_1/image.gif' % data_dir, 'rb'))
    frame_q2_id = fs.put(open('%s/frame/q_2/image.gif' % data_dir, 'rb'))
    frame_H_id = fs.put(open('%s/frame/H/image.gif' % data_dir, 'rb'))

    surf_q1_id = fs.put(open('%s/surf/q_1/image.gif' % data_dir, 'rb'))
    surf_q2_id = fs.put(open('%s/surf/q_2/image.gif' % data_dir, 'rb'))
    surf_H_id = fs.put(open('%s/surf/H/image.gif' % data_dir, 'rb'))

    wave_psi1_id = fs.put(open('%s/wave/psi_1/image.gif' % data_dir, 'rb'))
    wave_psi2_id = fs.put(open('%s/wave/psi_2/image.gif' % data_dir, 'rb'))

    mesh_file_id = fs.put(open(mesh_file_path, 'rb'))

    record = {
        "date": datetime.now().strftime("%Y-%m-%d-%H-%M"),
        "images": {
            "frame": {
                "q1": frame_q1_id,
                "q2": frame_q2_id,
                "H": frame_H_id
            },
            "surface": {
                "q1": surf_q1_id,
                "q2": surf_q2_id,
                "H": surf_H_id
            },
            "wave": {
                "psi1": wave_psi1_id,
                "psi2": wave_psi2_id
            }
        },
        "solution": {
            "matrix": json.load(open('%s/json/solution.json' % data_dir)),
            "time": json.load(open('%s/json/times.json' % data_dir))
        },
        "meta": {
            "mesh": {
                "type": mesh_type,
                "file": mesh_file_id
            },
            "time": str(time),
            "quantity_of_basis_functions": str(quantity_of_fe)
        }
    }
    db[collection].insert(record)


def read(db, collection, date):
    return db[collection].find_one({"date": date})
