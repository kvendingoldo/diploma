# -*- coding: utf-8 -*-
# @Author: Alexander Sharov

from bson.binary import Binary
from pymongo import MongoClient
from datetime import datetime

from utils import serialize, deserialize


def connect(url='mongodb://localhost:27017/', db_name='results_of_experiments', collection_name='data'):
    client = MongoClient(url)
    db = client[db_name]
    return db[collection_name]


def write(images, solution_vector, mesh_type, mesh_step, time, quantity_of_fe, filename, collection=None):

    bimages = list()
    for image in images:
        bimages.append(Binary(serialize(image)))

    record = {
        "date": datetime.now().strftime("%Y-%m-%d-%H-%M"),
        "images": bimages,
        "solution_vector": Binary(serialize(solution_vector)),
        "meta": {
            "mesh": {
                "type": mesh_type,
                "step": mesh_step
            },
            "time": str(time),
            "quantity_of_basis_functions": str(quantity_of_fe),
            "lake_file_name": filename
        }
    }

    collection.insert(record)


def read(date, collection=None):
    return collection.find_one({"date": date})



