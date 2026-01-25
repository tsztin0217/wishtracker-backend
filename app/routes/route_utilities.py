from flask import abort, make_response
from ..db import db
import requests
import os

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    response = new_model.to_dict()

    return response, 201